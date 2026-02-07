from gradebook.database.models import Assignment
from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import assignments as assignment_service
from PySide6 import QtWidgets, QtCore, QtGui
from gradebook.views.table_view_window.assignment_grader_window import (
    AssignmentGraderWindow,
)
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Class


class AssignmentTab(Tab):

    _selected_class: "Class" = None

    def __init__(self):

        # Variables
        self._data_model = QtCore.QStringListModel()
        self._assignment_list: list[Assignment] = []
        self._selected_view_item = (
            None  # Assignment title of the selected item in the current tab list view
        )

        super().__init__()

        # Signals
        self._bGrade.clicked.connect(self._bGrade_clicked)
        self._listView.clicked.connect(self._listview_clicked)

        # Selection mode
        self._listView.setSelectionMode(QtWidgets.QListView.SingleSelection)

    @property
    def assignment_names(self) -> list[str]:
        """
        Property to get assignment names from data model
        """
        return [
            self._data_model.index(i).data() for i in range(self._data_model.rowCount())
        ]

    def on_save_data(self) -> None:
        """
        Slot to handle data saving.
        """
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    def on_fetch_data(self, model: "Class") -> None:
        """
        Fetches the data and caches it for later.

        Args:
            model (Class): the class to get assignments of
        """
        self._selected_class = model
        # Get all the assignments for the class
        self._assignment_list = assignment_service.get_assignments_for_class(
            model.id, self.name.lower()
        )

    def on_refresh_view(self) -> None:
        """
        Loads the view model with the cached data.
        """
        self._data_model.setStringList([a.title for a in self._assignment_list])

    def _create_view(self) -> None:
        """
        Add a table view to the tab.
        """
        # Set my name
        self.setObjectName("tab" + self.name)

        # Add a layout to my view
        self._gridLayout = QtWidgets.QGridLayout(self)
        self._gridLayout.setObjectName("gridLayout")

        # List Box
        self._listView = QtWidgets.QListView()
        self._listView.setModel(self._data_model)

        # Add the table view to the layout
        self._gridLayout.addWidget(self._listView, 0, 0, 1, 1)

        # Add A Button Layout
        self._horizontal_layout = QtWidgets.QHBoxLayout()
        self._spacer_widget = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self._horizontal_layout.addItem(self._spacer_widget)

        # Add the button
        self._bGrade = QtWidgets.QPushButton("Grade")
        self._bGrade.setObjectName("bGrade")
        self._horizontal_layout.addWidget(self._bGrade)

        # Add the layout
        self._gridLayout.addLayout(self._horizontal_layout, 1, 0, 1, 1)

    def _get_assignment_from_name(self, name: str) -> Assignment:
        """
        Gets the assignment ide from the name.

        Args:
            name (str): the assignment name to search for

        Returns:
            Assignment: the assignment object
        """
        assignments: list[Assignment] = []
        for assignment in self._assignment_list:
            if assignment.title == self._selected_view_item:
                assignments.append(assignment)

        if len(assignments) != 1:
            raise ValueError(f"{len(assignments)} found with Name: {name}")

        return assignments[0]

    def _bGrade_clicked(self) -> None:
        """
        Event handler for the Grade button opens the grading window
        """
        if self._selected_view_item:
            # Selected Assignment
            selected_assignment: Assignment = self._get_assignment_from_name(
                self._selected_view_item
            )

            window = AssignmentGraderWindow(self)
            window.set_assignment_data(selected_assignment, self._selected_class)
            window.exec()

    def _add_row_to_data_model(self, text: str) -> None:
        """
        Add a value to the model
        """
        self._data_model.appendRow(QtGui.QStandardItem(text))

    def _listview_clicked(self, item: QtCore.QModelIndex) -> None:
        """Sets the current selected item when the view is clicked"""
        self._selected_view_item = item.data()


class Homework(AssignmentTab):
    name = "Homework"

    def __init__(self):
        super().__init__()


class Test(AssignmentTab):
    name = "Test"

    def __init__(self):
        super().__init__()
