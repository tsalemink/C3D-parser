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
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.doubleSpinBoxMarkerDiameter = QDoubleSpinBox(self.frameTrial)
        self.doubleSpinBoxMarkerDiameter.setObjectName(u"doubleSpinBoxMarkerDiameter")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.doubleSpinBoxMarkerDiameter.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxMarkerDiameter.setSizePolicy(sizePolicy3)
        self.doubleSpinBoxMarkerDiameter.setValue(14.000000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBoxMarkerDiameter)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frameTrial)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditInputDirectory = QLineEdit(self.frameTrial)
        self.lineEditInputDirectory.setObjectName(u"lineEditInputDirectory")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEditInputDirectory.sizePolicy().hasHeightForWidth())
        self.lineEditInputDirectory.setSizePolicy(sizePolicy4)
        self.lineEditInputDirectory.setMinimumSize(QSize(174, 0))

        self.horizontalLayout.addWidget(self.lineEditInputDirectory)

        self.pushButtonInputDirectoryChooser = QPushButton(self.frameTrial)
        self.pushButtonInputDirectoryChooser.setObjectName(u"pushButtonInputDirectoryChooser")
        sizePolicy4.setHeightForWidth(self.pushButtonInputDirectoryChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonInputDirectoryChooser.setSizePolicy(sizePolicy4)
        self.pushButtonInputDirectoryChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout.addWidget(self.pushButtonInputDirectoryChooser)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.frameTrial)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_6.addWidget(self.label_5)

        self.lineEditOutputDirectory = QLineEdit(self.frameTrial)
        self.lineEditOutputDirectory.setObjectName(u"lineEditOutputDirectory")
        sizePolicy4.setHeightForWidth(self.lineEditOutputDirectory.sizePolicy().hasHeightForWidth())
        self.lineEditOutputDirectory.setSizePolicy(sizePolicy4)
        self.lineEditOutputDirectory.setMinimumSize(QSize(174, 0))

        self.horizontalLayout_6.addWidget(self.lineEditOutputDirectory)

        self.pushButtonOutputDirectoryChooser = QPushButton(self.frameTrial)
        self.pushButtonOutputDirectoryChooser.setObjectName(u"pushButtonOutputDirectoryChooser")
        sizePolicy4.setHeightForWidth(self.pushButtonOutputDirectoryChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonOutputDirectoryChooser.setSizePolicy(sizePolicy4)
        self.pushButtonOutputDirectoryChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout_6.addWidget(self.pushButtonOutputDirectoryChooser)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

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

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(6, -1, -1, -1)
        self.labelProgress = QLabel(self.frameVisualisation)
        self.labelProgress.setObjectName(u"labelProgress")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"Input:", None))
        self.pushButtonInputDirectoryChooser.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output:", None))
        self.pushButtonOutputDirectoryChooser.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pushButtonParseData.setText(QCoreApplication.translate("MainWindow", u"Parse C3D Data", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGRF), QCoreApplication.translate("MainWindow", u"GRF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTorque), QCoreApplication.translate("MainWindow", u"Torque", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKinematic), QCoreApplication.translate("MainWindow", u"Kinematic", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKinetic), QCoreApplication.translate("MainWindow", u"Kinetic", None))
        self.labelProgress.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

