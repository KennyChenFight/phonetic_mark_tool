from encoding import Encoding


class FileTool:

    @classmethod
    def convert_to_multiple_file_by_line(cls, source_filepath, dest_file_dir):
        with open(source_filepath, encoding='utf-8') as f:
            line_count = 1
            for line in f:
                line = line.strip()
                with open(dest_file_dir + '/' + str(line_count) + '.txt', 'w', encoding='utf-8') as w:
                    w.write(line)
                line_count += 1