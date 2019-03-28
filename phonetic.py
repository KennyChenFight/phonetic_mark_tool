import os


class PhoneticMarkTool:
    # 注音與音節的對照表(固定檔案)
    phonetic_compare_file = 'phonetic_compare.txt'
    # 注音音調對照表(固定檔案)
    tone_compare_file = 'tone_compare.txt'
    # 特殊音節，遇到需跳過
    special_pron = ['pau', 'L', 'niL']
    # 過濾標點符號之用
    full_punctuation = ' ，。：!"#$%&\\()*+,-./:;<=>?@[\\]^_`{|}~→↓△▿⋄•！？。?〞＃＄％＆』（）＊＋－╱︰；＜＝＞＠〔╲〕 ＿ˋ｛∣｝∼、〃》「」『』【】﹝﹞【】〝〞–—『』「」…﹏'

    # 標記mono file的注音
    @classmethod
    def mark_mono_file(cls, recorded_file_dir,
                       mono_file_dir, mark_file):
        recorded_file_paths = cls.filepath_list(recorded_file_dir)
        mono_file_paths = cls.filepath_list(mono_file_dir)
        #recorded_file_paths, mono_file_paths = cls.check_same_sentence_file(recorded_file_paths, mono_file_paths)
        recorded_table = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
        c_table, v_table = cls.read_c_v_table()
        tone_table = cls.read_tone_table()
        phonetic_table = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
        cls.write_mark_file(phonetic_table, mark_file)

    # 標記full file的注音
    @classmethod
    def mark_full_file(cls, record_file_dir,
                       full_file_dir, mark_file):
        record_file_paths = cls.filepath_list(record_file_dir)
        full_file_paths = cls.filepath_list(full_file_dir)
        #record_file_paths, full_file_paths = cls.check_same_sentence_file(record_file_paths, full_file_paths)
        record_table = cls.produce_record_table(record_file_paths, full_file_paths)
        c_table, v_table = cls.read_c_v_table()
        tone_table = cls.read_tone_table()
        phonetic_table = cls.mark_phonetic(record_table, c_table, v_table, tone_table)
        cls.write_mark_file(phonetic_table, mark_file)

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
        # text_set = {}
        text_list = []
        for filepath in recorded_file_paths:
            with open(filepath, 'r', encoding='utf-8') as f:
                line = ''.join([text for text in f.read() if not (text in cls.full_punctuation)])
                text_list.append(line)
                # if line in text_set:
                #     print(filepath)
                #     print(text_set[line])
                #     print(line)
                # else:
                #     text_set[line] = filepath
        pron_list = []
        for mono_filepath in mono_file_paths:
            with open(mono_filepath, 'r', encoding='utf-8') as f:
                pron = []
                for line in f:
                    line = line.strip()
                    pron.append(''.join([pron for pron in line if not (pron.isdigit() or pron.isspace())]))
                pron_list.append(pron)
        #recorded_table = OrderedDict(zip(text_list, pron_list))
        recorded_table = list(map(list, zip(text_list, pron_list)))
        return recorded_table

    # 產生還沒錄音的句子與音節的對照表
    @classmethod
    def produce_record_table(cls,
                            record_file_paths,
                            full_file_paths):
        # text_set = set()
        text_list = []
        for filepath in record_file_paths:
            with open(filepath, 'r', encoding='utf-8') as f:
                line = f.read()
                text_list.append(line)
        #         if line in text_set:
        #             print(line)
        #         else:
        #             text_set.add(line)
        # print(len(text_set))
        pron_list = []
        for full_filepath in full_file_paths:
            with open(full_filepath, 'r', encoding='utf-8') as f:
                pron = []
                for line in f:
                    minus_index = line.index('-')
                    add_index = line.index('+')
                    pron.append(line[minus_index + 1:add_index])
                pron_list.append(pron)
        #recorded_table = OrderedDict(zip(text_list, pron_list))
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
        for i, element in enumerate(record_table):
            sentence = element[0]
            pron_list = element[1]
            phonetic_collection = []
            index = 0
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
                                index += 3
                                break
                    else:
                        print('找不到')
                        index += 3
                elif not (pron in cls.special_pron):
                    v1_index = index
                    v2_index = index + 1
                    if (pron_list[v1_index] and pron_list[v2_index]) in v_table:
                        tone = [pron_list[v1_index][-1:], pron_list[v2_index][-1:]]
                        for key, value in tone_table.items():
                            if value == tone:
                                phonetic_list = [v_table[pron_list[v1_index]], key]
                                phonetic_collection.append(phonetic_list)
                                index += 2
                                break
                    else:
                        print('找不到')
                        index += 2
                else:
                    print('找不到或是特殊符號')
                    index += 1
            print(sentence, phonetic_collection, pron_list)
            record_table[i][1] = phonetic_collection
        return record_table

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
