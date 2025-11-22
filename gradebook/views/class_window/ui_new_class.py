# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_classTVtFHc.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDateEdit, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QWidget)

class Ui_NewClassDialog(object):
    def setupUi(self, NewClassDialog):
        if not NewClassDialog.objectName():
            NewClassDialog.setObjectName(u"NewClassDialog")
        NewClassDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        NewClassDialog.resize(328, 125)
        self.gridLayout = QGridLayout(NewClassDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(NewClassDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.tbClassName = QLineEdit(NewClassDialog)
        self.tbClassName.setObjectName(u"tbClassName")

        self.gridLayout.addWidget(self.tbClassName, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(NewClassDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.dStart = QDateEdit(NewClassDialog)
        self.dStart.setObjectName(u"dStart")

        self.horizontalLayout.addWidget(self.dStart)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(NewClassDialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.dEnd = QDateEdit(NewClassDialog)
        self.dEnd.setObjectName(u"dEnd")

        self.horizontalLayout.addWidget(self.dEnd)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.buttonBox = QDialogButtonBox(NewClassDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)


        self.retranslateUi(NewClassDialog)
        self.buttonBox.accepted.connect(NewClassDialog.accept)
        self.buttonBox.rejected.connect(NewClassDialog.reject)

        QMetaObject.connectSlotsByName(NewClassDialog)
    # setupUi

    def retranslateUi(self, NewClassDialog):
        NewClassDialog.setWindowTitle(QCoreApplication.translate("NewClassDialog", u"New Class", None))
        self.label.setText(QCoreApplication.translate("NewClassDialog", u"Class Name:", None))
        self.label_2.setText(QCoreApplication.translate("NewClassDialog", u"Start Date:", None))
        self.label_3.setText(QCoreApplication.translate("NewClassDialog", u"End Date:", None))
    # retranslateUi

