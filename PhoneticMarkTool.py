from phonetic_mark_tool_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton, QMainWindow
import sys


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())