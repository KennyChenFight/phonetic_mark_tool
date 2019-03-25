from phonetic import PhoneticMarkTool
import sys
from phonetic_mark_tool import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton, QMainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pb_recorded_file_dir.clicked.connect(self.recorded_file_dir_click)
        self.ui.pb_recorded_mono_file_dir.clicked.connect(self.recorded_mono_file_dir_click)
        self.ui.pb_mark_mono_file.clicked.connect(self.mark_mono_file_click)
        self.ui.pb_record_file_dir.clicked.connect(self.record_file_dir_click)
        self.ui.pb_record_full_dir.clicked.connect(self.record_full_file_dir_click)
        self.ui.pb_mark_full_file.clicked.connect(self.mark_full_file_click)


    def recorded_file_dir_click(self):
        dir = QFileDialog.getExistingDirectory(self,
                                               '選取資料夾',
                                               './')
        self.ui.le_recorded_file_dir.setText(dir)

    def recorded_mono_file_dir_click(self):
        dir = QFileDialog.getExistingDirectory(self,
                                               '選取資料夾',
                                               './')
        self.ui.le_recorded_mono_dir.setText(dir)

    def mark_mono_file_click(self):
        filepath, filetype = QFileDialog. \
            getSaveFileName(self,
                            "選取文件",
                            "./",
                            "Text Files (*.txt)")
        recorded_file_dir = self.ui.le_recorded_file_dir.text()
        recorded_mono_file_dir = self.ui.le_recorded_mono_dir.text()
        PhoneticMarkTool.mark_mono_file(recorded_file_dir, recorded_mono_file_dir, filepath)

        QMessageBox.information(self,
                                '>_<',
                                '檔案產生成功!',
                                QMessageBox.Yes)

    def record_file_dir_click(self):
        dir = QFileDialog.getExistingDirectory(self,
                                               '選取資料夾',
                                               './')
        self.ui.le_record_file_dir.setText(dir)

    def record_full_file_dir_click(self):
        dir = QFileDialog.getExistingDirectory(self,
                                               '選取資料夾',
                                               './')
        self.ui.le_record_full_dir.setText(dir)

    def mark_full_file_click(self):
        filepath, filetype = QFileDialog. \
            getSaveFileName(self,
                            "選取文件",
                            "./",
                            "Text Files (*.txt)")
        record_file_dir = self.ui.le_record_file_dir.text()
        record_full_file_dir = self.ui.le_record_full_dir.text()
        PhoneticMarkTool.mark_full_file(record_file_dir, record_full_file_dir, filepath)

        QMessageBox.information(self,
                                '>_<',
                                '檔案產生成功!',
                                QMessageBox.Yes)


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())

#
# recorded_file_dir = 'recorded/txt/'
# recorded_mono_dir = 'recorded/mono/'
# recorded_mark_file = 'recorded/mark.txt'
#
# record_file_dir = 'record/txt/'
# record_full_dir = 'record/full/'
# record_mark_file = 'record/mark.txt'
#
#
# PhoneticMarkTool.mark_mono_file(recorded_file_dir, recorded_mono_dir, recorded_mark_file)
# PhoneticMarkTool.mark_full_file(record_file_dir, record_full_dir, record_mark_file)
#
#
# # line_collection = []
# # with open('pron_compare.txt', 'r', encoding='utf-8') as f:
# #     for line in f:
# #         line = line.strip().split(',')
# #         line_collection.append(line)
# #
# # phonetic_collection = []
# # with open('phonetic_compare.txt', 'r', encoding='utf-8') as f:
# #     for line in f:
# #         line = line.strip().split(',')
# #         phonetic_collection.append(line)
# #
# #
# # for line in line_collection:
# #     is_exist = False
# #     pron = line[1].split(' ')
# #     for phonetic in phonetic_collection:
# #         if phonetic[2] in pron:
# #             is_exist = True
# #             break
# #     if not(is_exist):
# #         print(line)
#
#
#
