from gradebook.views.assignment_window.assignment_window import AssignmentWindow
from gradebook.views.main_window.errors import InvalidTabError
from gradebook.views.main_window.tabs.homework_tab import Homework
from gradebook.views.main_window.tabs.roster_tab import Roster
from gradebook.views.main_window.ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtWidgets, QtCore
from gradebook.views.class_window.class_window import ClassWindow
from gradebook.database.services import classes as class_service
from gradebook.database.services import students as student_service
from gradebook.database.services import assignments as assignment_service
from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.models import Student
from gradebook.views.dialogs.new_student import NewStudentDialog
from gradebook.views.dialogs.data_verification import DataVerificationDialog
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Class


class MainWindow(QMainWindow):
    # Settings
    _show_verification_dialog = True

    # Signals
    _class_changed = QtCore.Signal()

    # UI data
    _unsaved_changes = []
    _tabs = [Roster, Homework]

    # Database data
    _selected_roster = None
    _selected_class = None

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._connect_handlers()

        # UI
        self._set_status("Ready")
        self.ui.lClassName.setText("No class selected")
        self.ui.tabWidget.clear()

        self._create_tab_views()

    @property
    def _current_class(self) -> "Class":
        '''
        Property to get all class data.
        '''
        return self._selected_class
    
    @_current_class.setter
    def _current_class(self, value: "Class") -> None:
        '''
        Property setter to set all class data.
        '''
        self._selected_class = value    
        self._refresh_tables()
        self.ui.lClassName.setText(value.name)

    @property
    def _roster(self) -> list["Student"]:
        '''
        Property to get the class roster.
        '''
        return self._selected_roster

    # View Management

    def _refresh_tables(self) -> None:
        '''
        Refresh all data tables in the main window.
        '''
        for index in range(self.ui.tabWidget.count()):
            tab: Tab = self.ui.tabWidget.widget(index)
            tab.fetch_data.emit(self._current_class)
            tab.refresh_view.emit()

    def _create_tab_views(self) -> None:
        '''
        Create and add all tab views to the main window's tab widget.
        '''
        for tab_class in self._tabs:
            tab_view = tab_class()
            self.ui.tabWidget.addTab(tab_view, tab_view.name)

    # Data Management

    def _add_student_clicked(self) -> None:
        '''
        Handler for adding a new student to the current class.
        '''
        if self._current_class is not None:
            dialog = NewStudentDialog(self)
            dialog.exec()

            if dialog.result() == QtWidgets.QDialog.Accepted:
                data = dialog.rows
                table = [line.replace(" ", "").split(",") for line in data if line.strip()]

                # Confirm
                if self._show_verification_dialog:
                    roster_tab: Roster = self.ui.tabWidget.currentWidget()
                    verification_dialog = DataVerificationDialog(table, roster_tab.headers, self)
                    verification_dialog.exec()

                    if verification_dialog.result() != QtWidgets.QDialog.Accepted:
                        self._set_status("Student addition cancelled.")
                        return
                    
                # Add students
                for row in table:
                    try:
                        new_student_record = student_service.create_student(student_number=row[0], last_name=row[1], first_name=row[2])
                        roster = class_service.enroll_student(self._current_class, new_student_record)
                        status = "added" if new_student_record == roster.student else "not added"
                        self._set_status(f"{roster.student.last_name}, {roster.student.first_name} {status} to class {self._current_class.name}.")
                    except Exception as e:
                        if "UNIQUE" in str(e):
                            field = str(e).split(".")[1]
                            self._set_status(f"Field {field} must be unique. Student {row[1]}, {row[2]} not added.")
                        else:
                            QtWidgets.QMessageBox.warning(self, "Error Adding Student", f"An error occurred while adding student: {str(e)}")

                # Refresh view
                self._refresh_tables()

            else:
                self._set_status("Student addition cancelled.")
        else:
            self._set_status("No class selected. Cannot add student.")

    def _add_assignment_clicked(self) -> None:
        '''
        Opens the assignment window for adding an assignment
        '''
        if self._selected_class is not None:
            dialog = AssignmentWindow()
            dialog.exec()

            if dialog.result() == QtWidgets.QDialog.Accepted:
                # Get the assignment data
                questions = [assignment_service.Question(q, p) for (q, p) in dialog.questions]

                # Create a new record with the assignment data
                new_assignment_record = assignment_service.create_assignment(dialog.assignment_name, dialog.total_points, questions)

                # Link the assignment to the existing class
                assignment_service.assign_to_class(self._selected_class, new_assignment_record)

                self._refresh_tables()
            else:
                self._set_status("Cancelling assignment addition.")
        else:
            self._set_status("Cannot add assignment to class. No class selected.")

    # UI Management


    def _open_classes_window(self) -> None:
        '''
        Open the Classes window to select a class.
        '''
        dialog = ClassWindow(self)
        dialog.exec()

        if dialog.result() == QtWidgets.QDialog.Accepted:
            self._current_class = dialog.selected_class

    def _set_status(self, message: str) -> None:
        '''
        Set the status bar message.
        '''
        self.ui.lStatus.setText(f"Status: {message}")

    def _connect_handlers(self) -> None:
        '''
        Connect menu actions to their handlers.
        '''
        # Actions
        self.ui.actionClasses.triggered.connect(self._open_classes_window)

        # Handlers
        self.ui.bAdd.clicked.connect(self._bAdd_clicked)

        # Signals
        self._class_changed.connect(self._refresh_tables)

    def _bAdd_clicked(self) -> None:
        '''
        Handler for the Add button click event.
        '''
        match self.ui.tabWidget.currentWidget().name:
            case Roster.__name__:
                self._add_student_clicked()
            case Homework.__name__:
                self._add_assignment_clicked()
            case _:
                raise InvalidTabError(self.ui.tabWidget.currentWidget().name)
            


