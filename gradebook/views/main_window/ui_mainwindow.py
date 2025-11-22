# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowlvJxIi.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1036, 650)
        self.actionClasses = QAction(MainWindow)
        self.actionClasses.setObjectName(u"actionClasses")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lClassName = QLabel(self.centralwidget)
        self.lClassName.setObjectName(u"lClassName")
        font = QFont()
        font.setPointSize(14)
        self.lClassName.setFont(font)

        self.gridLayout.addWidget(self.lClassName, 0, 0, 1, 1)

        self.lStatus = QLabel(self.centralwidget)
        self.lStatus.setObjectName(u"lStatus")

        self.gridLayout.addWidget(self.lStatus, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bAdd = QPushButton(self.centralwidget)
        self.bAdd.setObjectName(u"bAdd")

        self.horizontalLayout.addWidget(self.bAdd)

        self.bRemove = QPushButton(self.centralwidget)
        self.bRemove.setObjectName(u"bRemove")

        self.horizontalLayout.addWidget(self.bRemove)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bSave = QPushButton(self.centralwidget)
        self.bSave.setObjectName(u"bSave")

        self.horizontalLayout.addWidget(self.bSave)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.TabTemplate = QWidget()
        self.TabTemplate.setObjectName(u"TabTemplate")
        self.gridLayout_3 = QGridLayout(self.TabTemplate)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tableWidget = QTableWidget(self.TabTemplate)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout_3.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.TabTemplate, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1036, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionClasses)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Gradebook", None))
        self.actionClasses.setText(QCoreApplication.translate("MainWindow", u"Classes", None))
        self.lClassName.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lStatus.setText(QCoreApplication.translate("MainWindow", u"Status: ", None))
        self.bAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.bRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.bSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabTemplate), QCoreApplication.translate("MainWindow", u"TabTemplate", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

