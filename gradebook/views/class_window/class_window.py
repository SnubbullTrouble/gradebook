from PySide6 import QtWidgets, QtCore, QtGui
from gradebook.views.class_window.ui_class_window import Ui_ClassDialog
from gradebook.views.class_window.new_class_window import NewClassWindow
import gradebook.database.services.classes as class_service

import typing
if typing.TYPE_CHECKING:
    from gradebook.database.models import Class

class ClassWindow(QtWidgets.QDialog):

    _fetch_all_classes = QtCore.Signal()
    _all_classes = []
    _selected_class = None

    def __init__(self, parent: QtWidgets.QMainWindow) -> None:
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_ClassDialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Classes")
        self.setModal(True)

        # Setup controls
        self._connect_signals()

        # Load initial data
        self._fetch_all_classes.emit()
        self.ui.bOpen.setEnabled(False)

    @property
    def selected_class(self) -> "Class | None":
        '''
        Property to get the currently selected class.
        '''
        return self._selected_class

    @property
    def _class_list(self) -> list["Class"]:
        '''
        Property to get the list of classes.
        '''
        return self._all_classes
    
    @_class_list.setter
    def _class_list(self, value: list) -> None:
        '''
        Property setter to set the list of classes and refresh the UI.
        '''
        self._all_classes = value
        self._refresh_class_list()

    def _connect_signals(self) -> None:
        '''
        Connect signals to their respective slots.
        '''
        # Controls
        self.ui.bNew.clicked.connect(self._bNew_clicked)
        self.ui.bOpen.clicked.connect(self._bOpen_clicked)

        # Signals
        self._fetch_all_classes.connect(self._get_all_classes)
        self.ui.lwClassList.itemSelectionChanged.connect(self._update_open_button_state)
        self.ui.lwClassList.itemSelectionChanged.connect(self._set_selected_class)

    def _get_class_by_name(self, name: str) -> "Class | None":
        '''
        Retrieves a class by its name.

        Args:
            name: The name of the class to retrieve.

        Returns:
            Class | None: The Class object if found, otherwise None.
        '''
        for cls in self._class_list:
            if cls.name == name:
                return cls
        return None

    def _set_selected_class(self) -> None:
        '''
        Sets the selected class based on the current selection in the list widget.
        '''
        self._selected_class = self._get_class_by_name(self.ui.lwClassList.currentItem().text().split(',')[0])

    def _update_open_button_state(self) -> None:
        '''
        Enables or disables the Open button based on selection.
        '''
        selected_items = self.ui.lwClassList.selectedItems()
        self.ui.bOpen.setEnabled(bool(selected_items) and len(selected_items) == 1)

    def _bNew_clicked(self) -> None:
        '''
        Opens the New Class window and refreshes the class list upon successful creation.
        '''
        new_class_window = NewClassWindow(self)
        new_class_window.exec()

        if new_class_window.result() == QtWidgets.QDialog.Accepted:
            class_name = new_class_window.ui.tbClassName.text()
            if self._get_class_by_name(class_name):
                QtWidgets.QMessageBox.warning(
                    self,
                    "Duplicate Class",
                    f"A class named '{class_name}' already exists.",
                )
            else:
                class_service.create_class(class_name, new_class_window.ui.dStart.date().toPython(), new_class_window.ui.dEnd.date().toPython())
                self._fetch_all_classes.emit()

    def _refresh_class_list(self) -> None:
        '''
        Updates the list of classes into the list widget.
        '''
        self.ui.lwClassList.clear()
        for cls in self._class_list:
            self.ui.lwClassList.addItem(self._format_class_string(cls))

    def _get_all_classes(self) -> None:
        '''
        Fetches all classes from the database and updates the internal class list.
        '''
        self._class_list = class_service.get_all_classes()

    def _bOpen_clicked(self) -> None:
        '''
        Opens the selected class for further actions.
        '''
        self.accept()

    def _format_class_string(self, cls: "Class") -> QtWidgets.QListWidgetItem:
        '''
        Formats the class information into a string for display.

        Args:
            cls (database.models.Class): The Class object to format.
        
        Returns:
            QListWidgetItem: The formatted list widget item.
        '''
        active = cls.end_date is None or cls.end_date >= QtCore.QDate.currentDate().toPython()

        # Create font
        font = QtGui.QFont()
        if active:
            font.setBold(True)
        else:
            font.setItalic(True)

        # Get number of students from the db
        number_of_students = class_service.get_number_of_students_in_class(cls)

        # Create the status string
        status = f"Active until {cls.end_date}" if active else f"Inactive since {cls.end_date}"

        # Create item and apply font
        item = QtWidgets.QListWidgetItem(f"{cls.name}, Students: {number_of_students}, {status}")
        item.setFont(font)

        return item
