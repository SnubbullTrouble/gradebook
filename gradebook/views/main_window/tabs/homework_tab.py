from gradebook.database.models import Assignment, AssignmentQuestion
from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import assignments as assignment_service
from gradebook.database.services import scoring as scoring_service
from gradebook.database.services import classes as class_service
from PySide6 import QtWidgets, QtCore, QtGui
from gradebook.views.table_view_window.table_view_window import TableViewWindow
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Class, StudentQuestionScore


class Homework(Tab):

    _data_model = QtCore.QStringListModel()
    _assignment_list: list[Assignment] = []
    _selected_class: "Class" = None
    _selected_view_item = None

    def __init__(self):
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
        # Get all the homeworks for the class
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

    def _get_assignment_from_name(self, name: str) -> int:
        """
        Gets the assignment ide from the name.

        Args:
            name (str): the assignment name to search for

        Returns:
            int: the id of the assignment
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

            # Get the question list for the headers
            question_list: list[AssignmentQuestion] = (
                assignment_service.get_assignment_questions(selected_assignment.id)
            )

            # Get the roster
            student_list = class_service.get_students_in_class(self._selected_class.id)

            # Get or Create the rows for each student
            table = []
            for student in student_list:
                # Get the student score for each question
                score_records: list["StudentQuestionScore"] = (
                    scoring_service.get_student_scores_for_assignment(
                        selected_assignment.id, student.id
                    )
                )
                row_data = [
                    student.student_number,
                    student.last_name,
                    student.first_name,
                ]
                if score_records == []:
                    table.append(
                        row_data + [0 for i in range(len(question_list))] + ["", ""]
                    )
                else:
                    table.append(
                        row_data + [s.points_scored for s in score_records] + ["", ""]
                    )  # TODO: figure out what structure gets returned

            window = TableViewWindow(self)
            window.set_headers(
                ["Student ID", "Last Name", "First Name"]
                + [q.text for q in question_list]
                + ["Time", "Total"]
            )

            window.set_model_data(table)
            window.sum_totals()
            window.exec()

    def _add_row_to_data_model(self, text: str) -> None:
        """
        Add a value to the model
        """
        self._data_model.appendRow(QtGui.QStandardItem(text))

    def _listview_clicked(self, item: QtCore.QModelIndex) -> None:
        """Sets the current selected item when the view is clicked"""
        self._selected_view_item = item.data()
