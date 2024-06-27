# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QSplitter, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.frame_trial = QFrame(self.splitter)
        self.frame_trial.setObjectName(u"frame_trial")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_trial.sizePolicy().hasHeightForWidth())
        self.frame_trial.setSizePolicy(sizePolicy)
        self.frame_trial.setMinimumSize(QSize(0, 0))
        self.frame_trial.setFrameShape(QFrame.StyledPanel)
        self.frame_trial.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_trial)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame_trial)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditDirectory = QLineEdit(self.frame_trial)
        self.lineEditDirectory.setObjectName(u"lineEditDirectory")

        self.horizontalLayout.addWidget(self.lineEditDirectory)

        self.pushButtonDirectoryChooser = QPushButton(self.frame_trial)
        self.pushButtonDirectoryChooser.setObjectName(u"pushButtonDirectoryChooser")
        self.pushButtonDirectoryChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout.addWidget(self.pushButtonDirectoryChooser)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.listWidgetFiles = QListWidget(self.frame_trial)
        self.listWidgetFiles.setObjectName(u"listWidgetFiles")

        self.verticalLayout_2.addWidget(self.listWidgetFiles)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonScanDirectory = QPushButton(self.frame_trial)
        self.pushButtonScanDirectory.setObjectName(u"pushButtonScanDirectory")
        self.pushButtonScanDirectory.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonScanDirectory)

        self.pushButtonParseData = QPushButton(self.frame_trial)
        self.pushButtonParseData.setObjectName(u"pushButtonParseData")
        self.pushButtonParseData.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonParseData)

        self.pushButtonUpload = QPushButton(self.frame_trial)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")
        self.pushButtonUpload.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonUpload)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.frame_trial)
        self.frame_visualisation = QFrame(self.splitter)
        self.frame_visualisation.setObjectName(u"frame_visualisation")
        self.frame_visualisation.setFrameShape(QFrame.StyledPanel)
        self.frame_visualisation.setFrameShadow(QFrame.Raised)
        self.splitter.addWidget(self.frame_visualisation)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Input:", None))
        self.pushButtonDirectoryChooser.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pushButtonScanDirectory.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.pushButtonParseData.setText(QCoreApplication.translate("MainWindow", u"Parse C3D Data", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
    # retranslateUi

