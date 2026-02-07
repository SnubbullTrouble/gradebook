from gradebook.database.models import Assignment, AssignmentQuestion
from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import assignments as assignment_service
from gradebook.database.services import scoring as scoring_service
from gradebook.database.services import classes as class_service
from gradebook.database.services import students as students_service
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
            window = self._get_selected_assignment_table_view()
            window.exec()

    def _get_selected_assignment_table_view(self) -> TableViewWindow:
        """
        Gets the table data for the selected assignment

        Returns:
            TableViewWindow: the table view window for the selected assignment
        """
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
            # Get the time taken from the database
            total_time = scoring_service.get_student_assignment_time(
                student.id, selected_assignment.id
            )
            if score_records == []:
                table.append(
                    row_data + [0 for _ in range(len(question_list))] + [total_time]
                )
            else:
                table.append(
                    row_data + [s.points_scored for s in score_records] + [total_time]
                )  # TODO: figure out what structure gets returned

        window = TableViewWindow(self)
        window.set_headers(
            ["Student ID", "Last Name", "First Name"]
            + [q.text for q in question_list]
            + ["Time", "Total"]
        )
        window.accept_signal.connect(self._update_student_scores_from_table_view)
        window.set_model_data(table)
        window.sum_totals()

        return window

    def _update_student_scores_from_table_view(
        self, model: QtGui.QStandardItemModel
    ) -> None:
        """
        Slot to handle updating student scores from the table view.

        Args:
            model (QtGui.QStandardItemModel): the model from the table view with updated scores
        """
        # Get the selected assignment
        selected_assignment: Assignment = self._get_assignment_from_name(
            self._selected_view_item
        )

        # Get the question list for the headers
        question_list: list[AssignmentQuestion] = (
            assignment_service.get_assignment_questions(selected_assignment.id)
        )

        # Loop though all the students in the model and update their assignment scores, question scores, and total time if applicable
        for r in range(model.rowCount()):
            student_number = model.item(r, 0).text()
            student = students_service.get_student_by_number(student_number)

            # Update question scores
            for c in range(3, 3 + len(question_list)):
                question_score = float(model.item(r, c).text())
                question = question_list[c - 3]
                scoring_service.update_student_question_score(
                    student.id, question.id, question_score
                )

            # Update total time if applicable
            if model.item(r, 3 + len(question_list)).text() != "":
                total_time = int(model.item(r, 3 + len(question_list)).text())
                scoring_service.update_student_assignment_time(
                    student.id, selected_assignment.id, total_time
                )

    def _add_row_to_data_model(self, text: str) -> None:
        """
        Add a value to the model
        """
        self._data_model.appendRow(QtGui.QStandardItem(text))

    def _listview_clicked(self, item: QtCore.QModelIndex) -> None:
        """Sets the current selected item when the view is clicked"""
        self._selected_view_item = item.data()
