from PySide6 import QtWidgets, QtGui, QtCore
from gradebook.views.table_view_window.ui_table_view_window import Ui_TableViewWindow


class TableViewWindow(QtWidgets.QDialog):
    """
    Dialog for verifying data before importing.
    """

    _data_model_update_lock = False
    _data_model = QtGui.QStandardItemModel()
    _accept_signal = QtCore.Signal(QtGui.QStandardItemModel)
    _original_model = QtGui.QStandardItemModel()
    _has_total = False

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_TableViewWindow()
        self.ui.setupUi(self)
        self.setModal(True)

        # Setup Model
        self.ui.tableView.setModel(self._data_model)

    @property
    def accept_signal(self) -> QtCore.Signal:
        """
        Signal emitted when the user clicks the "OK" button. Use to trigger database updates.

        Returns:
            QtCore.Signal: the accept signal
        """
        return self._accept_signal

    @property
    def data_model(self) -> QtGui.QStandardItemModel:
        """Property to access the data model for this dialog."""
        return self._data_model

    def accept(self) -> None:
        """
        Override the accept method to prevent closing the dialog when the user clicks "OK". Use to trigger database updates.
        """
        if self._data_changed():
            self._accept_signal.emit(self._data_model)
        super().accept()

    def _data_changed(self) -> bool:
        """
        Checks if the data in the model has been changed by comparing it to the original model.

        Returns:
            bool: True if the data has been changed, False otherwise.
        """
        row_bounds = self._data_model.rowCount() - (
            1 if self._has_total else 0
        )  # If we have totals, ignore the last two columns
        column_bounds = self._data_model.columnCount() - (1 if self._has_total else 0)
        for r in range(row_bounds):
            for c in range(column_bounds):
                if (
                    self._data_model.item(r, c).text()
                    != self._original_model.item(r, c).text()
                ):
                    return True
        return False

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

            copy_row = [QtGui.QStandardItem(str(c)) for c in r]
            self._original_model.appendRow(copy_row)

    def sum_totals(self) -> None:
        """
        Gets the points sum for each row and updates the table. Also sets up the dataChanged signal for the first time
        """
        if self._data_model_update_lock:
            return

        # Track if we need to ignore the last two columns when summing (if they are Time and Total)
        self._has_total = True

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
