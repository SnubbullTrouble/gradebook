import dataclasses
from PySide6 import QtWidgets, QtCore
from gradebook.views.assignment_window.ui_assignment_window import Ui_Dialog
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Assignment

@dataclasses.dataclass
class Row:
    description: str
    points: int

class ObservableList(list):
    callback: typing.Callable = None

    def __init__(self):
        super().__init__()

    def append(self, item: any) -> None:
        super().append(item)
        if self.callback:
            self.callback()

    def clear(self) -> None:
        super().clear()

class AssignmentWindow(QtWidgets.QDialog):

    _rows: ObservableList[Row] = ObservableList()

    def __init__(self, parent: QtWidgets.QMainWindow = None, selected_assignment: "Assignment" = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self._selected_assignment = selected_assignment
        
        # Disenable the save button initially
        self.ui.buttonBox.buttons()[0].setEnabled(False)

        # Signals
        self.ui.bAdd.clicked.connect(self._bAdd_clicked)
        self.ui.tableWidget.currentCellChanged.connect(self._set_bSave_enable)
        self.ui.buttonBox.buttons()[0].clicked.connect(self._read_table_widget_data)
        self.ui.tbName.textChanged.connect(self._read_table_widget_data)

        # Callback
        self._rows.callback = self._refresh_table_view

    @property
    def questions(self) -> list[Row]:
        '''The rows in the table.'''
        return self._rows
    
    @property
    def assignment_name(self) -> str:
        '''
        The name of the file.
        '''
        return self.ui.tbName.text().strip()
    
    @property
    def total_points(self) -> int:
        '''Total points of the assignment'''
        return sum([r.points for r in self.questions])

    def _load_Assignment(self) -> None:
        raise NotImplementedError("Assignment Loader not implemented")

    def _bAdd_clicked(self) -> None:
        '''
        Adds a new question when the Add button is clicked
        '''
        self._rows.append(Row("", ""))

    def _set_bSave_enable(self) -> None:
        '''
        Enables the Save button
        '''
        if len(self.ui.tbName.text().strip()) > 0 and self.ui.tableWidget.rowCount() > 0:
            self.ui.buttonBox.buttons()[0].setEnabled(True)

    def _refresh_table_view(self) -> None:
        '''
        Updates the table view with the current question list
        '''
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Description", "Points"])
        for row in self.questions:
            index = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(index)
            self.ui.tableWidget.setItem(index, 0, (QtWidgets.QTableWidgetItem(row.description)))
            self.ui.tableWidget.setItem(index, 0, (QtWidgets.QTableWidgetItem(row.points)))

    def _read_table_widget_data(self) -> None:
        '''
        Gets the typed data out of the table and puts it in the rows collection
        '''
        self._rows.clear()
        for index in range(self.ui.tableWidget.rowCount()):
            self._rows.append(Row(self.ui.tableWidget.item(index, 0).text(), int(self.ui.tableWidget.item(index, 1).text())))


