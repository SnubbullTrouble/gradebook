# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_verificationnEiyBf.ui'
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
    QGridLayout, QHeaderView, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_DataVerificationDialog(object):
    def setupUi(self, DataVerificationDialog):
        if not DataVerificationDialog.objectName():
            DataVerificationDialog.setObjectName(u"DataVerificationDialog")
        DataVerificationDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        DataVerificationDialog.resize(400, 300)
        self.gridLayout = QGridLayout(DataVerificationDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableWidget = QTableWidget(DataVerificationDialog)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DataVerificationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(DataVerificationDialog)
        self.buttonBox.accepted.connect(DataVerificationDialog.accept)
        self.buttonBox.rejected.connect(DataVerificationDialog.reject)

        QMetaObject.connectSlotsByName(DataVerificationDialog)
    # setupUi

    def retranslateUi(self, DataVerificationDialog):
        DataVerificationDialog.setWindowTitle(QCoreApplication.translate("DataVerificationDialog", u"Dialog", None))
    # retranslateUi

