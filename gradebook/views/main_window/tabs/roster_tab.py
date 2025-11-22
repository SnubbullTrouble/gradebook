from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import classes as class_service
from PySide6 import QtWidgets
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Student, Class

class Roster(Tab):

    _roster_data: list["Student"] = []

    def __init__(self) -> None:
        '''
        Initialize the Tab with a reference to the main window.
        '''
        super().__init__()

    @property
    def roster(self) -> list["Student"]:
        '''
        Property to get the roster data.
        '''
        return self._roster_data

    def on_save_data(self) -> None:
        '''
        Slot to handle data saving.
        '''
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    def on_fetch_data(self, model: "Class") -> None:
        '''
        Slot to handle data fetching.
        '''
        self._roster_data = class_service.get_students_in_class(model.id)

    def on_refresh_view(self) -> list["Student"]:
        '''
        Slot to handle view refreshing.
        '''
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Student Number", "Last Name", "First Name"])
        for student in self._roster_data:
            index = self.table_widget.rowCount()
            self.table_widget.insertRow(index)
            self.table_widget.setItem(index, 0, (QtWidgets.QTableWidgetItem(student.student_number)))
            self.table_widget.setItem(index, 1, (QtWidgets.QTableWidgetItem(student.last_name)))
            self.table_widget.setItem(index, 2, (QtWidgets.QTableWidgetItem(student.first_name)))