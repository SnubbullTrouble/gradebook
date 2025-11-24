# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table_view_windowPSxOYZ.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHeaderView, QSizePolicy, QTableView,
    QWidget)

class Ui_TableViewWindow(object):
    def setupUi(self, TableViewWindow):
        if not TableViewWindow.objectName():
            TableViewWindow.setObjectName(u"TableViewWindow")
        TableViewWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
        TableViewWindow.resize(702, 452)
        self.gridLayout = QGridLayout(TableViewWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(TableViewWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.tableView = QTableView(TableViewWindow)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)


        self.retranslateUi(TableViewWindow)
        self.buttonBox.accepted.connect(TableViewWindow.accept)
        self.buttonBox.rejected.connect(TableViewWindow.reject)

        QMetaObject.connectSlotsByName(TableViewWindow)
    # setupUi

    def retranslateUi(self, TableViewWindow):
        TableViewWindow.setWindowTitle(QCoreApplication.translate("TableViewWindow", u"Dialog", None))
    # retranslateUi

