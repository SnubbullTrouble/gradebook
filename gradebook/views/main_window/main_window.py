from gradebook.views.main_window.ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtWidgets, QtCore
from gradebook.views.class_window.class_window import ClassWindow
from gradebook.database.services import classes as class_service
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Class, Student


class MainWindow(QMainWindow):

    # Signals
    _fetch_class = QtCore.Signal()
    _fetch_roster = QtCore.Signal()
    _class_changed = QtCore.Signal()

    # UI data
    _unsaved_changes = []

    # Database data
    _selected_roster = None
    _selected_class = None

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._connect_handlers()

        # UI
        self._set_status("Ready")
        self.ui.lClassName.setText("No class selected")

    @property
    def _current_class(self) -> "Class":
        '''
        Property to get all class data.
        '''
        return self._selected_class
    
    @_current_class.setter
    def _current_class(self, value: "Class") -> None:
        '''
        Property setter to set all class data.
        '''
        self._selected_class = value    
        self._refresh_tables()
        self.ui.lClassName.setText(value.name)

    @property
    def _roster(self) -> list["Student"]:
        '''
        Property to get the class roster.
        '''
        return self._selected_roster

    # View Management

    def _refresh_tables(self) -> None:
        '''
        Refresh all data tables in the main window.
        '''
        self._refresh_roster_table()

    def _refresh_roster_table(self) -> None:
        '''
        Refresh the class roster table.
        '''
        if self._roster:
            self.ui.tRoster.setRowCount(len(self._roster))
            for row, student in enumerate(self._roster):
                self.ui.tRoster.setItem(row, 0, QtWidgets.QTableWidgetItem(student.student_number))
                self.ui.tRoster.setItem(row, 1, QtWidgets.QTableWidgetItem(student.last_name))
                self.ui.tRoster.setItem(row, 2, QtWidgets.QTableWidgetItem(student.first_name))
        else:
            self.ui.tRoster.setRowCount(0)
            self._set_status("No students enrolled in this class.")

    # Data Management

    def _fetch_roster_data(self) -> None:
        '''
        Load roster data for the selected class.
        '''
        try:
            self._selected_roster = class_service.get_students_in_class(self._current_class.id)
        except Exception as e:
            self._set_status(f"Error - Failed to load roster data: {e}")

    def _fetch_class_data(self) -> None:
        '''
        Load data for the selected class.
        '''
        try:
            self._current_class = class_service.get_class_by_id(self._selected_class.id)
        except Exception as e:
            self._set_status(f"Error - Failed to load class data: {e}")


    # UI Management


    def _open_classes_window(self) -> None:
        '''
        Open the Classes window to select a class.
        '''
        dialog = ClassWindow(self)
        dialog.exec()

        if dialog.result() == QtWidgets.QDialog.Accepted:
            self._current_class = dialog.selected_class

    def _set_status(self, message: str) -> None:
        '''
        Set the status bar message.
        '''
        self.ui.lStatus.setText(f"Status: {message}")

    def _connect_handlers(self) -> None:
        '''
        Connect menu actions to their handlers.
        '''
        # Actions
        self.ui.actionClasses.triggered.connect(self._open_classes_window)

        # Handlers


        # Signals
        self._class_changed.connect(self._refresh_tables)
        self._fetch_class.connect(self._fetch_class_data)
        self._fetch_roster.connect(self._fetch_roster_data)