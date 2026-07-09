from gradebook.database.models import ensure_db_initialized
from gradebook.views.main_window.main_window import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    ensure_db_initialized(create_tables=True)
    app = QApplication([])
    window = MainWindow(app)
    window.show()
    app.exec()