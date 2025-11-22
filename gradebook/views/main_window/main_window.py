from gradebook.views.main_window.context import Context
from gradebook.views.main_window.tabs.roster_tab import Roster
from gradebook.views.main_window.ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtWidgets, QtCore
from gradebook.views.class_window.class_window import ClassWindow
from gradebook.database.services import classes as class_service
from gradebook.views.main_window.tabs.tab import Tab
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Class, Student


class MainWindow(QMainWindow):

    # Signals
    _class_changed = QtCore.Signal()

    # UI data
    _unsaved_changes = []
    _tabs = [Roster]

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
            tab.refresh_view.emit()

    def _create_tab_views(self) -> None:
        '''
        Create and add all tab views to the main window's tab widget.
        '''
        for tab_class in self._tabs:
            tab_view = Roster()
            self.ui.tabWidget.addTab(tab_view, tab_view.name)

    # Data Management

    def _fetch_class_data(self) -> None:
        '''
        Load data for the selected class.
        '''
        try:
            self._current_class = class_service.get_class_by_id(self._selected_class.id)
        except Exception as e:
            self._set_status(f"Error - Failed to load class data: {e}")


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
        

        # Signals
        self._class_changed.connect(self._refresh_tables)
        self._fetch_class.connect(self._fetch_class_data)
        self._fetch_roster.connect(self._fetch_roster_data)

    def _add_tab_view(self) -> None:
        '''
        Add tab views to the main window's tab widget.
        '''
        # Example of adding a tab
        example_tab = Tab(self.ui.tabWidget, "ExampleTab")


