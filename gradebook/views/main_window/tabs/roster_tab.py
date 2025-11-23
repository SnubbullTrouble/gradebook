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
    
    @property
    def _headers(self) -> None:
        '''Headers for the View'''
        return ["Student Number", "Last Name", "First Name"]

    def on_save_data(self) -> None:
        '''
        Slot to handle data saving.
        '''
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    def on_fetch_data(self, model: "Class") -> None:
        '''
        Fetches data from the database and holds caches it.
        '''
        self._roster_data = class_service.get_students_in_class(model.id)

    def on_refresh_view(self) -> list["Student"]:
        '''
        Updates the model with fetched data.
        '''
        # Clear the model
        self._data_model.removeRows(0, self._data_model.rowCount())

        # Add the rows from the cache
        for student in self._roster_data:
            self._add_row_to_model([student.student_number, student.last_name, student.first_name])
