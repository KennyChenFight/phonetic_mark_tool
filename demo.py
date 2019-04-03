from phonetic import PhoneticMarkTool
# import os
# import sys
# from phonetic_mark_tool import Ui_MainWindow
# from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton, QMainWindow
#
#
# class AppWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.pb_recorded_file_dir.clicked.connect(self.recorded_file_dir_click)
#         self.ui.pb_recorded_mono_file_dir.clicked.connect(self.recorded_mono_file_dir_click)
#         self.ui.pb_mark_mono_file.clicked.connect(self.mark_mono_file_click)
#         self.ui.pb_record_file_dir.clicked.connect(self.record_file_dir_click)
#         self.ui.pb_record_full_dir.clicked.connect(self.record_full_file_dir_click)
#         self.ui.pb_mark_full_file.clicked.connect(self.mark_full_file_click)
#
#     def recorded_file_dir_click(self):
#         dir = QFileDialog.getExistingDirectory(self,
#                                                '選取資料夾',
#                                                './')
#         self.ui.le_recorded_file_dir.setText(dir)
#
#     def recorded_mono_file_dir_click(self):
#         dir = QFileDialog.getExistingDirectory(self,
#                                                '選取資料夾',
#                                                './')
#         self.ui.le_recorded_mono_dir.setText(dir)
#
#     def mark_mono_file_click(self):
#         mark_file, filetype = QFileDialog. \
#             getSaveFileName(self,
#                             "選取注音檔存放位置",
#                             "./",
#                             "Text Files (*.txt)")
#         pron_file, filetype = QFileDialog. \
#             getSaveFileName(self,
#                             "選取分析檔存放位置",
#                             "./",
#                             "Text Files (*.txt)")
#
#         recorded_file_dir = self.ui.le_recorded_file_dir.text()
#         recorded_mono_file_dir = self.ui.le_recorded_mono_dir.text()
#         error_files = PhoneticMarkTool.mark_mono_file(recorded_file_dir, recorded_mono_file_dir, mark_file, pron_file)
#
#         QMessageBox.information(self,
#                                 '>_<',
#                                 '檔案產生成功!',
#                                 QMessageBox.Yes)
#         message = ''
#         for path, reason in error_files.items():
#             message += path + '   ' + reason + '\n'
#         self.ui.tb_error_file.setText(message)
#
#     def record_file_dir_click(self):
#         dir = QFileDialog.getExistingDirectory(self,
#                                                '選取資料夾',
#                                                './')
#         self.ui.le_record_file_dir.setText(dir)
#
#     def record_full_file_dir_click(self):
#         dir = QFileDialog.getExistingDirectory(self,
#                                                '選取資料夾',
#                                                './')
#         self.ui.le_record_full_dir.setText(dir)
#
#     def mark_full_file_click(self):
#         filepath, filetype = QFileDialog. \
#             getSaveFileName(self,
#                             "選取文件",
#                             "./",
#                             "Text Files (*.txt)")
#         record_file_dir = self.ui.le_record_file_dir.text()
#         record_full_file_dir = self.ui.le_record_full_dir.text()
#         PhoneticMarkTool.mark_full_file(record_file_dir, record_full_file_dir, filepath)
#
#         QMessageBox.information(self,
#                                 '>_<',
#                                 '檔案產生成功!',
#                                 QMessageBox.Yes)
#
#
# app = QApplication(sys.argv)
# w = AppWindow()
# w.show()
# sys.exit(app.exec_())

recorded_file_dir = 'C:\\Users\\P19054\\Desktop\\recorded\\txt\\'
recorded_mono_dir = 'C:\\Users\\P19054\\Desktop\\recorded\\mono\\'
recorded_mark_file = 'C:\\Users\\P19054\\Desktop\\recorded\\mark.txt'
pron_file = 'C:\\Users\\P19054\\Desktop\\recorded\\pron.txt'

# record_file_dir = 'C:\\Users\\P19054\\Desktop\\407\\txt'
# record_full_dir = 'C:\\Users\\P19054\\Desktop\\407\\full'
# record_mark_file = 'C:\\Users\\P19054\\Desktop\\407\\mark.txt'

# wrong_filepaths = PhoneticMarkTool.mark_mono_file(recorded_file_dir, recorded_mono_dir, recorded_mark_file, pron_file)
# print(wrong_filepaths)
#PhoneticMarkTool.mark_full_file(record_file_dir, record_full_dir, record_mark_file)

PhoneticMarkTool.write_problem_sentence_file('problem.txt')