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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.frameTrial = QFrame(self.splitter)
        self.frameTrial.setObjectName(u"frameTrial")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameTrial.sizePolicy().hasHeightForWidth())
        self.frameTrial.setSizePolicy(sizePolicy)
        self.frameTrial.setMinimumSize(QSize(0, 0))
        self.frameTrial.setFrameShape(QFrame.StyledPanel)
        self.frameTrial.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frameTrial)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frameTrial)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditDirectory = QLineEdit(self.frameTrial)
        self.lineEditDirectory.setObjectName(u"lineEditDirectory")

        self.horizontalLayout.addWidget(self.lineEditDirectory)

        self.pushButtonDirectoryChooser = QPushButton(self.frameTrial)
        self.pushButtonDirectoryChooser.setObjectName(u"pushButtonDirectoryChooser")
        self.pushButtonDirectoryChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout.addWidget(self.pushButtonDirectoryChooser)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.listWidgetFiles = QListWidget(self.frameTrial)
        self.listWidgetFiles.setObjectName(u"listWidgetFiles")

        self.verticalLayout_2.addWidget(self.listWidgetFiles)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonScanDirectory = QPushButton(self.frameTrial)
        self.pushButtonScanDirectory.setObjectName(u"pushButtonScanDirectory")
        self.pushButtonScanDirectory.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonScanDirectory)

        self.pushButtonParseData = QPushButton(self.frameTrial)
        self.pushButtonParseData.setObjectName(u"pushButtonParseData")
        self.pushButtonParseData.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonParseData)

        self.pushButtonUpload = QPushButton(self.frameTrial)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")
        self.pushButtonUpload.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonUpload)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.frameTrial)
        self.frameVisualisation = QFrame(self.splitter)
        self.frameVisualisation.setObjectName(u"frameVisualisation")
        self.frameVisualisation.setFrameShape(QFrame.StyledPanel)
        self.frameVisualisation.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frameVisualisation)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.label_2 = QLabel(self.frameVisualisation)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.comboBoxChannels = QComboBox(self.frameVisualisation)
        self.comboBoxChannels.setObjectName(u"comboBoxChannels")

        self.horizontalLayout_3.addWidget(self.comboBoxChannels)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayoutPlot = QVBoxLayout()
        self.verticalLayoutPlot.setObjectName(u"verticalLayoutPlot")

        self.verticalLayout_3.addLayout(self.verticalLayoutPlot)

        self.splitter.addWidget(self.frameVisualisation)

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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Channels:", None))
    # retranslateUi
