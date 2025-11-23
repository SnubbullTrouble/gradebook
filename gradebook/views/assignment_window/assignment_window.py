import dataclasses
from PySide6 import QtWidgets, QtGui
from gradebook.views.assignment_window.ui_assignment_window import Ui_Dialog
import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import Assignment

class AssignmentWindow(QtWidgets.QDialog):

    _data_model = QtGui.QStandardItemModel()

    def __init__(self, parent: QtWidgets.QMainWindow = None, selected_assignment: "Assignment" = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self._selected_assignment = selected_assignment
        
        # Disenable the save button initially
        self.ui.buttonBox.buttons()[0].setEnabled(False)

        # Signals
        self.ui.bAdd.clicked.connect(self._add_row_to_model)
        self._data_model.dataChanged.connect(self._set_bSave_enable)
        self.ui.tbName.textChanged.connect(self._set_bSave_enable)

        # Connect Model
        self._connect_model()

    @property
    def questions(self) -> list[tuple[str, int]]:
        '''The rows in the table.'''
        return self._get_rows_as_tuples()
    
    @property
    def assignment_name(self) -> str:
        '''
        The name of the file.
        '''
        return self.ui.tbName.text().strip()
    
    @property
    def total_points(self) -> int:
        '''Total points of the assignment'''
        return self._get_total_points_value()
    
    def _connect_model(self) -> None:
        '''Connect the model to the table and set the headers'''
        self._data_model.setHorizontalHeaderLabels(["Description", "Points"])
        self.ui.tableView.setModel(self._data_model)
        
    def _load_Assignment(self) -> None:
        raise NotImplementedError("Assignment Loader not implemented")

    def _set_bSave_enable(self) -> None:
        '''
        Enables the Save button
        '''
        if len(self.ui.tbName.text().strip()) > 0 and self._data_model.rowCount() > 0:
            self.ui.buttonBox.buttons()[0].setEnabled(True)

    def _add_row_to_model(self, description: str = "", points: str = "") -> None:
        '''
        Adds the data to the model as a new row.

        Args:
            description (str): question description
            points (int): point value of the question
        '''
        self._data_model.appendRow([QtGui.QStandardItem(description), QtGui.QStandardItem(points)])

    def _get_rows_as_tuples(self) -> list[tuple[str, int]]:
        '''
        Gets the table data in a parsable format
        
        Returns:
            list[tuple[str, int]]: the description and points values for each question
        '''
        model = self._data_model
        rows = model.rowCount()
        cols = model.columnCount()

        result = []

        for r in range(rows):
            # build a tuple of column values for this row
            row_tuple = tuple(
                model.item(r, c).text() if model.item(r, c) else None
                for c in range(cols)
            )
            result.append(row_tuple)

        return result
    
    def _get_total_points_value(self) -> None:
        '''
        Gets the total value of the assignment.

        Returns:
            int: the total points value
        '''
        total = 0

        for row in range(self._data_model.rowCount()):
            item = self._data_model.item(row, 1)
            if item:
                try:
                    value = int(item.text())  # convert text to number
                    total += value
                except ValueError:
                    pass  # ignore non-numeric cells

        return total