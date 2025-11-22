from PySide6 import QtWidgets
from gradebook.views.class_window.ui_class_window import Ui_ClassDialog

class ClassWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow) -> None:
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_ClassDialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Classes")
        self.setModal(True)
