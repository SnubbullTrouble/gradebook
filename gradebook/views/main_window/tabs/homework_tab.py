from gradebook.database.models import BaseModel, Assignment
from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import classes as class_service
from PySide6 import QtWidgets
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Student


class Homework(Tab):

    _assignment_list: list[Assignment] = []

    def __init__(self):
        super().__init__()

    def on_save_data(self) -> None:
        '''
        Slot to handle data saving.
        '''
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    def on_fetch_data(self, model: BaseModel) -> None:
        '''
        Slot to handle data fetching.
        '''
        # Get all the homeworks for the class


        # Get all the homework questions for each homework

        # Get the list of students in the class
        students: list["Student"] = class_service.get_students_in_class(model.id)

        # For all students in the class

        # Get all the homework question scores

        # Get the homework assignment scores

        self._assignment_list = None # TODO

    def on_refresh_view(self) -> None:
        '''
        Slot to handle view refreshing.
        '''
        return # TODO
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Student Number", "Last Name", "First Name"])
        for student in self._roster_data:
            index = self.table_widget.rowCount()
            self.table_widget.insertRow(index)
            self.table_widget.setItem(index, 0, (QtWidgets.QTableWidgetItem(student.student_number)))
            self.table_widget.setItem(index, 1, (QtWidgets.QTableWidgetItem(student.last_name)))
            self.table_widget.setItem(index, 2, (QtWidgets.QTableWidgetItem(student.first_name)))

    def _get_roster(self, class_id: int) -> list["Student"]:
        '''
        Get all the students in the class.

        Returns:
            list: All students in the class
        '''
        return 