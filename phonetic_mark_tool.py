from phonetic import PhoneticMarkTool
import os
from file import FileTool, Encoding
from pathlib import Path
import traceback
import sys
from phonetic_mark_tool_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton, QMainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.check_default_dir()
        self.ui.pb_big5_utf8.clicked.connect(self.big5_utf8_click)
        self.ui.pb_mark_full_file.clicked.connect(self.mark_full_file_click)
        self.ui.pb_wrong_lab.clicked.connect(self.wrong_mono_lab_file_click)
        self.ui.pb_mark_mono_file.clicked.connect(self.mark_mono_file_click)
        self.ui.pb_phone_analysis.clicked.connect(self.phonetic_analysis_file_click)
        self.ui.pb_sentences_analysis.clicked.connect(self.sentences_analysis_file_click)

    def check_default_dir(self):
        PhoneticMarkTool.check_default_path()

    def big5_utf8_click(self):
        if self.ui.rb_big5.isChecked():
            encoding = Encoding.BIG5
        elif self.ui.rb_utf8.isChecked():
            encoding = Encoding.UTF8
        message = PhoneticMarkTool.produce_corpus_split_file(encoding)
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)

    def mark_full_file_click(self):
        if self.ui.rb_big5_2.isChecked():
            encoding = Encoding.BIG5
        elif self.ui.rb_utf8_2.isChecked():
            encoding = Encoding.UTF8
        message = PhoneticMarkTool.mark_full_file(encoding)
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)

    def wrong_mono_lab_file_click(self):
        try:
            wrong_filepaths = PhoneticMarkTool.pick_wrong_mono_file()
            message = ''
            if wrong_filepaths:
                for path, reason in wrong_filepaths.items():
                    message += path + '   ' + reason + '\n'
            else:
                message = '無錯誤lab檔案'

            self.ui.tb_wrong_lab.setText(message)
            QMessageBox.information(self,
                                '>_<',
                                '處理結束!',
                                QMessageBox.Yes)
        except:
            traceback.print_exc()
            QMessageBox.warning(self,
                                '>_<',
                                '檢查失敗',
                                QMessageBox.Yes)

    def mark_mono_file_click(self):
        message = PhoneticMarkTool.mark_mono_file()
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)

    def phonetic_analysis_file_click(self):
        if self.ui.rb_big5_3.isChecked():
            encoding = Encoding.BIG5
        elif self.ui.rb_utf8_3.isChecked():
            encoding = Encoding.UTF8

        message = PhoneticMarkTool.produce_phone_analysis(encoding)
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)

    def sentences_analysis_file_click(self):
        if self.ui.rb_big5_3.isChecked():
            encoding = Encoding.BIG5
        elif self.ui.rb_utf8_3.isChecked():
            encoding = Encoding.UTF8

        message = PhoneticMarkTool.produce_sentence_analysis(encoding)
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())


# recorded_file_dir = 'corpus/big5/'
# utf8_file_dir = 'corpus/utf8/'
# FileTool.big5_utf8(recorded_file_dir, utf8_file_dir)
#
# recorded_file_dir = 'corpus/utf8/'
# mono_file_dir = 'label/mono/'
# analysis_file = 'sentences_analysis.txt'
# PhoneticMarkTool.produce_sentence_analysis(recorded_file_dir, mono_file_dir, analysis_file)
