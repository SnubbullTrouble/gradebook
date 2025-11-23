from PySide6 import QtWidgets
from gradebook.views.dialogs.ui_data_verification import Ui_DataVerificationDialog

class DataVerificationDialog(QtWidgets.QDialog):
    '''
    Dialog for verifying data before importing.
    '''

    def __init__(self, data_table: list[list[str]], table_headers: list[str] = None, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_DataVerificationDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self._data_table = data_table
        self._table_headers = table_headers

        self._fill_table()

    def _fill_table(self) -> None:
        '''
        Fill the table widget with data from the data table.
        '''
        self.ui.tableWidget.setRowCount(len(self._data_table))
        self.ui.tableWidget.setColumnCount(len(self._data_table[0]) if self._data_table else 0)

        if self._table_headers:
            self.ui.tableWidget.setHorizontalHeaderLabels(self._table_headers)

        for row_idx, row in enumerate(self._data_table):
            for col_idx, cell in enumerate(row):
                item = QtWidgets.QTableWidgetItem(cell)
                self.ui.tableWidget.setItem(row_idx, col_idx, item)