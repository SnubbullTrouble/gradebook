from PySide6.QtWidgets import QDialog, QWidget
from gradebook.views.dialogs.ui_new_student import Ui_Dialog

class NewStudentDialog(QDialog):
    '''
    Dialog to add new students to the roster.
    '''
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.buttonBox.buttons()[0].setEnabled(False)  # Disable OK button initially

        # Handlers
        self.ui.tbRoster.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self) -> None:
        '''
        Enable or disable the OK button based on whether there is text in the textbox.
        '''
        text = self.ui.tbRoster.toPlainText().strip()
        self.ui.buttonBox.buttons()[0].setEnabled(bool(text))
        