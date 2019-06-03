import os
import statistics
from decimal import Decimal
import traceback
import os.path
from pathlib import Path
from file import FileTool, Encoding, ConvertZTool


class PhoneticMarkTool:
    # 文字語料資料夾位置
    corpus_path = Path('corpus/')
    # 文字語料檔案位置
    corpus_file = Path('corpus/corpus.txt')
    # 文字語料big5編碼資料夾位置
    corpus_big5_path = Path('corpus/big5/')
    # 文字語料utf8編碼資料夾位置
    corpus_utf8_path = Path('corpus/utf8/')
    # lab檔案資料夾位置
    label_path = Path('label/')
    # lab檔案為half-full格式的資料夾位置
    label_half_full_path = Path('label/half_full/')
    # lab檔案為mono格式的資料夾位置
    label_mono_path = Path('label/mono/')
    # 全部文字語料標註注音的檔案
    mark_path = Path('mark.txt')
    # 將文字語料標註注音後，每一句將其分句之資料夾位置
    sentence_mark_path = Path('sentence_mark/')
    # 音節時長分析檔位置
    phonetic_analysis_path = Path('phonetic_analysis.txt')
    # 單句時長分析檔位置
    sentences_analysis_path = Path('sentences_analysis.txt')
    # 注音與音節的對照表檔案位置(必要檔案需存在)
    phonetic_compare_file = 'data/phonetic_compare.txt'
    # 注音音調對照表檔案位置(必要檔案需存在)
    tone_compare_file = 'data/tone_compare.txt'

    default_all_path = [corpus_path, corpus_big5_path, corpus_utf8_path,
                label_path, label_half_full_path, label_mono_path,
                sentence_mark_path]
    important_path = [phonetic_compare_file, tone_compare_file]

    # 特殊拼音，遇到需跳過
    special_pron = ['pau', 'L', 'niL']
    # 常見的符號，用來過濾語料句子之用
    full_punctuation = ' ，。：!"#$%&\\()*+,-./:;<=>?@[\\]^_`{|}~→↓△▿⋄•！？。?〞＃＄％＆』（）＊＋－╱︰；＜＝＞＠〔╲〕 ＿ˋ｛∣｝∼、〃》「」『』【】﹝﹞【】〝〞–—『』「」…﹏'

    # 檢查預設的檔案路徑是否存在，沒有存在則自動建立
    @classmethod
    def check_default_path(cls):
        for path in cls.default_all_path:
            if not (path.exists()):
                path.mkdir()

    @classmethod
    def produce_corpus_split_file(cls, encoding):
        if not (cls.corpus_file.exists()):
            return 'corpus/corpus.txt =>' + '檔案不存在，無法產生'
        else:
            try:
                FileTool.convert_to_multiple_file_by_line(str(cls.corpus_file.resolve()),
                                                          str(cls.corpus_big5_path.resolve()),
                                                          str(cls.corpus_utf8_path.resolve()),
                                                          encoding)
                return '兩種分句檔產生成功!'
            except Exception as e:
                traceback.print_exc()
                return '轉換編碼失敗，檢查介面選擇的編碼與實際檔案編碼是否一致'

    # 挑出時長錯誤的mono lab檔案
    @classmethod
    def pick_wrong_mono_file(cls):
        mono_file_paths = cls.filepath_list(str(cls.label_mono_path.resolve()))

        try:
            # 檢查出有哪些時長錯誤的mono lab檔案
            wrong_dict = cls.check_wrong_mono_file(mono_file_paths)
            wrong_filepaths = dict(
                (os.path.basename(mono_file_paths[wrong_index]), reason) for (wrong_index, reason) in wrong_dict.items())
            return wrong_filepaths
        except Exception as e:
            raise e

    # 標記mono lab的注音
    @classmethod
    def mark_mono_file(cls):
        try:
            ConvertZTool.convert_file(source_filepath=str(cls.corpus_big5_path.resolve()) + '\\',
                                      source_encoding=Encoding.BIG5,
                                      dest_filepath=str(cls.corpus_utf8_path.resolve()) + '\\',
                                      dest_encoding=Encoding.UTF8)

            recorded_file_paths = cls.filepath_list(str(cls.corpus_utf8_path.resolve()))
            mono_file_paths = cls.filepath_list(str(cls.label_mono_path.resolve()))
            recorded_table, wrong_filepaths = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
            c_table, v_table = cls.read_c_v_table()
            tone_table = cls.read_tone_table()
            phonetic_table, pron_dict = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
            cls.write_mark_file(phonetic_table, str(cls.mark_path.resolve()))
            cls.split_mark_file(str(cls.mark_path.resolve()), str(cls.sentence_mark_path.resolve()))
            message = '產生兩種注音檔成功!'
        except Exception as e:
            traceback.print_exc()
            message = '產生失敗'
        return message

    # 產生音節時長分析檔
    @classmethod
    def produce_phone_analysis(cls, encoding):
        try:
            # 如果txt檔案是big5編碼，則先轉成utf8
            if encoding == Encoding.BIG5:
                ConvertZTool.convert_file(source_filepath=str(cls.corpus_big5_path.resolve()) + '\\',
                                          source_encoding=Encoding.BIG5,
                                          dest_filepath=str(cls.corpus_utf8_path.resolve()) + '\\',
                                          dest_encoding=Encoding.UTF8)

            recorded_file_paths = cls.filepath_list(str(cls.corpus_utf8_path.resolve()))
            mono_file_paths = cls.filepath_list(str(cls.label_mono_path.resolve()))
            recorded_table, wrong_filepaths = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
            c_table, v_table = cls.read_c_v_table()
            tone_table = cls.read_tone_table()
            phonetic_table, pron_dict = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
            cls.calculate_pron(mono_file_paths, pron_dict, str(cls.phonetic_analysis_path.resolve()))
            message = '產生音節時長分析檔成功!'
        except:
            traceback.print_exc()
            message = '產生失敗'
        return message

    @classmethod
    def produce_sentence_analysis(cls, encoding):
        try:
            # 如果txt檔案是big5編碼，則先轉成utf8
            if encoding == Encoding.BIG5:
                ConvertZTool.convert_file(source_filepath=str(cls.corpus_big5_path.resolve()) + '\\',
                                          source_encoding=Encoding.BIG5,
                                          dest_filepath=str(cls.corpus_utf8_path.resolve()) + '\\',
                                          dest_encoding=Encoding.UTF8)

            recorded_file_paths = cls.filepath_list(str(cls.corpus_utf8_path.resolve()))
            mono_file_paths = cls.filepath_list(str(cls.label_mono_path.resolve()))
            recorded_table, wrong_filepaths = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
            c_table, v_table = cls.read_c_v_table()
            tone_table = cls.read_tone_table()
            phonetic_table, pron_dict = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
            cls.calculate_sentence_pron(mono_file_paths, pron_dict, str(cls.sentences_analysis_path.resolve()))
            message = '產生單句時長分析檔成功!'
        except:
            traceback.print_exc()
            message = '產生失敗'
        return message

    # 標記 half-full lab的注音
    @classmethod
    def mark_full_file(cls, encoding):
        try:
            # 如果txt檔案是big5編碼，則先轉成utf8
            if encoding == Encoding.BIG5:
                ConvertZTool.convert_file(source_filepath=str(cls.corpus_big5_path.resolve()) + '\\',
                                          source_encoding=Encoding.BIG5,
                                          dest_filepath=str(cls.corpus_utf8_path.resolve()) + '\\',
                                          dest_encoding=Encoding.UTF8)

            # 讀取utf8資料夾的文字檔及half-full資料夾的lab檔案
            record_file_paths = cls.filepath_list(str(cls.corpus_utf8_path.resolve()))
            full_file_paths = cls.filepath_list(str(cls.label_half_full_path.resolve()))
            # 根據文字檔跟lab檔案產生, 不會檢查是否有錯的lab檔案(無從檢查)
            record_table = cls.produce_record_table(record_file_paths, full_file_paths)
            # 讀取注音與音節的對照表
            c_table, v_table = cls.read_c_v_table()
            # 讀取音調表
            tone_table = cls.read_tone_table()
            # 標記注音
            phonetic_table, pron_dict = cls.mark_phonetic(record_table, c_table, v_table, tone_table)
            # 將注音檔寫檔出來，兩種格式:多句一檔、單句多檔
            cls.write_mark_file(phonetic_table, str(cls.mark_path.resolve()))
            cls.split_mark_file(cls.mark_path, str(cls.sentence_mark_path.resolve()))
            message = '兩種注音檔產生成功!'
        except Exception as e:
            traceback.print_exc()
            message = '兩種注音檔產生失敗!'
        return message

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

    # 檢查出哪些mono lab檔有錯:時長為負數、時常相減不符合標準
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
                    with open(split_mark_file_dir + '/' + str(file_count) + '.txt', 'w', encoding='utf-8') as w:
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






