# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'phonetic_mark_tool.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1035, 600)
        MainWindow.setMaximumSize(QtCore.QSize(1035, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Basic_Dashboard_UI_fix_option_machine_tools-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 70, 231, 41))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 60, 231, 41))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.le_recorded_file_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.le_recorded_file_dir.setGeometry(QtCore.QRect(70, 110, 311, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.le_recorded_file_dir.setFont(font)
        self.le_recorded_file_dir.setObjectName("le_recorded_file_dir")
        self.le_record_file_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.le_record_file_dir.setGeometry(QtCore.QRect(560, 110, 311, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.le_record_file_dir.setFont(font)
        self.le_record_file_dir.setObjectName("le_record_file_dir")
        self.pb_recorded_file_dir = QtWidgets.QPushButton(self.centralwidget)
        self.pb_recorded_file_dir.setGeometry(QtCore.QRect(410, 110, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_recorded_file_dir.setFont(font)
        self.pb_recorded_file_dir.setObjectName("pb_recorded_file_dir")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 140, 231, 41))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.le_recorded_mono_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.le_recorded_mono_dir.setGeometry(QtCore.QRect(70, 180, 311, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.le_recorded_mono_dir.setFont(font)
        self.le_recorded_mono_dir.setObjectName("le_recorded_mono_dir")
        self.pb_recorded_mono_file_dir = QtWidgets.QPushButton(self.centralwidget)
        self.pb_recorded_mono_file_dir.setGeometry(QtCore.QRect(410, 180, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_recorded_mono_file_dir.setFont(font)
        self.pb_recorded_mono_file_dir.setObjectName("pb_recorded_mono_file_dir")
        self.pb_mark_mono_file = QtWidgets.QPushButton(self.centralwidget)
        self.pb_mark_mono_file.setGeometry(QtCore.QRect(120, 230, 201, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_mark_mono_file.setFont(font)
        self.pb_mark_mono_file.setObjectName("pb_mark_mono_file")
        self.pb_record_file_dir = QtWidgets.QPushButton(self.centralwidget)
        self.pb_record_file_dir.setGeometry(QtCore.QRect(890, 110, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_record_file_dir.setFont(font)
        self.pb_record_file_dir.setObjectName("pb_record_file_dir")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(570, 140, 231, 41))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.le_record_full_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.le_record_full_dir.setGeometry(QtCore.QRect(560, 180, 311, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.le_record_full_dir.setFont(font)
        self.le_record_full_dir.setObjectName("le_record_full_dir")
        self.pb_record_full_dir = QtWidgets.QPushButton(self.centralwidget)
        self.pb_record_full_dir.setGeometry(QtCore.QRect(890, 180, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_record_full_dir.setFont(font)
        self.pb_record_full_dir.setObjectName("pb_record_full_dir")
        self.pb_mark_full_file = QtWidgets.QPushButton(self.centralwidget)
        self.pb_mark_full_file.setGeometry(QtCore.QRect(620, 230, 201, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_mark_full_file.setFont(font)
        self.pb_mark_full_file.setObjectName("pb_mark_full_file")
        self.tb_error_file = QtWidgets.QTextBrowser(self.centralwidget)
        self.tb_error_file.setGeometry(QtCore.QRect(70, 280, 441, 201))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tb_error_file.setFont(font)
        self.tb_error_file.setObjectName("tb_error_file")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1035, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "注音標記tool"))
        self.label.setText(_translate("MainWindow", "已錄音的文字檔資料夾路徑"))
        self.label_2.setText(_translate("MainWindow", "未錄音的文字檔資料夾路徑"))
        self.pb_recorded_file_dir.setText(_translate("MainWindow", "選擇"))
        self.label_3.setText(_translate("MainWindow", "mono檔資料夾路徑"))
        self.pb_recorded_mono_file_dir.setText(_translate("MainWindow", "選擇"))
        self.pb_mark_mono_file.setText(_translate("MainWindow", "產生注音檔及分析檔"))
        self.pb_record_file_dir.setText(_translate("MainWindow", "選擇"))
        self.label_4.setText(_translate("MainWindow", "full檔資料夾路徑"))
        self.pb_record_full_dir.setText(_translate("MainWindow", "選擇"))
        self.pb_mark_full_file.setText(_translate("MainWindow", "產生注音檔"))

