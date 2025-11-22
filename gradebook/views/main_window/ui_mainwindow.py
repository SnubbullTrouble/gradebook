# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowwgrllW.ui'
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

        self.tFinal = QTabWidget(self.centralwidget)
        self.tFinal.setObjectName(u"tFinal")
        self.Roster = QWidget()
        self.Roster.setObjectName(u"Roster")
        self.gridLayout_3 = QGridLayout(self.Roster)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tRoster = QTableWidget(self.Roster)
        self.tRoster.setObjectName(u"tRoster")

        self.gridLayout_3.addWidget(self.tRoster, 0, 0, 1, 1)

        self.tFinal.addTab(self.Roster, "")
        self.Homework = QWidget()
        self.Homework.setObjectName(u"Homework")
        self.gridLayout_2 = QGridLayout(self.Homework)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tHomework = QTableWidget(self.Homework)
        self.tHomework.setObjectName(u"tHomework")

        self.gridLayout_2.addWidget(self.tHomework, 0, 0, 1, 1)

        self.tFinal.addTab(self.Homework, "")
        self.Quiz = QWidget()
        self.Quiz.setObjectName(u"Quiz")
        self.gridLayout_4 = QGridLayout(self.Quiz)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tQuiz = QTableWidget(self.Quiz)
        self.tQuiz.setObjectName(u"tQuiz")

        self.gridLayout_4.addWidget(self.tQuiz, 0, 0, 1, 1)

        self.tFinal.addTab(self.Quiz, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tTest = QTableWidget(self.tab_2)
        self.tTest.setObjectName(u"tTest")

        self.gridLayout_5.addWidget(self.tTest, 0, 0, 1, 1)

        self.tFinal.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_6 = QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tQuiz_2 = QTableWidget(self.tab_3)
        self.tQuiz_2.setObjectName(u"tQuiz_2")

        self.gridLayout_6.addWidget(self.tQuiz_2, 0, 0, 1, 1)

        self.tFinal.addTab(self.tab_3, "")
        self.Project = QWidget()
        self.Project.setObjectName(u"Project")
        self.gridLayout_7 = QGridLayout(self.Project)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tProject = QTableWidget(self.Project)
        self.tProject.setObjectName(u"tProject")

        self.gridLayout_7.addWidget(self.tProject, 0, 0, 1, 1)

        self.tFinal.addTab(self.Project, "")
        self.Grade = QWidget()
        self.Grade.setObjectName(u"Grade")
        self.gridLayout_8 = QGridLayout(self.Grade)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.tGrade = QTableWidget(self.Grade)
        self.tGrade.setObjectName(u"tGrade")

        self.gridLayout_8.addWidget(self.tGrade, 0, 0, 1, 1)

        self.tFinal.addTab(self.Grade, "")

        self.gridLayout.addWidget(self.tFinal, 1, 0, 1, 1)

        self.lClassName = QLabel(self.centralwidget)
        self.lClassName.setObjectName(u"lClassName")
        font = QFont()
        font.setPointSize(14)
        self.lClassName.setFont(font)

        self.gridLayout.addWidget(self.lClassName, 0, 0, 1, 1)

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

        self.tFinal.setCurrentIndex(6)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Gradebook", None))
        self.actionClasses.setText(QCoreApplication.translate("MainWindow", u"Classes", None))
        self.lStatus.setText(QCoreApplication.translate("MainWindow", u"Status: ", None))
        self.bAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.bRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.bSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tFinal.setTabText(self.tFinal.indexOf(self.Roster), QCoreApplication.translate("MainWindow", u"Roster", None))
        self.tFinal.setTabText(self.tFinal.indexOf(self.Homework), QCoreApplication.translate("MainWindow", u"Homework", None))
        self.tFinal.setTabText(self.tFinal.indexOf(self.Quiz), QCoreApplication.translate("MainWindow", u"Quiz", None))
        self.tFinal.setTabText(self.tFinal.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Test", None))
        self.tFinal.setTabText(self.tFinal.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Final", None))
        self.tFinal.setTabText(self.tFinal.indexOf(self.Project), QCoreApplication.translate("MainWindow", u"Project", None))
        self.tFinal.setTabText(self.tFinal.indexOf(self.Grade), QCoreApplication.translate("MainWindow", u"Grade", None))
        self.lClassName.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

