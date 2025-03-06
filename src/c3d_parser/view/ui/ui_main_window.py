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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSplitter, QTabWidget, QVBoxLayout,
    QWidget)

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
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frameTrial)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.comboBoxLab = QComboBox(self.frameTrial)
        self.comboBoxLab.setObjectName(u"comboBoxLab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxLab.sizePolicy().hasHeightForWidth())
        self.comboBoxLab.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.comboBoxLab)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.frameTrial)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.doubleSpinBoxMarkerDiameter = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxMarkerDiameter.setObjectName(u"doubleSpinBoxMarkerDiameter")
        self.doubleSpinBoxMarkerDiameter.setValue(14.000000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBoxMarkerDiameter)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.frameTrial)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.doubleSpinBoxKADMarkerDiameter = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxKADMarkerDiameter.setObjectName(u"doubleSpinBoxKADMarkerDiameter")
        self.doubleSpinBoxKADMarkerDiameter.setValue(25.000000000000000)

        self.horizontalLayout_5.addWidget(self.doubleSpinBoxKADMarkerDiameter)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

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

        self.listWidgetFiles = CustomListWidget(self.frameTrial)
        self.listWidgetFiles.setObjectName(u"listWidgetFiles")

        self.verticalLayout_2.addWidget(self.listWidgetFiles)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
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
        self.tabWidget = QTabWidget(self.frameVisualisation)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabGRF = QWidget()
        self.tabGRF.setObjectName(u"tabGRF")
        self.verticalLayout_4 = QVBoxLayout(self.tabGRF)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.layoutGRFPlot = QVBoxLayout()
        self.layoutGRFPlot.setObjectName(u"layoutGRFPlot")

        self.verticalLayout_4.addLayout(self.layoutGRFPlot)

        self.tabWidget.addTab(self.tabGRF, "")
        self.tabTorque = QWidget()
        self.tabTorque.setObjectName(u"tabTorque")
        self.verticalLayout_8 = QVBoxLayout(self.tabTorque)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.layoutTorquePlot = QVBoxLayout()
        self.layoutTorquePlot.setObjectName(u"layoutTorquePlot")

        self.verticalLayout_8.addLayout(self.layoutTorquePlot)

        self.tabWidget.addTab(self.tabTorque, "")
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

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.splitter.addWidget(self.frameVisualisation)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1500, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionOptions)

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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Lab: ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Marker Diameter:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"KAD Marker Diameter:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Input:", None))
        self.pushButtonDirectoryChooser.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pushButtonParseData.setText(QCoreApplication.translate("MainWindow", u"Parse C3D Data", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGRF), QCoreApplication.translate("MainWindow", u"GRF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTorque), QCoreApplication.translate("MainWindow", u"Torque", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKinematic), QCoreApplication.translate("MainWindow", u"Kinematic", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKinetic), QCoreApplication.translate("MainWindow", u"Kinetic", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

