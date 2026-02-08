from abc import abstractmethod
from PySide6 import QtWidgets, QtCore, QtGui
from gradebook.database.models import BaseModel, Class


class Tab(QtWidgets.QWidget):
    """
    A class representing a tab in the main window.
    """

    fetch_data = QtCore.Signal(BaseModel)
    refresh_view = QtCore.Signal()

    def __init__(self) -> None:
        """
        Initialize the Tab with a reference to the main window.
        """
        super().__init__()

        # Connect signals
        self.fetch_data.connect(self.on_fetch_data)
        self.refresh_view.connect(self.on_refresh_view)

        # Create the view
        self._create_view()

    @abstractmethod
    def on_fetch_data(self, selected_class: "Class") -> None:
        """
        Fetches data from the database and holds caches it.
        """
        raise NotImplementedError("Subclasses must implement on_fetch_data method.")

    @abstractmethod
    def on_refresh_view(self) -> None:
        """
        Updates the model with fetched data.
        """
        raise NotImplementedError("Subclasses must implement on_refresh_view method.")

    @property
    def name(self) -> str:
        """
        Abstract property to get the name of the tab.
        """
        return type(self).__name__

    @abstractmethod
    def _create_view(self) -> None:
        """
        Add a view to the tab.
        """
        pass
