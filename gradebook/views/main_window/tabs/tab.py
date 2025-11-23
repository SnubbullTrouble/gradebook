from abc import abstractmethod
from PySide6 import QtWidgets, QtCore, QtGui
from gradebook.database.models import BaseModel

class Tab(QtWidgets.QWidget):
    '''
    A class representing a tab in the main window.
    '''

    fetch_data = QtCore.Signal(BaseModel)
    refresh_view = QtCore.Signal()
    save_data = QtCore.Signal()

    def __init__(self) -> None:
        '''
        Initialize the Tab with a reference to the main window.
        '''
        super().__init__()

        # Connect signals
        self.fetch_data.connect(self.on_fetch_data)
        self.refresh_view.connect(self.on_refresh_view)
        self.save_data.connect(self.on_save_data)

        # Connect Model
        self._data_model = QtGui.QStandardItemModel()

        # Create the view
        self._create_view()

    @property
    @abstractmethod
    def _headers(self) -> None:
        pass

    @abstractmethod
    def on_save_data(self) -> None:
        '''
        Slot to handle data saving.
        '''
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    @abstractmethod
    def on_fetch_data(self, model: BaseModel) -> None:
        '''
        Fetches data from the database and holds caches it.
        '''
        raise NotImplementedError("Subclasses must implement on_fetch_data method.")

    @abstractmethod
    def on_refresh_view(self) -> None:
        '''
        Updates the model with fetched data.
        '''
        raise NotImplementedError("Subclasses must implement on_refresh_view method.")
    
    @property
    def name(self) -> str:
        '''
        Abstract property to get the name of the tab.
        '''
        return type(self).__name__       

    def _create_view(self) -> None:
        '''
        Add a table view to the tab.
        '''
        # Set my name
        self.setObjectName(u"tab" + self.name)

        # Add a layout to my view
        self._gridLayout = QtWidgets.QGridLayout(self)
        self._gridLayout.setObjectName(u"gridLayout")

        # Model Headers
        self._data_model.setHorizontalHeaderLabels(self._headers)

        # Add a table view to my view
        self._tableView = QtWidgets.QTableView(self)
        self._tableView.setObjectName(u"tableWidget")
        self._tableView.setModel(self._data_model)

        # Add the table view to the layout
        self._gridLayout.addWidget(self._tableView, 0, 0, 1, 1)

    def _add_row_to_model(self, row_values: list[str]) -> None:
        '''
        Adds a new row to the model with the row values.
        
        Args:
            row_values (list[str]): the values to add to the model
        '''
        self._data_model.appendRow([QtGui.QStandardItem(str(v)) for v in row_values])