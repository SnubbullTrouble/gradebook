from PySide6 import QtWidgets, QtGui, QtCore
from gradebook.views.table_view_window.table_view_window import TableViewWindow
from gradebook.database.services import scoring as scoring_service
from gradebook.database.services import classes as class_service
from gradebook.database.services import students as students_service
from gradebook.database.services import assignments as assignment_service
from gradebook.database.models import (
    Assignment,
    AssignmentQuestion,
    Class,
    StudentQuestionScore,
)


class AssignmentGraderWindow(TableViewWindow):

    _selected_assignment: Assignment = None

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Grade Assignment")

        # Connect the data changed signal to this function so that it updates when the user changes a value
        self._data_model.dataChanged.connect(
            self.sum_totals, QtCore.Qt.UniqueConnection
        )

        # Signal for saving data
        self.accept_signal.connect(self._update_student_scores_from_table_view)

    def _data_changed(self) -> bool:
        """
        Checks if the data in the model has been changed by comparing it to the original model.

        Returns:
            bool: True if the data has been changed, False otherwise.
        """
        for r in range(self._data_model.rowCount() - 1):
            for c in range(self._data_model.columnCount() - 1):
                if (
                    self._data_model.item(r, c).text()
                    != self._original_model.item(r, c).text()
                ):
                    return True
        return False

    def sum_totals(self) -> None:
        """
        Gets the points sum for each row and updates the table. Also sets up the dataChanged signal for the first time
        """
        if self._data_model_update_lock:
            return

        # Prevent an infinite loop
        self._data_model_update_lock = True

        for r in range(self._data_model.rowCount()):
            _sum = 0
            for c in range(3, self._data_model.columnCount() - 2):
                _sum += float(self._data_model.item(r, c).text())
            self._data_model.setItem(
                r,
                self._data_model.columnCount() - 1,
                QtGui.QStandardItem(str(f"{_sum:.2f}")),
            )

        # Unlock for the next time it changes
        self._data_model_update_lock = False

    def set_assignment_data(
        self, selected_assignment: Assignment, selected_class: Class
    ) -> None:
        """
        Sets the table data for the selected assignment

        Args:
            assignment (Assignment): the assignment to get the data for
        """
        self._selected_assignment = selected_assignment

        # Get the question list for the headers
        question_list: list[AssignmentQuestion] = (
            assignment_service.get_assignment_questions(selected_assignment.id)
        )

        # Get the roster
        student_list = class_service.get_students_in_class(selected_class.id)

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

        self.set_headers(
            ["Student ID", "Last Name", "First Name"]
            + [q.text for q in question_list]
            + ["Time", "Total"]
        )

        self.set_model_data(table)
        self.sum_totals()

    def _update_student_scores_from_table_view(
        self, model: QtGui.QStandardItemModel
    ) -> None:
        """
        Slot to handle updating student scores from the table view.

        Args:
            model (QtGui.QStandardItemModel): the model from the table view with updated scores
        """
        # Get the question list for the headers
        question_list: list[AssignmentQuestion] = (
            assignment_service.get_assignment_questions(self._selected_assignment.id)
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
                    student.id, self._selected_assignment.id, total_time
                )
