import sys
import os
from phonetic import PhoneticMarkTool
import uuid
import shutil

compare_file = sys.argv[1]
tone_file = sys.argv[2]
sentence = sys.argv[3]
lab = sys.argv[4]

filedirname = str(uuid.uuid4().hex)
record_file_dir = filedirname + '/corpus/utf8/'
record_full_file_dir = filedirname + '/label/half_full/'
mark_file = filedirname + '/mark.txt'
split_mark_file_dir = filedirname + '/sentence_mark/'
os.makedirs(record_file_dir)
os.makedirs(record_full_file_dir)
os.makedirs(split_mark_file_dir)

PhoneticMarkTool.phonetic_compare_file = compare_file
PhoneticMarkTool.tone_compare_file = tone_file

with open(record_file_dir + '0.txt', 'w', encoding='utf-8') as f:
    f.write(sentence)

with open(record_full_file_dir + 'SomeFile_0.lab', 'w', encoding='utf-8', newline='') as f:
    f.write(lab)

try:
    PhoneticMarkTool.mark_full_file(record_file_dir, record_full_file_dir, mark_file, split_mark_file_dir)
    with open(mark_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        sentence = lines[0]
        phonetic = lines[1]

    print(sentence, phonetic)
except Exception as e:
    print(e)

shutil.rmtree(filedirname)


