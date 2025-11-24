from gradebook.database.models import Assignment
from gradebook.views.main_window.tabs.tab import Tab
from gradebook.database.services import assignments as assignment_service
from PySide6 import QtWidgets, QtCore, QtGui
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Class


class Homework(Tab):

    _data_model = QtCore.QStringListModel()
    _assignment_list: list[Assignment] = []

    def __init__(self):
        super().__init__()

        # Signals
        self._bGrade.clicked.connect(self._bGrade_clicked)

    def on_save_data(self) -> None:
        '''
        Slot to handle data saving.
        '''
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    def on_fetch_data(self, model: "Class") -> None:
        '''
        Fetches the data and caches it for later.

        Args:
            model (Class): the class to get assignments of
        '''
        # Get all the homeworks for the class
        self._assignment_list = assignment_service.get_assignments_for_class(model.id, self.name)

    def on_refresh_view(self) -> None:
        '''
        Loads the view model with the cached data.
        '''
        self._data_model.setStringList([a.title for a in self._assignment_list])

    def _create_view(self) -> None:
        '''
        Add a table view to the tab.
        '''
        # Set my name
        self.setObjectName(u"tab" + self.name)

        # Add a layout to my view
        self._gridLayout = QtWidgets.QGridLayout(self)
        self._gridLayout.setObjectName(u"gridLayout")

        # List Box
        self._listView = QtWidgets.QListView()
        self._listView.setModel(self._data_model)

        # Add the table view to the layout
        self._gridLayout.addWidget(self._listView, 0, 0, 1, 1)

        # Add A Button Layout
        self._horizontal_layout = QtWidgets.QHBoxLayout()
        self._spacer_widget = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self._horizontal_layout.addItem(self._spacer_widget)

        # Add the button
        self._bGrade = QtWidgets.QPushButton("Grade")
        self._bGrade.setObjectName(f"bGrade")
        self._horizontal_layout.addWidget(self._bGrade)
    
        # Add the layout
        self._gridLayout.addLayout(self._horizontal_layout, 1, 0, 1, 1)

    def _bGrade_clicked(self) -> None:
        '''
        Event handler for the Grade button opens the grading window
        '''
        pass

    def _add_row_to_data_model(self, text: str) -> None:
        '''
        Add a value to the model
        '''
        self._data_model.appendRow(QtGui.QStandardItem(text))

        