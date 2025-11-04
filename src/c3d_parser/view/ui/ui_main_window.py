# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSpinBox, QSplitter,
    QTabWidget, QVBoxLayout, QWidget)

from c3d_parser.view.widgets import CustomListWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1500, 800)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionOptions = QAction(MainWindow)
        self.actionOptions.setObjectName(u"actionOptions")
        self.actionReloadInput = QAction(MainWindow)
        self.actionReloadInput.setObjectName(u"actionReloadInput")
        self.actionCustomMarkerSet = QAction(MainWindow)
        self.actionCustomMarkerSet.setObjectName(u"actionCustomMarkerSet")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.frameTrial = QFrame(self.splitter)
        self.frameTrial.setObjectName(u"frameTrial")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameTrial.sizePolicy().hasHeightForWidth())
        self.frameTrial.setSizePolicy(sizePolicy)
        self.frameTrial.setMinimumSize(QSize(0, 0))
        self.frameTrial.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameTrial.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frameTrial)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 5, 0, 5)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, -1, 5, -1)
        self.label_2 = QLabel(self.frameTrial)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.comboBoxLab = QComboBox(self.frameTrial)
        self.comboBoxLab.setObjectName(u"comboBoxLab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxLab.sizePolicy().hasHeightForWidth())
        self.comboBoxLab.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.comboBoxLab)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, -1, 5, -1)
        self.label = QLabel(self.frameTrial)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(41, 0))

        self.horizontalLayout.addWidget(self.label)

        self.lineEditInputDirectory = QLineEdit(self.frameTrial)
        self.lineEditInputDirectory.setObjectName(u"lineEditInputDirectory")
        sizePolicy1.setHeightForWidth(self.lineEditInputDirectory.sizePolicy().hasHeightForWidth())
        self.lineEditInputDirectory.setSizePolicy(sizePolicy1)
        self.lineEditInputDirectory.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.lineEditInputDirectory)

        self.pushButtonInputDirectoryChooser = QPushButton(self.frameTrial)
        self.pushButtonInputDirectoryChooser.setObjectName(u"pushButtonInputDirectoryChooser")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonInputDirectoryChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonInputDirectoryChooser.setSizePolicy(sizePolicy2)
        self.pushButtonInputDirectoryChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout.addWidget(self.pushButtonInputDirectoryChooser)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(5, -1, 5, -1)
        self.label_5 = QLabel(self.frameTrial)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(41, 0))

        self.horizontalLayout_6.addWidget(self.label_5)

        self.lineEditOutputDirectory = QLineEdit(self.frameTrial)
        self.lineEditOutputDirectory.setObjectName(u"lineEditOutputDirectory")
        sizePolicy1.setHeightForWidth(self.lineEditOutputDirectory.sizePolicy().hasHeightForWidth())
        self.lineEditOutputDirectory.setSizePolicy(sizePolicy1)
        self.lineEditOutputDirectory.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.lineEditOutputDirectory)

        self.pushButtonOutputDirectoryChooser = QPushButton(self.frameTrial)
        self.pushButtonOutputDirectoryChooser.setObjectName(u"pushButtonOutputDirectoryChooser")
        sizePolicy2.setHeightForWidth(self.pushButtonOutputDirectoryChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonOutputDirectoryChooser.setSizePolicy(sizePolicy2)
        self.pushButtonOutputDirectoryChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout_6.addWidget(self.pushButtonOutputDirectoryChooser)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.listWidgetFiles = CustomListWidget(self.frameTrial)
        self.listWidgetFiles.setObjectName(u"listWidgetFiles")

        self.verticalLayout_2.addWidget(self.listWidgetFiles)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(5, -1, 5, -1)
        self.label_12 = QLabel(self.frameTrial)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_14.addWidget(self.label_12)

        self.comboBoxSex = QComboBox(self.frameTrial)
        self.comboBoxSex.addItem("")
        self.comboBoxSex.addItem("")
        self.comboBoxSex.setObjectName(u"comboBoxSex")

        self.horizontalLayout_14.addWidget(self.comboBoxSex)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(5, -1, 5, -1)
        self.label_11 = QLabel(self.frameTrial)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_13.addWidget(self.label_11)

        self.spinBoxAge = QSpinBox(self.frameTrial)
        self.spinBoxAge.setObjectName(u"spinBoxAge")

        self.horizontalLayout_13.addWidget(self.spinBoxAge)


        self.verticalLayout_2.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, -1, 5, -1)
        self.label_4 = QLabel(self.frameTrial)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_5.addWidget(self.label_4)

        self.doubleSpinBoxHeight = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxHeight.setObjectName(u"doubleSpinBoxHeight")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxHeight.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxHeight.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxHeight.setDecimals(0)
        self.doubleSpinBoxHeight.setMaximum(9999.000000000000000)
        self.doubleSpinBoxHeight.setSingleStep(1.000000000000000)

        self.horizontalLayout_5.addWidget(self.doubleSpinBoxHeight)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(5, -1, 5, -1)
        self.label_6 = QLabel(self.frameTrial)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_8.addWidget(self.label_6)

        self.doubleSpinBoxBodyMass = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxBodyMass.setObjectName(u"doubleSpinBoxBodyMass")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxBodyMass.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxBodyMass.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxBodyMass.setMinimumSize(QSize(0, 0))
        self.doubleSpinBoxBodyMass.setMaximum(999.990000000000009)

        self.horizontalLayout_8.addWidget(self.doubleSpinBoxBodyMass)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(5, -1, 5, -1)
        self.label_15 = QLabel(self.frameTrial)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_17.addWidget(self.label_15)

        self.doubleSpinBoxASISWidth = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxASISWidth.setObjectName(u"doubleSpinBoxASISWidth")
        self.doubleSpinBoxASISWidth.setDecimals(1)
        self.doubleSpinBoxASISWidth.setMaximum(999.000000000000000)

        self.horizontalLayout_17.addWidget(self.doubleSpinBoxASISWidth)


        self.verticalLayout_2.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(5, -1, 5, -1)
        self.label_7 = QLabel(self.frameTrial)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_9.addWidget(self.label_7)

        self.doubleSpinBoxLeftKneeWidth = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxLeftKneeWidth.setObjectName(u"doubleSpinBoxLeftKneeWidth")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxLeftKneeWidth.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxLeftKneeWidth.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxLeftKneeWidth.setDecimals(1)
        self.doubleSpinBoxLeftKneeWidth.setMaximum(999.000000000000000)
        self.doubleSpinBoxLeftKneeWidth.setSingleStep(1.000000000000000)

        self.horizontalLayout_9.addWidget(self.doubleSpinBoxLeftKneeWidth)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, -1, 5, -1)
        self.label_8 = QLabel(self.frameTrial)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_10.addWidget(self.label_8)

        self.doubleSpinBoxRightKneeWidth = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxRightKneeWidth.setObjectName(u"doubleSpinBoxRightKneeWidth")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxRightKneeWidth.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxRightKneeWidth.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxRightKneeWidth.setDecimals(1)
        self.doubleSpinBoxRightKneeWidth.setMaximum(999.000000000000000)
        self.doubleSpinBoxRightKneeWidth.setSingleStep(1.000000000000000)

        self.horizontalLayout_10.addWidget(self.doubleSpinBoxRightKneeWidth)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(5, -1, 5, -1)
        self.label_13 = QLabel(self.frameTrial)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_15.addWidget(self.label_13)

        self.doubleSpinBoxLeftAnkleWidth = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxLeftAnkleWidth.setObjectName(u"doubleSpinBoxLeftAnkleWidth")
        self.doubleSpinBoxLeftAnkleWidth.setDecimals(1)
        self.doubleSpinBoxLeftAnkleWidth.setMaximum(999.000000000000000)

        self.horizontalLayout_15.addWidget(self.doubleSpinBoxLeftAnkleWidth)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(5, -1, 5, -1)
        self.label_14 = QLabel(self.frameTrial)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_16.addWidget(self.label_14)

        self.doubleSpinBoxRightAnkleWidth = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxRightAnkleWidth.setObjectName(u"doubleSpinBoxRightAnkleWidth")
        self.doubleSpinBoxRightAnkleWidth.setDecimals(1)
        self.doubleSpinBoxRightAnkleWidth.setMaximum(999.000000000000000)

        self.horizontalLayout_16.addWidget(self.doubleSpinBoxRightAnkleWidth)


        self.verticalLayout_2.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(5, -1, 5, -1)
        self.label_9 = QLabel(self.frameTrial)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_11.addWidget(self.label_9)

        self.doubleSpinBoxLeftLegLength = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxLeftLegLength.setObjectName(u"doubleSpinBoxLeftLegLength")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxLeftLegLength.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxLeftLegLength.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxLeftLegLength.setDecimals(0)
        self.doubleSpinBoxLeftLegLength.setMaximum(9999.000000000000000)
        self.doubleSpinBoxLeftLegLength.setSingleStep(1.000000000000000)

        self.horizontalLayout_11.addWidget(self.doubleSpinBoxLeftLegLength)


        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(5, -1, 5, -1)
        self.label_10 = QLabel(self.frameTrial)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_12.addWidget(self.label_10)

        self.doubleSpinBoxRightLegLength = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxRightLegLength.setObjectName(u"doubleSpinBoxRightLegLength")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxRightLegLength.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxRightLegLength.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxRightLegLength.setDecimals(0)
        self.doubleSpinBoxRightLegLength.setMaximum(9999.000000000000000)
        self.doubleSpinBoxRightLegLength.setSingleStep(1.000000000000000)

        self.horizontalLayout_12.addWidget(self.doubleSpinBoxRightLegLength)


        self.verticalLayout_2.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, -1, 5, -1)
        self.label_3 = QLabel(self.frameTrial)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setMinimumSize(QSize(134, 0))

        self.horizontalLayout_4.addWidget(self.label_3)

        self.doubleSpinBoxMarkerDiameter = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxMarkerDiameter.setObjectName(u"doubleSpinBoxMarkerDiameter")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxMarkerDiameter.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxMarkerDiameter.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxMarkerDiameter.setValue(14.000000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBoxMarkerDiameter)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, -1, 5, -1)
        self.pushButtonParseData = QPushButton(self.frameTrial)
        self.pushButtonParseData.setObjectName(u"pushButtonParseData")
        self.pushButtonParseData.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonParseData)

        self.pushButtonHarmonise = QPushButton(self.frameTrial)
        self.pushButtonHarmonise.setObjectName(u"pushButtonHarmonise")
        self.pushButtonHarmonise.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonHarmonise)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.frameTrial)
        self.frameVisualisation = QFrame(self.splitter)
        self.frameVisualisation.setObjectName(u"frameVisualisation")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frameVisualisation.sizePolicy().hasHeightForWidth())
        self.frameVisualisation.setSizePolicy(sizePolicy4)
        self.frameVisualisation.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameVisualisation.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frameVisualisation)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.frameVisualisation)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabKinematic = QWidget()
        self.tabKinematic.setObjectName(u"tabKinematic")
        self.verticalLayout_6 = QVBoxLayout(self.tabKinematic)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.layoutKinematicPlot = QVBoxLayout()
        self.layoutKinematicPlot.setObjectName(u"layoutKinematicPlot")

        self.verticalLayout_6.addLayout(self.layoutKinematicPlot)

        self.tabWidget.addTab(self.tabKinematic, "")
        self.tabKinetic = QWidget()
        self.tabKinetic.setObjectName(u"tabKinetic")
        self.verticalLayout_7 = QVBoxLayout(self.tabKinetic)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.layoutKineticPlot = QVBoxLayout()
        self.layoutKineticPlot.setObjectName(u"layoutKineticPlot")

        self.verticalLayout_7.addLayout(self.layoutKineticPlot)

        self.tabWidget.addTab(self.tabKinetic, "")
        self.tabGRF = QWidget()
        self.tabGRF.setObjectName(u"tabGRF")
        self.verticalLayout_4 = QVBoxLayout(self.tabGRF)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.layoutGRFPlot = QVBoxLayout()
        self.layoutGRFPlot.setObjectName(u"layoutGRFPlot")

        self.verticalLayout_4.addLayout(self.layoutGRFPlot)

        self.tabWidget.addTab(self.tabGRF, "")
        self.tabSpatiotemporal = QWidget()
        self.tabSpatiotemporal.setObjectName(u"tabSpatiotemporal")
        self.verticalLayout_8 = QVBoxLayout(self.tabSpatiotemporal)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scrollArea = QScrollArea(self.tabSpatiotemporal)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"background-color: transparent;")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaSpatiotemporal = QWidget()
        self.scrollAreaSpatiotemporal.setObjectName(u"scrollAreaSpatiotemporal")
        self.scrollAreaSpatiotemporal.setGeometry(QRect(0, 0, 1193, 668))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaSpatiotemporal)
        self.verticalLayout_5.setSpacing(40)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(30, 30, 30, 30)
        self.scrollArea.setWidget(self.scrollAreaSpatiotemporal)

        self.verticalLayout_8.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tabSpatiotemporal, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(6, -1, -1, -1)
        self.labelProgress = QLabel(self.frameVisualisation)
        self.labelProgress.setObjectName(u"labelProgress")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.labelProgress.sizePolicy().hasHeightForWidth())
        self.labelProgress.setSizePolicy(sizePolicy5)
        self.labelProgress.setMinimumSize(QSize(0, 24))

        self.horizontalLayout_7.addWidget(self.labelProgress)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.splitter.addWidget(self.frameVisualisation)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1500, 33))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName(u"menuView")
        self.menuMarker = QMenu(self.menuBar)
        self.menuMarker.setObjectName(u"menuMarker")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuMarker.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionReloadInput)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionOptions)
        self.menuMarker.addAction(self.actionCustomMarkerSet)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionOptions.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.actionReloadInput.setText(QCoreApplication.translate("MainWindow", u"Reload Input", None))
        self.actionCustomMarkerSet.setText(QCoreApplication.translate("MainWindow", u"Custom Marker Set", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Lab: ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Input:", None))
        self.pushButtonInputDirectoryChooser.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output:", None))
        self.pushButtonOutputDirectoryChooser.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Sex:", None))
        self.comboBoxSex.setItemText(0, QCoreApplication.translate("MainWindow", u"Female", None))
        self.comboBoxSex.setItemText(1, QCoreApplication.translate("MainWindow", u"Male", None))

        self.comboBoxSex.setCurrentText("")
        self.comboBoxSex.setPlaceholderText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Age:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Height (mm):", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Body Mass (kg):", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Inter ASIS Distance (mm):", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Left Knee Width (mm):", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Right Knee Width (mm):", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Left Ankle Width (mm):", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Right Ankle Width (mm):", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Left Leg Length (mm):", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Right Leg Length (mm):", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Marker Diameter (mm):", None))
        self.pushButtonParseData.setText(QCoreApplication.translate("MainWindow", u"Process Data", None))
        self.pushButtonHarmonise.setText(QCoreApplication.translate("MainWindow", u"Harmonise Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKinematic), QCoreApplication.translate("MainWindow", u"Kinematic", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKinetic), QCoreApplication.translate("MainWindow", u"Kinetic", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGRF), QCoreApplication.translate("MainWindow", u"GRF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSpatiotemporal), QCoreApplication.translate("MainWindow", u"Spatio-temporal", None))
        self.labelProgress.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuMarker.setTitle(QCoreApplication.translate("MainWindow", u"Marker", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

