import os
from collections import OrderedDict


class PhoneticMarkTool:

    phonetic_compare_file = 'phonetic_compare.txt'
    tone_compare_file = 'tone_compare.txt'

    special_pron = ['pau', 'L', 'niL']

    @classmethod
    def mark_mono_file(cls, recorded_file_dir,
                       mono_file_dir, mark_file):
        recorded_file_paths = cls.filepath_list(recorded_file_dir)
        mono_file_paths = cls.filepath_list(mono_file_dir)
        recorded_table = cls.produce_recorded_table(recorded_file_paths, mono_file_paths)
        c_table, v_table = cls.read_c_v_table()
        tone_table = cls.read_tone_table()
        phonetic_table = cls.mark_phonetic(recorded_table, c_table, v_table, tone_table)
        cls.write_mark_file(phonetic_table, mark_file)

    @classmethod
    def mark_full_file(cls, record_file_dir,
                       full_file_dir, mark_file):
        record_file_paths = cls.filepath_list(record_file_dir)
        full_file_paths = cls.filepath_list(full_file_dir)
        record_table = cls.produce_record_table(record_file_paths, full_file_paths)
        c_table, v_table = cls.read_c_v_table()
        tone_table = cls.read_tone_table()
        phonetic_table = cls.mark_phonetic(record_table, c_table, v_table, tone_table)
        cls.write_mark_file(phonetic_table, mark_file)

    @classmethod
    def produce_recorded_table(cls,
                               recorded_file_paths,
                               mono_file_paths):
        text_list = []
        for filepath in recorded_file_paths:
            with open(filepath, 'r', encoding='utf-8') as f:
                text_list.append(f.read())

        pron_list = []
        for mono_filepath in mono_file_paths:
            with open(mono_filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    pron_list.append(''.join([pron for pron in line if not (pron.isdigit() or pron.isspace())]))

        recorded_table = OrderedDict(zip(text_list, [pron_list]))
        return recorded_table

    @classmethod
    def produce_record_table(cls,
                               record_file_paths,
                               full_file_paths):
        text_list = []
        for filepath in record_file_paths:
            with open(filepath, 'r', encoding='utf-8') as f:
                text_list.append(f.read())

        pron_list = []
        for full_filepath in full_file_paths:
            with open(full_filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    minus_index = line.index('-')
                    add_index = line.index('+')
                    pron_list.append(line[minus_index + 1:add_index])

        recorded_table = OrderedDict(zip(text_list, [pron_list]))
        return recorded_table

    @classmethod
    def filepath_list(cls, file_dir):
        return [file_dir + '/' + filename for filename in os.listdir(file_dir)]

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

    @classmethod
    def read_tone_table(cls):
        tone_table = {}
        with open(cls.tone_compare_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                tone_table[line[2]] = [line[0], line[1]]
        return tone_table

    @classmethod
    def mark_phonetic(cls, record_table, c_table, v_table, tone_table):

        for sentence, pron_list in record_table.items():
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
                    index += 1

            record_table[sentence] = phonetic_collection
        print(record_table)
        return record_table

    @classmethod
    def write_mark_file(cls, phonetic_table, mark_file):
        with open(mark_file, 'w', encoding='utf-8') as f:
            for sentence, phonetic_list in phonetic_table.items():
                f.write(sentence + '\n')
                f.write('   '.join([''.join(phonetic) for phonetic in phonetic_list]))




#
# phonetic_compare_file = 'phonetic_compare.txt'
# tone_compare_file = 'tone_compare.txt'
# record_full_file = 'SomeFile_0.lab'
# recorded_mono_file = 'a0001.lab'
# record_file = 'SomeFile.txt'
# record_phonetic_mark_file = 'SomeFile_phonetic.txt'
# special_pron = ['pau', 'L', 'niL']
#
#
# pron_list = []
# with open(recorded_mono_file, 'r', encoding='utf-8') as f:
#     for line in f:
#         line = line.strip()
#         pron_list.append(''.join([pron for pron in line if not(pron.isdigit() or pron.isspace())]))
#
# print(pron_list)

# pron_list = []
# with open(record_full_file, 'r', encoding='utf-8') as f:
#     for line in f:
#         minus_index = line.index('-')
#         add_index = line.index('+')
#         pron_list.append(line[minus_index + 1:add_index])
#
# print(pron_list)
#
# phonetic_collection = []
# index = 0
# while index < len(pron_list):
#     pron = pron_list[index]
#     if pron in c_table:
#         v1_index = index + 1
#         v2_index = index + 2
#         if pron_list[v1_index] and pron_list[v2_index] in v_table:
#             tone = [pron_list[v1_index][-1:], pron_list[v2_index][-1:]]
#             for key, value in tone_compare.items():
#                 if value == tone:
#                     phonetic_list = [c_table[pron], v_table[pron_list[v1_index]], key]
#                     phonetic_collection.append(phonetic_list)
#                     index += 3
#                     break
#     elif not (pron in special_pron):
#         v1_index = index
#         v2_index = index + 1
#         if (pron_list[v1_index] and pron_list[v2_index]) in v_table:
#             tone = [pron_list[v1_index][-1:], pron_list[v2_index][-1:]]
#             for key, value in tone_compare.items():
#                 if value == tone:
#                     phonetic_list = [v_table[pron_list[v1_index]], key]
#                     phonetic_collection.append(phonetic_list)
#                     index += 2
#                     break
#     else:
#         index += 1
#
# print(phonetic_collection)

#
# with open(record_file, 'r', encoding='utf-8') as f:
#         text = f.read()
#
# with open(record_phonetic_mark_file, 'w', encoding='utf-8') as f:
#     f.write(text + '\n')
#     for mark in phonetic_collection:
#         f.write(''.join(mark))
#         f.write('   ')