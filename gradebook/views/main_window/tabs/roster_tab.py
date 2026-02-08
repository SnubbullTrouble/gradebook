from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import classes as class_service
from PySide6 import QtWidgets, QtGui
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Student, Class


class Roster(Tab):

    _data_model = QtGui.QStandardItemModel()
    _roster_data: list["Student"] = []

    def __init__(self) -> None:
        """
        Initialize the Tab with a reference to the main window.
        """
        super().__init__()

    @property
    def roster(self) -> list["Student"]:
        """
        Property to get the roster data.
        """
        return self._roster_data

    @property
    def headers(self) -> list[str]:
        """Headers for the View"""
        return ["Student Number", "Last Name", "First Name"]

    def on_fetch_data(self, selected_class: "Class") -> None:
        """
        Fetches data from the database and holds caches it.
        """
        self._roster_data = class_service.get_students_in_class(selected_class.id)

    def on_refresh_view(self) -> list["Student"]:
        """
        Updates the model with fetched data.
        """
        # Clear the model
        self._data_model.removeRows(0, self._data_model.rowCount())

        # Add the rows from the cache
        for student in self._roster_data:
            self._add_row_to_model(
                [student.student_number, student.last_name, student.first_name]
            )

    def _create_view(self) -> None:
        """
        Add a table view to the tab.
        """
        # Set my name
        self.setObjectName("tab" + self.name)

        # Add a layout to my view
        self._gridLayout = QtWidgets.QGridLayout(self)
        self._gridLayout.setObjectName("gridLayout")

        # Model Headers
        self._data_model.setHorizontalHeaderLabels(self.headers)

        # Add a table view to my view
        self._tableView = QtWidgets.QTableView(self)
        self._tableView.setObjectName("tableWidget")
        self._tableView.setModel(self._data_model)

        # Add the table view to the layout
        self._gridLayout.addWidget(self._tableView, 0, 0, 1, 1)

    def _add_row_to_model(self, row_values: list[str]) -> None:
        """
        Adds a new row to the model with the row values.

        Args:
            row_values (list[str]): the values to add to the model
        """
        self._data_model.appendRow([QtGui.QStandardItem(str(v)) for v in row_values])
