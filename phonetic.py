import os
import statistics
from decimal import Decimal
import traceback
import os.path


class PhoneticMarkTool:
    # 注音與音節的對照表(固定檔案)
    phonetic_compare_file = 'data/phonetic_compare.txt'
    # 注音音調對照表(固定檔案)
    tone_compare_file = 'data/tone_compare.txt'
    # 特殊音節，遇到需跳過
    special_pron = ['pau', 'L', 'niL']
    # 過濾標點符號之用
    full_punctuation = ' ，。：!"#$%&\\()*+,-./:;<=>?@[\\]^_`{|}~→↓△▿⋄•！？。?〞＃＄％＆』（）＊＋－╱︰；＜＝＞＠〔╲〕 ＿ˋ｛∣｝∼、〃》「」『』【】﹝﹞【】〝〞–—『』「」…﹏'

    @classmethod
    def pick_wrong_mono_file(cls,
                       mono_file_dir):
        mono_file_paths = cls.filepath_list(mono_file_dir)
        try:
            wrong_dict = cls.check_wrong_mono_file(mono_file_paths)
            wrong_filepaths = dict(
                (mono_file_paths[wrong_index], reason) for (wrong_index, reason) in wrong_dict.items())
        except:
            traceback.print_exc()
        return wrong_filepaths

    # 標記mono file的注音
    @classmethod
    def mark_mono_file(cls, recorded_file_dir,
                       mono_file_dir, mark_file,
                       split_mark_file_dir):
        try:
            recorded_file_paths = cls.filepath_list(recorded_file_dir)
            mono_file_paths = cls.filepath_list(mono_file_dir)
            recorded_table, wrong_filepaths = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
            c_table, v_table = cls.read_c_v_table()
            tone_table = cls.read_tone_table()
            phonetic_table, pron_dict = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
            cls.write_mark_file(phonetic_table, mark_file)
            cls.split_mark_file(mark_file, split_mark_file_dir)
        except Exception as e:
            traceback.print_exc()
            raise e

    @classmethod
    def produce_phone_analysis(cls, recorded_file_dir, mono_file_dir, analysis_file):
        try:
            recorded_file_paths = cls.filepath_list(recorded_file_dir)
            mono_file_paths = cls.filepath_list(mono_file_dir)
            recorded_table, wrong_filepaths = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
            c_table, v_table = cls.read_c_v_table()
            tone_table = cls.read_tone_table()
            phonetic_table, pron_dict = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
            cls.calculate_pron(mono_file_paths, pron_dict, analysis_file)
        except Exception as e:
            traceback.print_exc()
            raise e

    @classmethod
    def produce_sentence_analysis(cls, recorded_file_dir, mono_file_dir, analysis_file):
        try:
            recorded_file_paths = cls.filepath_list(recorded_file_dir)
            mono_file_paths = cls.filepath_list(mono_file_dir)
            recorded_table, wrong_filepaths = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
            c_table, v_table = cls.read_c_v_table()
            tone_table = cls.read_tone_table()
            phonetic_table, pron_dict = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
            cls.calculate_sentence_pron(mono_file_paths, pron_dict, analysis_file)
        except Exception as e:
            traceback.print_exc()
            raise e

    # 標記full file的注音
    @classmethod
    def mark_full_file(cls, record_file_dir,
                       full_file_dir, mark_file, split_mark_file_dir):
        try:
            record_file_paths = cls.filepath_list(record_file_dir)
            full_file_paths = cls.filepath_list(full_file_dir)
            # record_file_paths, full_file_paths = cls.check_same_sentence_file(record_file_paths, full_file_paths)
            record_table = cls.produce_record_table(record_file_paths, full_file_paths)
            c_table, v_table = cls.read_c_v_table()
            tone_table = cls.read_tone_table()
            phonetic_table, pron_dict = cls.mark_phonetic(record_table, c_table, v_table, tone_table)
            cls.write_mark_file(phonetic_table, mark_file)
            cls.split_mark_file(mark_file, split_mark_file_dir)
        except Exception as e:
            print(e)
            traceback.print_exc()
            raise e

    # @classmethod
    # def mark_sentence_with_full_lab(cls, sentence, lab):
    #     record_file_dir = 'corpus/utf8/'
    #     record_full_file_dir = 'label/half_full/'
    #     mark_file = 'mark.txt'
    #     split_mark_file_dir = 'sentence_mark/'
    #     try:
    #         cls.mark_full_file(record_file_dir, record_full_file_dir, mark_file, split_mark_file_dir)
    #     except Exception as e:
    #         print(e)

    # 用來檢查有沒有重複的句子，有的話刪除相同的檔案
    @classmethod
    def check_same_sentence_file(cls, txt_file_paths, pron_file_paths):
        txt = {}
        repeated_file = []
        delete_file = []
        for txt_file in txt_file_paths:
            with open(txt_file, 'r', encoding='utf-8') as f:
                line = ''.join([text for text in f.read() if not (text in cls.full_punctuation)])
                if line in txt:
                    delete_file.append(txt_file)
                    repeated_file.append((txt[line], txt_file))
                else:
                    txt[line] = txt_file
        txt_file_paths = [t for t in txt_file_paths if t not in delete_file]
        delete_file_names = [os.path.basename(t).replace('.txt', '') for t in delete_file]
        pron_file_paths = [t for t in pron_file_paths if os.path.basename(t).replace('.lab', '') not in delete_file_names]

        return txt_file_paths, pron_file_paths

    # 產生已經錄音過的句子與音節的對照表
    @classmethod
    def produce_recorded_table(cls,
                               recorded_file_paths,
                               mono_file_paths):
        wrong_dict = cls.check_wrong_mono_file(mono_file_paths)
        text_list = []
        for index, filepath in enumerate(recorded_file_paths):
            if index not in wrong_dict:
                with open(filepath, 'r', encoding='utf-8') as f:
                    line = ''.join([text for text in f.read() if not (text in cls.full_punctuation)])
                    text_list.append(line)

        pron_list = []
        for index, mono_filepath in enumerate(mono_file_paths):
            if index not in wrong_dict:
                with open(mono_filepath, 'r', encoding='utf-8') as f:
                    pron = []
                    for line in f:
                        line = line.strip()
                        pron.append(''.join([pron for pron in line if not (pron.isdigit() or pron.isspace())]))
                    pron_list.append(pron)

        recorded_table = list(map(list, zip(text_list, pron_list)))
        wrong_filepaths = dict((mono_file_paths[wrong_index], reason) for (wrong_index, reason) in wrong_dict.items())
        return recorded_table, wrong_filepaths

    @classmethod
    def check_wrong_mono_file(cls, mono_file_paths):
        count = 0
        time_collection = {}
        for mono_filepath in mono_file_paths:
            with open(mono_filepath, 'r', encoding='utf-8') as f:
                text_list = []
                line_count = 1
                for line in f:
                    line = line.strip().split(' ')
                    if 'pau' not in line:
                        time_list = []
                        for text in line:
                            if text != '' and text.lstrip('-').isdigit():
                                time_list.append(int(text))
                        time_list.append(line_count)
                        text_list.append(time_list)
                        #text_list.append([int(text) for text in line if text != '' and text.lstrip('-').isdigit()])
                    line_count += 1
                time_collection[count] = text_list
            count += 1

        wrong_dict = {}
        for key, text_list in time_collection.items():
            is_wrong = False
            for time_list in text_list:
                for time in time_list[:-1]:
                    if time < 0:
                        wrong_dict[key] = '時長為負數=>' + '行數:' + str(time_list[-1])
                        is_wrong = True
                        print('時長為負數:', os.path.basename(mono_file_paths[key]))
                        break
                if is_wrong:
                    break

        for key, text_list in time_collection.items():
            if key not in wrong_dict:
                for index, time_list in enumerate(text_list):
                    if index + 1 < len(text_list):
                        time1 = time_list[1]
                        time2 = text_list[index+1][0]
                        if time2 - time1 < -250000:
                            print('時長相減不符合:', os.path.basename(mono_file_paths[key]))
                            wrong_dict[key] = '時長相減不符合=>' + '行數:' + str(time_list[-1] + 1)
                            break
        print('錯誤個數:', len(wrong_dict))
        return wrong_dict

    # 產生還沒錄音的句子與音節的對照表
    @classmethod
    def produce_record_table(cls,
                            record_file_paths,
                            full_file_paths):
        text_list = []
        for filepath in record_file_paths:
            with open(filepath, 'r', encoding='utf-8') as f:
                line = f.read()
                text_list.append(line)
        pron_list = []
        for full_filepath in full_file_paths:
            with open(full_filepath, 'r', encoding='utf-8') as f:
                pron = []
                for line in f:
                    minus_index = line.index('-')
                    add_index = line.index('+')
                    pron.append(line[minus_index + 1:add_index])
                pron_list.append(pron)
        record_table = list(map(list, zip(text_list, pron_list)))
        return record_table

    # 根據傳進來的資料夾路徑，傳回所有檔案的路徑
    @classmethod
    def filepath_list(cls, file_dir):
        return [file_dir + '/' + filename for filename in sorted(os.listdir(file_dir), key=cls.filter_filename)]

    # 根據不同的的檔名進行排序
    @classmethod
    def filter_filename(cls, filename):
        if filename.startswith('a'):
            return int(filename[:-4].replace('a', ''))
        elif filename.startswith('SomeFile_'):
            return int(filename[:-4].replace('SomeFile_', ''))
        else:
            return int(filename[:-4])

    # 讀取注音與音節的對照表
    @classmethod
    def read_c_v_table(cls):
        c_table = {}
        v_table = {}
        with open(cls.phonetic_compare_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                id = int(line[0])
                if id <= 53:
                    c_table[line[2]] = line[1]
                else:
                    v_table[line[2]] = line[1]
        return c_table, v_table

    # 讀取注音音調對照表
    @classmethod
    def read_tone_table(cls):
        tone_table = {}
        with open(cls.tone_compare_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                tone_table[line[2]] = [line[0], line[1]]
        return tone_table

    # 標記每個句子的注音，並產生對照表
    @classmethod
    def mark_phonetic(cls, record_table, c_table, v_table, tone_table):
        pron_dict = {}
        for i, element in enumerate(record_table):
            sentence = element[0]
            pron_list = element[1]
            phonetic_collection = []
            index = 0
            word_count = 0
            while index < len(pron_list):
                pron = pron_list[index]
                if pron in c_table:
                    v1_index = index + 1
                    v2_index = index + 2
                    if pron_list[v1_index] and pron_list[v2_index] in v_table:
                        tone = [pron_list[v1_index][-1:], pron_list[v2_index][-1:]]
                        for key, value in tone_table.items():
                            if value == tone:
                                phonetic_list = [c_table[pron], v_table[pron_list[v1_index]], key]
                                phonetic_collection.append(phonetic_list)
                                if sentence == '花圈的緞帶上寫著深切悼念理查尼克森先生':
                                    print(phonetic_list)
                                    print(sentence[word_count])
                                    print(word_count)
                                word_pron = pron + ' ' + pron_list[v1_index] + ' ' + pron_list[v2_index]
                                if word_pron in pron_dict:
                                    pron_dict[word_pron][0] += 1
                                    pron_dict[word_pron][1].add(sentence[word_count])
                                    pron_dict[word_pron][2].append([i, index, index + 1, index + 2])
                                else:
                                    pron_dict[word_pron] = [1, set(sentence[word_count]),
                                                            [[i, index, index + 1, index + 2]]]
                                word_count += 1
                                index += 3
                                break
                    else:
                        print('找不到')
                        index += 3
                        print(sentence[word_count])
                        word_count += 1
                elif not (pron in cls.special_pron):
                    v1_index = index
                    v2_index = index + 1
                    if (pron_list[v1_index] and pron_list[v2_index]) in v_table:
                        tone = [pron_list[v1_index][-1:], pron_list[v2_index][-1:]]
                        for key, value in tone_table.items():
                            if value == tone:
                                phonetic_list = [v_table[pron_list[v1_index]], key]
                                phonetic_collection.append(phonetic_list)

                                if sentence == '花圈的緞帶上寫著深切悼念理查尼克森先生':
                                    print(phonetic_list)
                                    print(sentence[word_count])
                                    print(word_count)
                                word_pron = pron_list[v1_index] + ' ' + pron_list[v2_index]
                                if word_pron in pron_dict:
                                    pron_dict[word_pron][0] += 1
                                    pron_dict[word_pron][1].add(sentence[word_count])
                                    pron_dict[word_pron][2].append([i, index, index + 1])
                                else:
                                    pron_dict[word_pron] = [1, set(sentence[word_count]), [[i, index, index + 1]]]

                                word_count += 1
                                index += 2
                                break
                    else:
                        print('找不到')
                        index += 2
                        print(sentence[word_count])
                        word_count += 1
                else:
                    print('找不到或是特殊符號')
                    index += 1
            print(sentence, phonetic_collection, pron_list)
            record_table[i][1] = phonetic_collection
        print(pron_dict)
        return record_table, pron_dict

    # 將句子與注音的對照表進行寫檔
    @classmethod
    def write_mark_file(cls, phonetic_table, mark_file):
        with open(mark_file, 'w', encoding='utf-8') as f:
            for index, element in enumerate(phonetic_table):
                sentence = element[0]
                phonetic_list = element[1]
                f.write(sentence + '\n')
                f.write('   '.join([''.join(phonetic) for phonetic in phonetic_list]))
                f.write('\n')

    @classmethod
    def split_mark_file(cls, mark_file, split_mark_file_dir):
        with open(mark_file, 'r', encoding='utf-8') as f:
            line_count = 1
            line_list = []
            file_count = 1
            for line in f:
                line = line.strip()
                line_list.append(line)
                if not(line_count % 2):
                    with open(split_mark_file_dir + str(file_count) + '.txt', 'w', encoding='utf-8') as w:
                        w.write('\n'.join(line_list))
                    line_list = []
                    file_count += 1
                line_count += 1

    @classmethod
    def calculate_pron(cls, mono_filepaths, pron_dict, pron_file):
        all_total_time = []
        for pron, info in pron_dict.items():
            count = info[0]
            total_time = []
            wrong_time_file_index = set()
            for detail in info[2]:
                filepath = mono_filepaths[detail[0]]
                filename_index = int(os.path.basename(filepath).replace('.lab', '').replace('a', ''))
                line_count = 0
                time_start_index = detail[1]
                time_end_index = detail[-1]
                with open(filepath, 'r', encoding='utf-8') as f:
                    time1 = 0
                    time2 = 0
                    for line in f:
                        if line_count == time_start_index:
                            time1 = int(line.strip().split(' ')[0])
                        elif line_count == time_end_index:
                            time2 = int(line.strip().split(' ')[-2])
                            total_time.append((filename_index, round((time2 - time1) / 10000000, 4)))
                            break
                        line_count += 1
            all_total_time.extend(total_time)
            if len(total_time) >= 2:
                average_time = round(statistics.mean([time for index, time in total_time]), 4)
                stdev_time = round(statistics.stdev([time for index, time in total_time]), 4)
            elif len(total_time) == 1:
                average_time = round(statistics.mean([time for index, time in total_time]), 4)
                stdev_time = 0
            else:
                average_time = 0
                stdev_time = 0

            average_time = Decimal(str(average_time))
            stdev_time = Decimal(str(stdev_time))
            upbound_time = average_time + stdev_time
            downbound_time = average_time - stdev_time

            for index, time in total_time:
                if time < downbound_time or time > upbound_time:
                    wrong_time_file_index.add(index)

            wrong_time_file_percentage = int((len(wrong_time_file_index) / count) * 100)

            pron_dict[pron].insert(1, average_time)
            pron_dict[pron].insert(2, stdev_time)
            pron_dict[pron].insert(3, upbound_time)
            pron_dict[pron].insert(4, downbound_time)
            pron_dict[pron].insert(5, wrong_time_file_percentage)
            pron_dict[pron].insert(7, wrong_time_file_index)

        with open(pron_file, 'w', encoding='utf-8') as f:
            for pron, info in pron_dict.items():
                if len(pron.split(' ')) == 2:
                    f.write(' ' + pron + ',')
                else:
                    f.write(pron + ',')
                f.write(str(info[0]) + ',')
                f.write(str(info[1]) + ',')
                f.write(str(info[2]) + ',')
                f.write(str(info[3]) + ',')
                f.write(str(info[4]) + ',')
                f.write(str(info[5]) + '%,')
                f.write('、'.join(info[6]))
                f.write(',')
                if len(info[7]) != 0:
                    f.write('、'.join([str(index) for index in info[7]]))
                else:
                    f.write('無問題句子')
                f.write('\n')

    @classmethod
    def write_problem_sentence_file(cls, filepath):
        with open('mark.txt', 'r', encoding='utf-8') as f:
            line_count = 1
            problem_dict = {}
            for line in f:
                line = line.strip()
                if line_count % 2:
                    sentence_collection = []
                    for index in range(len(line)):
                        if index < len(line) - 1:
                            sentence_split = [line[index], line[index + 1]]
                            sentence_collection.append(sentence_split)
                else:
                    mark_collection = []
                    marks = line.split('   ')
                    for index in range(len(marks)):
                        if index < len(marks) - 1:
                            mark_split = [marks[index], marks[index + 1]]
                            mark_collection.append(mark_split)
                    for index, mark_two_split in enumerate(mark_collection):
                        one_tone = mark_two_split[0][-1]
                        two_tone = mark_two_split[1][-1]
                        if one_tone == 'ˇ' and two_tone == 'ˇ':
                            if line_count - 1 in problem_dict:
                                problem_dict[line_count - 1].append(sentence_collection[index])
                            else:
                                problem_dict[line_count - 1] = [sentence_collection[index]]
                line_count += 1

            with open(filepath, 'w', encoding='utf-8') as w:
                for key, value_collection in problem_dict.items():
                    w.write(str(key) + ',')
                    for value_list in value_collection:
                        w.write(''.join(value_list))
                        w.write(',')
                    w.write('\n')

    @classmethod
    def calculate_sentence_pron(cls, mono_filepaths, pron_dict, pron_file):
        all_total_time = []
        for pron, info in pron_dict.items():
            total_time = []
            for detail in info[2]:
                filepath = mono_filepaths[detail[0]]
                filename_index = int(os.path.basename(filepath).replace('.lab', '').replace('a', ''))
                line_count = 0
                time_start_index = detail[1]
                time_end_index = detail[-1]
                with open(filepath, 'r', encoding='utf-8') as f:
                    time1 = 0
                    time2 = 0
                    for line in f:
                        if line_count == time_start_index:
                            time1 = int(line.strip().split(' ')[0])
                        elif line_count == time_end_index:
                            list = line.strip().split(' ')
                            for index, s in enumerate(list):
                                if index != 0 and s.isdigit():
                                    time2 = int(s)
                                    break
                            total_time.append((filename_index, round((time2 - time1) / 10000000, 4)))
                            break
                        line_count += 1
            all_total_time.extend(total_time)

        all_sentence_time = {}
        all_sentence_length = {}
        for time in all_total_time:
            file_index = time[0]
            if file_index in all_sentence_time:
                all_sentence_time[file_index] += time[1]
                all_sentence_length[file_index] += 1
            else:
                all_sentence_time[file_index] = time[1]
                all_sentence_length[file_index] = 1

        all_sentence_average_time = {}
        for file_index, time in all_sentence_time.items():
            count = all_sentence_length[file_index]
            if count >= 1:
                average_time = round(time / count, 4)
            else:
                average_time = 0
            all_sentence_average_time[file_index] = (count, average_time)

        with open(pron_file, 'w', encoding='utf-8') as f:
            for file_index, sentence_time in sorted(all_sentence_average_time.items()):
                count = sentence_time[0]
                f.write(str(file_index) + ',' + str(count) + ',' + str(sentence_time[1]))
                f.write('\n')






