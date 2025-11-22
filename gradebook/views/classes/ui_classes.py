# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'classeswOfoJB.ui'
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

class Ui_classDialog(object):
    def setupUi(self, classDialog):
        if not classDialog.objectName():
            classDialog.setObjectName(u"classDialog")
        classDialog.resize(711, 555)
        self.gridLayout = QGridLayout(classDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listWidget = QListWidget(classDialog)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bNew = QPushButton(classDialog)
        self.bNew.setObjectName(u"bNew")

        self.verticalLayout.addWidget(self.bNew)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.bOpen = QPushButton(classDialog)
        self.bOpen.setObjectName(u"bOpen")

        self.verticalLayout.addWidget(self.bOpen)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)


        self.retranslateUi(classDialog)

        QMetaObject.connectSlotsByName(classDialog)
    # setupUi

    def retranslateUi(self, classDialog):
        classDialog.setWindowTitle(QCoreApplication.translate("classDialog", u"Classes", None))
        self.bNew.setText(QCoreApplication.translate("classDialog", u"New", None))
        self.bOpen.setText(QCoreApplication.translate("classDialog", u"Load", None))
    # retranslateUi

