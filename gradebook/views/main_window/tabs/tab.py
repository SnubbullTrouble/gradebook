from abc import abstractmethod
from PySide6 import QtWidgets, QtCore
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
        # Create the view
        self._create_view()

        # Connect signals
        self.fetch_data.connect(self.on_fetch_data)
        self.refresh_view.connect(self.on_refresh_view)
        self.save_data.connect(self.on_save_data)

    @abstractmethod
    def on_save_data(self) -> None:
        '''
        Slot to handle data saving.
        '''
        raise NotImplementedError("Subclasses must implement on_save_data method.")

    @abstractmethod
    def on_fetch_data(self, model: BaseModel) -> None:
        '''
        Slot to handle data fetching.
        '''
        raise NotImplementedError("Subclasses must implement on_fetch_data method.")

    @abstractmethod
    def on_refresh_view(self) -> None:
        '''
        Slot to handle view refreshing.
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
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")

        # Add a table widget to my view
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName(u"tableWidget")

        # Add the table widget to the layout
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)