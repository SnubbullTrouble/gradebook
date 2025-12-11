from PySide6 import QtWidgets, QtCore
from gradebook.views.class_window.ui_new_class import Ui_NewClassDialog


class NewClassWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow) -> None:
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_NewClassDialog()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.dStart.setDate(QtCore.QDate.currentDate())
        self.ui.dEnd.setDate(QtCore.QDate.currentDate().addMonths(4))
