from gradebook.views.main_window.ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from gradebook.views.class_window.class_window import ClassWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._connect_handlers()


    def _connect_handlers(self):
        self.ui.actionClasses.triggered.connect(self._open_classes_window)

    def _open_classes_window(self):
        dialog = ClassWindow(self)
        dialog.exec()
