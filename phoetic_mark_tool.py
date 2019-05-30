from phonetic import PhoneticMarkTool
import os
from file import FileTool, Encoding
from pathlib import Path
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
        message = PhoneticMarkTool.mark_full_file
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)
        # if len(os.listdir(record_file_dir)) != len(os.listdir(record_full_file_dir)):
        #     QMessageBox.warning(self,
        #                             '>_<',
        #                             'label/half_full/\n' +
        #                             '裡面的lab檔案數量不對喔!',
        #                             QMessageBox.Yes)
        #
        # else:
        #     try:
        #         PhoneticMarkTool.mark_full_file(record_file_dir, record_full_file_dir, mark_file, split_mark_file_dir)
        #         QMessageBox.information(self,
        #                                 '>_<',
        #                                 '兩種注音檔產生成功!',
        #                                 QMessageBox.Yes)
        #     except:
        #         QMessageBox.warning(self,
        #                                 '>_<',
        #                                 'Oops!產生過程出錯\n' +
        #                                 '檢查lab檔案跟分句檔是否有互相對應\n' +
        #                                 'ex: 句子的文字少了或多了、檔名出錯',
        #                                 QMessageBox.Yes)

    def wrong_mono_lab_file_click(self):
        mono_file_dir = 'label/mono/'
        try:
            wrong_filepaths = PhoneticMarkTool.pick_wrong_mono_file(mono_file_dir)

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
        except Exception as e:
            QMessageBox.warning(self,
                                '>_<',
                                'Oops!出錯!\n' +
                                '請檢查corpus/big5/下的檔案是否皆為big5編碼',
                                QMessageBox.Yes)

    def mark_mono_file_click(self):
        try:
            recorded_file_dir = 'corpus/big5/'
            utf8_file_dir = 'corpus/utf8/'
            FileTool.big5_utf8(recorded_file_dir, utf8_file_dir)

            recorded_file_dir = 'corpus/utf8/'
            mono_file_dir = 'label/mono/'
            mark_file = 'mark.txt'
            split_mark_file_dir = 'sentence_mark/'
            PhoneticMarkTool.mark_mono_file(recorded_file_dir,
                                            mono_file_dir,
                                            mark_file,
                                            split_mark_file_dir)
            QMessageBox.information(self,
                                    '>_<',
                                    '產生兩種注音檔成功!',
                                    QMessageBox.Yes)
        except:
            QMessageBox.warning(self,
                                '>_<',
                                'Oops!產生過程出錯\n' +
                                '檢查lab檔案跟分句檔是否有互相對應\n' +
                                'ex: 句子的文字少了或多了、檔名出錯',
                                QMessageBox.Yes)

    def phonetic_analysis_file_click(self):
        try:
            recorded_file_dir = 'corpus/big5/'
            utf8_file_dir = 'corpus/utf8/'
            FileTool.big5_utf8(recorded_file_dir, utf8_file_dir)

            recorded_file_dir = 'corpus/utf8/'
            mono_file_dir = 'label/mono/'
            analysis_file = 'phonetic_analysis.txt'
            PhoneticMarkTool.produce_phone_analysis(recorded_file_dir, mono_file_dir, analysis_file)
            QMessageBox.information(self,
                                    '>_<',
                                    '產生音節時長分析檔成功!',
                                    QMessageBox.Yes)
        except Exception as e:
            QMessageBox.warning(self,
                                '>_<',
                                'Oops!產生過程出錯\n',
                                QMessageBox.Yes)

    def sentences_analysis_file_click(self):
        try:
            recorded_file_dir = 'corpus/big5/'
            utf8_file_dir = 'corpus/utf8/'
            FileTool.big5_utf8(recorded_file_dir, utf8_file_dir)

            recorded_file_dir = 'corpus/utf8/'
            mono_file_dir = 'label/mono/'
            analysis_file = 'sentences_analysis.txt'
            PhoneticMarkTool.produce_sentence_analysis(recorded_file_dir, mono_file_dir, analysis_file)
            QMessageBox.information(self,
                                    '>_<',
                                    '產生單句時長分析檔成功!',
                                    QMessageBox.Yes)
        except Exception as e:
            QMessageBox.warning(self,
                                '>_<',
                                'Oops!產生過程出錯\n',
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
