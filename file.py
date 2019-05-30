import os
import shutil
import traceback
from enum import Enum
import subprocess


class Encoding(Enum):
    UTF8 = 0,
    BIG5 = 1

    encodings = {
        UTF8: 'utf-8',
        BIG5: 'big5hkscs'
    }


class FileTool:

    @classmethod
    def convert_to_multiple_file_by_line(cls, source_filepath, big5_file_dir, utf8_file_dir, source_encoding):
        try:
            # 先清空utf8及big5資料夾原有文字檔
            shutil.rmtree(big5_file_dir)
            os.mkdir(big5_file_dir)
            shutil.rmtree(utf8_file_dir)
            os.mkdir(utf8_file_dir)

            # 選擇原始檔案的編碼
            encoding = ''
            if source_encoding == Encoding.BIG5:
                encoding = Encoding.encodings.value[Encoding.BIG5.value]
            elif source_encoding == Encoding.UTF8:
                encoding = Encoding.encodings.value[Encoding.UTF8.value]

            # 將原始檔案的每一行轉為一個檔案，並且各轉為UTF-8、BIG5編碼
            with open(source_filepath, encoding=encoding) as f:
                line_count = 0
                if source_encoding == Encoding.BIG5:
                    for line in f:
                        line = line.strip()
                        with open(big5_file_dir + '/' + str(line_count) + '.txt', 'w',
                                  encoding=Encoding.encodings.value[source_encoding.value]) as w:
                            w.write(line)
                        line = line.encode(Encoding.encodings.value[Encoding.UTF8.value])
                        with open(utf8_file_dir + '/' + str(line_count) + '.txt', 'wb') as w:
                            w.write(line)
                        line_count += 1
                elif source_encoding == Encoding.UTF8:
                    for line in f:
                        line = line.strip()
                        with open(utf8_file_dir + '/' + str(line_count) + '.txt', 'w', encoding=Encoding.encodings.value[source_encoding.value]) as w:
                            w.write(line)
                        line_count += 1
                    # 利用convertz來轉換utf-8為big5編碼，因為big5hkscs可能不夠用
                    # 利用大神的工具去做轉換
                    ConvertZTool.convert_file(utf8_file_dir + '\\', Encoding.UTF8, Encoding.BIG5, big5_file_dir + '\\')

        except Exception as e:
            traceback.print_exc()
            raise e

    # 將BIG5編碼的檔案轉為UTF-8編碼的檔案
    @classmethod
    def big5_utf8(cls, big5_dir, utf8_dir):
        try:
            shutil.rmtree(utf8_dir)
            os.mkdir(utf8_dir)
            big5_paths = os.listdir(big5_dir)
            for path in big5_paths:
                with open(big5_dir + path, 'r', encoding=Encoding.encodings[Encoding.BIG5]) as f:
                    line = f.read().strip().encode(Encoding.encodings[Encoding.UTF8])
                    with open(utf8_dir + path, 'wb') as w:
                        w.write(line)
        except Exception as e:
            traceback.print_exc()
            raise e


class ConvertZTool:

    CONVERTZ_EXE = 'ConvertZ/convertz'
    SOURCE_ENCODING_ORDER = {
        Encoding.UTF8: '/i:utf8',
        Encoding.BIG5: '/i:big5'
    }
    DEST_ENCODING_ORDER = {
        Encoding.UTF8: '/o:utf8',
        Encoding.BIG5: '/o:big5'
    }

    @classmethod
    def convert_file(cls, source_filepath, source_encoding,
                            dest_encoding, dest_filepath=None):
        order = [cls.CONVERTZ_EXE,
                 cls.SOURCE_ENCODING_ORDER[source_encoding],
                 cls.DEST_ENCODING_ORDER[dest_encoding]]
        if os.path.isdir(source_filepath):
            source_filepath += '*'
            order.append(source_filepath)
            if dest_filepath:
                dest_filepath += '*'
                order.append(dest_filepath)
        else:
            order.append(source_filepath)
            if dest_filepath:
                order.append(dest_filepath)
        print(order)
        subprocess.call(order)