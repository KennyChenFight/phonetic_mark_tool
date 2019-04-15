import os
import shutil
import traceback


class FileTool:

    @classmethod
    def convert_to_multiple_file_by_line(cls, source_filepath, big5_file_dir, utf8_file_dir):
        try:
            shutil.rmtree(big5_file_dir)
            os.mkdir(big5_file_dir)
            shutil.rmtree(utf8_file_dir)
            os.mkdir(utf8_file_dir)
            with open(source_filepath, encoding='big5hkscs') as f:
                line_count = 0
                for line in f:
                    line = line.strip()
                    with open(big5_file_dir + '/' + str(line_count) + '.txt', 'w', encoding='big5') as w:
                        w.write(line)
                    line = line.encode('utf-8')
                    with open(utf8_file_dir + '/' + str(line_count) + '.txt', 'wb') as w:
                        w.write(line)
                    line_count += 1
        except Exception as e:
            traceback.print_exc()
            raise e

    @classmethod
    def big5_utf8(cls, big5_dir, utf8_dir):
        try:
            shutil.rmtree(utf8_dir)
            os.mkdir(utf8_dir)
            big5_paths = os.listdir(big5_dir)
            for path in big5_paths:
                with open(big5_dir + path, 'r', encoding='big5hkscs') as f:
                    line = f.read().strip().encode('utf-8')
                    with open(utf8_dir + path, 'wb') as w:
                        w.write(line)
        except Exception as e:
            traceback.print_exc()
            raise e
