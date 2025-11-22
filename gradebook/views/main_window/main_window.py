from gradebook.views.main_window.ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtWidgets
from gradebook.views.class_window.class_window import ClassWindow

class MainWindow(QMainWindow):

    _selected_class = None

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._connect_handlers()

    def _connect_handlers(self) -> None:
        '''
        Connect menu actions to their handlers.
        '''
        self.ui.actionClasses.triggered.connect(self._open_classes_window)

    def _open_classes_window(self) -> None:
        '''
        Open the Classes window to select a class.
        '''
        dialog = ClassWindow(self)
        dialog.exec()

        if dialog.result() == QtWidgets.QDialog.Accepted:
            selected_class = dialog.selected_class
