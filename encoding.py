import chardet
import subprocess
import os
from enum import Enum


class Encoding(Enum):
    UTF8 = 0,
    UTF8_Bom = 1,
    Big5 = 2


class ConvertZTool:

    CONVERTZ_EXE = 'ConvertZ/convertz'
    SOURCE_ENCODING_ORDER = {
        Encoding.UTF8: '/i:utf8',
        Encoding.Big5: '/i:big5'
    }
    DEST_ENCODING_ORDER = {
        Encoding.UTF8: '/o:utf8',
        Encoding.Big5: '/o:big5'
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

        subprocess.call(order)


class EncodingTool:
    encoding = {
        'UTF-8-SIG': Encoding.UTF8_Bom,
        'utf-8': Encoding.UTF8,
        'Big5': Encoding.Big5
    }

    @classmethod
    def convert_utf8_encoding(cls, filepath):
        encoding = cls.get_file_encoding(filepath)

        if encoding == Encoding.UTF8_Bom:
            with open(filepath, 'rb') as f:
                s = f.read().decode('utf-8-sig').encode('utf-8')
            with open(filepath, 'wb') as w:
                w.write(s)
        elif encoding == Encoding.Big5:
            cls.convert_file_encoding(filepath,
                                      Encoding.Big5,
                                      Encoding.UTF8)

    @classmethod
    def convert_big5_encoding(cls, source_filepath, dest_filepath):
        cls.convert_file_encoding(source_filepath,
                                  Encoding.UTF8,
                                  Encoding.Big5,
                                  dest_filepath)

    @classmethod
    def get_file_encoding(cls, filepath):
        with open(filepath, 'rb') as f:
            return cls.encoding[chardet.detect(f.read())['encoding']]

    @classmethod
    def convert_file_encoding(cls,
                              source_filepath,
                              source_encoding,
                              dest_encoding,
                              dest_filepath=None):
        ConvertZTool.convert_file(source_filepath, source_encoding, dest_encoding, dest_filepath)
