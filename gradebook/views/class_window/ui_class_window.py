# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'class_windowwkUZut.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ClassDialog(object):
    def setupUi(self, ClassDialog):
        if not ClassDialog.objectName():
            ClassDialog.setObjectName(u"ClassDialog")
        ClassDialog.resize(711, 555)
        self.gridLayout = QGridLayout(ClassDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lwClassList = QListWidget(ClassDialog)
        self.lwClassList.setObjectName(u"lwClassList")

        self.gridLayout.addWidget(self.lwClassList, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bNew = QPushButton(ClassDialog)
        self.bNew.setObjectName(u"bNew")

        self.verticalLayout.addWidget(self.bNew)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.bOpen = QPushButton(ClassDialog)
        self.bOpen.setObjectName(u"bOpen")

        self.verticalLayout.addWidget(self.bOpen)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)


        self.retranslateUi(ClassDialog)

        QMetaObject.connectSlotsByName(ClassDialog)
    # setupUi

    def retranslateUi(self, ClassDialog):
        ClassDialog.setWindowTitle(QCoreApplication.translate("ClassDialog", u"Classes", None))
        self.bNew.setText(QCoreApplication.translate("ClassDialog", u"New", None))
        self.bOpen.setText(QCoreApplication.translate("ClassDialog", u"Load", None))
    # retranslateUi

