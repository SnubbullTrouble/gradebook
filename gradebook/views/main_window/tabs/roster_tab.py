from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import classes as class_service
from PySide6 import QtWidgets
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Student, Class

class Roster(Tab):

    def __init__(self) -> None:
        '''
        Initialize the Tab with a reference to the main window.
        '''
        super().__init__()

    def on_save_data(self) -> None:
        '''
        Slot to handle data saving.
        '''
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    def on_fetch_data(self) -> None:
        '''
        Slot to handle data fetching.
        '''
        raise NotImplementedError("Subclasses must implement on_fetch_data method.")

    def on_refresh_view(self, model: "Class") -> list["Student"]:
        '''
        Slot to handle view refreshing.
        '''
        self._selected_roster = class_service.get_students_in_class(model.id)