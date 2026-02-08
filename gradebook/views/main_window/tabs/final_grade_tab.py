from abc import abstractmethod
from typing import TypedDict
from wsgiref import headers
from PySide6 import QtWidgets, QtGui
from gradebook.database.models import Class, Student
from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import classes as class_service
from gradebook.database.services import assignments as assignment_service


class GradeBook(TypedDict):
    attendance: float
    homework: float
    quiz: float
    test: float
    project: float
    final: float


class Grade(Tab):
    """
    A class representing a tab in the main window.
    """

    _class_roster: list[Student] = []
    _grades: list[GradeBook] = []
    _weights: dict[str, float] = {}
    _data_model = QtGui.QStandardItemModel()

    def __init__(self) -> None:
        """
        Initialize the Tab with a reference to the main window.
        """
        super().__init__()

    @property
    def headers(self) -> list[str]:
        """Headers for the View"""
        headers = []
        for h in GradeBook.__annotations__.keys():
            headers.append(h.capitalize())
            headers.append(h.capitalize() + " (Weighted)")
        return ["Student Number", "Last Name", "First Name"] + headers

    @abstractmethod
    def on_fetch_data(self, selected_class: "Class") -> None:
        """
        Fetches data from the database and holds caches it.
        """
        # Get the roster for the class
        self._class_roster = class_service.get_students_in_class(selected_class.id)

        # Get a table of all the score sums for each assignment category in Gradebook for each student in the class
        self._grades = [
            self._get_student_scores(student.id, selected_class.id)
            for student in self._class_roster
        ]

        # Get a dictionary of the category weights for the class
        self._weights = {}
        for category in GradeBook.__annotations__.keys():
            self._weights[category] = assignment_service.get_assignment_weight(
                selected_class.id, category
            )

    def _build_data_table(self) -> list[list]:
        """
        Build a data table for the view.

        Args:
            student_data: A list of tuples containing student information and their scores.
            weights: A dictionary of category weights for the class.

        Returns:
        """
        table = []
        for student, grade_book in zip(self._class_roster, self._grades):
            row = [
                student.student_number,
                student.last_name,
                student.first_name,
            ] + list(
                zip(
                    grade_book.values(),
                    [
                        grade_book[category] * self._weights[category]
                        for category in GradeBook.__annotations__.keys()
                    ],
                )
            )
            table.append(row)
        return table

    def _set_data_model(self, data_table: list[list]) -> None:
        """
        Set the data model for the view.

        Args:
            data_table: A list of lists containing the data to be displayed in the view.
        """
        self._data_model.setRowCount(0)
        for row in data_table:
            model_row = []
            for value in row:
                if isinstance(value, tuple):
                    for v in value:
                        item = QtGui.QStandardItem(f"{v:.2f}")
                        item.setEditable(False)
                        model_row.append(item)
                else:
                    item = QtGui.QStandardItem(str(value))
                    item.setEditable(False)
                    model_row.append(item)
            self._data_model.appendRow(model_row)

    def _get_student_scores(self, student_id: int, class_id: int) -> GradeBook:
        """
        Get the total scores for each category for a student in a class.

        Args:
            student_id: The ID of the student.
            class_id: The ID of the class.

        Returns:
            Gradebook: A dictionary containing the total scores for each category.
        """
        # Get all the assignment scores for the student in the class
        assignment_scores = [
            assignment_service.get_student_category_score(
                student_id, class_id, category
            )
            for category in GradeBook.__annotations__.keys()
        ]
        return GradeBook(
            **dict(zip(GradeBook.__annotations__.keys(), assignment_scores))
        )

    @abstractmethod
    def on_refresh_view(self) -> None:
        """
        Updates the model with fetched data.
        """
        # Build a data table for the view
        data_table = self._build_data_table()

        # Set the data model for the view
        self._set_data_model(data_table)

    @abstractmethod
    def _create_view(self) -> None:
        """
        Add a table view to the tab.
        """
        # Set my name
        self.setObjectName("tab" + self.name)

        # Add a layout to my view
        self._gridLayout = QtWidgets.QGridLayout(self)
        self._gridLayout.setObjectName("gridLayout")

        # Create a table view
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setObjectName("tableView")

        # Add the table view to the layout
        self._gridLayout.addWidget(self.tableView, 0, 0, 1, 1)

        # Setup Model
        self.tableView.setModel(self._data_model)

        # Set up the headers
        self._data_model.setHorizontalHeaderLabels(self.headers)
