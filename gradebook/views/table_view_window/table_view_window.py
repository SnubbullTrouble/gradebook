from PySide6 import QtWidgets, QtGui, QtCore
from gradebook.views.table_view_window.ui_table_view_window import Ui_TableViewWindow


class TableViewWindow(QtWidgets.QDialog):
    """
    Dialog for verifying data before importing.
    """

    _data_model_update_lock = False
    _data_model = QtGui.QStandardItemModel()

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_TableViewWindow()
        self.ui.setupUi(self)
        self.setModal(True)

        # Setup Model
        self.ui.tableView.setModel(self._data_model)

    @property
    def data_model(self) -> QtGui.QStandardItemModel:
        return self._data_model

    def set_headers(self, headers: list[str]) -> None:
        """
        Sets the headers for the model

        Args:
            list(str): headers to use in the model
        """
        self._data_model.setHorizontalHeaderLabels(headers)

    def set_model_data(self, data: list[list[any]]) -> None:
        """
        Sets sets the data of the view model using raw data.

        Args:
            data (list[list[any]]): The raw data to add to the model
        """
        self._data_model.removeRows(0, self._data_model.rowCount())

        for r in data:
            new_row = [QtGui.QStandardItem(str(c)) for c in r]
            self._data_model.appendRow(new_row)

    def sum_totals(self) -> None:
        """
        Gets the points sum for each row and updates the table. Also sets up the dataChanged signal for the first time
        """
        if self._data_model_update_lock:
            return

        # Connect the data changed signal to this function so that it updates when the user changes a value
        self._data_model.dataChanged.connect(
            self.sum_totals, QtCore.Qt.UniqueConnection
        )

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
