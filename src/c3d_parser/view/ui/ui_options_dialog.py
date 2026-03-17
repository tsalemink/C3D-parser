# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'options_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        if not OptionsDialog.objectName():
            OptionsDialog.setObjectName(u"OptionsDialog")
        OptionsDialog.resize(450, 562)
        self.verticalLayout = QVBoxLayout(OptionsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_3 = QGroupBox(OptionsDialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.formLayout_3 = QFormLayout(self.groupBox_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.labelInputDirectory = QLabel(self.groupBox_3)
        self.labelInputDirectory.setObjectName(u"labelInputDirectory")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelInputDirectory)

        self.labelOutputDirectory = QLabel(self.groupBox_3)
        self.labelOutputDirectory.setObjectName(u"labelOutputDirectory")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelOutputDirectory)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditRootOutput = QLineEdit(self.groupBox_3)
        self.lineEditRootOutput.setObjectName(u"lineEditRootOutput")

        self.horizontalLayout.addWidget(self.lineEditRootOutput)

        self.pushButtonRootOutputChooser = QPushButton(self.groupBox_3)
        self.pushButtonRootOutputChooser.setObjectName(u"pushButtonRootOutputChooser")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRootOutputChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonRootOutputChooser.setSizePolicy(sizePolicy)
        self.pushButtonRootOutputChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout.addWidget(self.pushButtonRootOutputChooser)


        self.formLayout_3.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditRootInput = QLineEdit(self.groupBox_3)
        self.lineEditRootInput.setObjectName(u"lineEditRootInput")

        self.horizontalLayout_2.addWidget(self.lineEditRootInput)

        self.pushButtonRootInputChooser = QPushButton(self.groupBox_3)
        self.pushButtonRootInputChooser.setObjectName(u"pushButtonRootInputChooser")
        sizePolicy.setHeightForWidth(self.pushButtonRootInputChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonRootInputChooser.setSizePolicy(sizePolicy)
        self.pushButtonRootInputChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout_2.addWidget(self.pushButtonRootInputChooser)


        self.formLayout_3.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(OptionsDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.labelLineWidth = QLabel(self.groupBox)
        self.labelLineWidth.setObjectName(u"labelLineWidth")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelLineWidth)

        self.doubleSpinBoxLineWidth = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxLineWidth.setObjectName(u"doubleSpinBoxLineWidth")
        self.doubleSpinBoxLineWidth.setValue(1.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.doubleSpinBoxLineWidth)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEditLeftColour = QLineEdit(self.groupBox)
        self.lineEditLeftColour.setObjectName(u"lineEditLeftColour")
        self.lineEditLeftColour.setMaxLength(7)

        self.horizontalLayout_4.addWidget(self.lineEditLeftColour)

        self.labelLeftColour = QLabel(self.groupBox)
        self.labelLeftColour.setObjectName(u"labelLeftColour")
        sizePolicy.setHeightForWidth(self.labelLeftColour.sizePolicy().hasHeightForWidth())
        self.labelLeftColour.setSizePolicy(sizePolicy)
        self.labelLeftColour.setMinimumSize(QSize(18, 18))
        self.labelLeftColour.setStyleSheet(u"border: 1px solid black;\n"
"border-radius: 2px; \n"
"background-color: #FFFFFF")

        self.horizontalLayout_4.addWidget(self.labelLeftColour)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEditRightColour = QLineEdit(self.groupBox)
        self.lineEditRightColour.setObjectName(u"lineEditRightColour")
        self.lineEditRightColour.setMaxLength(7)

        self.horizontalLayout_5.addWidget(self.lineEditRightColour)

        self.labelRightColour = QLabel(self.groupBox)
        self.labelRightColour.setObjectName(u"labelRightColour")
        sizePolicy.setHeightForWidth(self.labelRightColour.sizePolicy().hasHeightForWidth())
        self.labelRightColour.setSizePolicy(sizePolicy)
        self.labelRightColour.setMinimumSize(QSize(18, 18))
        self.labelRightColour.setStyleSheet(u"border: 1px solid black;\n"
"border-radius: 2px; \n"
"background-color: #FFFFFF")

        self.horizontalLayout_5.addWidget(self.labelRightColour)


        self.formLayout.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEditSelectionColour = QLineEdit(self.groupBox)
        self.lineEditSelectionColour.setObjectName(u"lineEditSelectionColour")
        self.lineEditSelectionColour.setMaxLength(7)

        self.horizontalLayout_6.addWidget(self.lineEditSelectionColour)

        self.labelSelectionColour = QLabel(self.groupBox)
        self.labelSelectionColour.setObjectName(u"labelSelectionColour")
        sizePolicy.setHeightForWidth(self.labelSelectionColour.sizePolicy().hasHeightForWidth())
        self.labelSelectionColour.setSizePolicy(sizePolicy)
        self.labelSelectionColour.setMinimumSize(QSize(18, 18))
        self.labelSelectionColour.setStyleSheet(u"border: 1px solid black;\n"
"border-radius: 2px; \n"
"background-color: #FFFFFF")

        self.horizontalLayout_6.addWidget(self.labelSelectionColour)


        self.formLayout.setLayout(6, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(OptionsDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.checkBoxOptimiseKneeAxis = QCheckBox(self.groupBox_2)
        self.checkBoxOptimiseKneeAxis.setObjectName(u"checkBoxOptimiseKneeAxis")
        self.checkBoxOptimiseKneeAxis.setChecked(False)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.checkBoxOptimiseKneeAxis)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(OptionsDialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout = QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBoxFilterTRC = QCheckBox(self.groupBox_4)
        self.checkBoxFilterTRC.setObjectName(u"checkBoxFilterTRC")

        self.gridLayout.addWidget(self.checkBoxFilterTRC, 0, 0, 1, 1)

        self.checkBoxFilterGRF = QCheckBox(self.groupBox_4)
        self.checkBoxFilterGRF.setObjectName(u"checkBoxFilterGRF")

        self.gridLayout.addWidget(self.checkBoxFilterGRF, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(OptionsDialog)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBoxCustomTaskSet = QCheckBox(self.groupBox_5)
        self.checkBoxCustomTaskSet.setObjectName(u"checkBoxCustomTaskSet")

        self.verticalLayout_2.addWidget(self.checkBoxCustomTaskSet)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelIKTaskSet = QLabel(self.groupBox_5)
        self.labelIKTaskSet.setObjectName(u"labelIKTaskSet")

        self.horizontalLayout_7.addWidget(self.labelIKTaskSet)

        self.lineEditIKTaskSet = QLineEdit(self.groupBox_5)
        self.lineEditIKTaskSet.setObjectName(u"lineEditIKTaskSet")

        self.horizontalLayout_7.addWidget(self.lineEditIKTaskSet)

        self.pushButtonIKTaskSetChooser = QPushButton(self.groupBox_5)
        self.pushButtonIKTaskSetChooser.setObjectName(u"pushButtonIKTaskSetChooser")
        sizePolicy.setHeightForWidth(self.pushButtonIKTaskSetChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonIKTaskSetChooser.setSizePolicy(sizePolicy)
        self.pushButtonIKTaskSetChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout_7.addWidget(self.pushButtonIKTaskSetChooser)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButtonOK = QPushButton(OptionsDialog)
        self.pushButtonOK.setObjectName(u"pushButtonOK")

        self.horizontalLayout_3.addWidget(self.pushButtonOK)

        self.pushButtonCancel = QPushButton(OptionsDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout_3.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(OptionsDialog)
        self.pushButtonOK.clicked.connect(OptionsDialog.accept)
        self.pushButtonCancel.clicked.connect(OptionsDialog.reject)

        QMetaObject.connectSlotsByName(OptionsDialog)
    # setupUi

    def retranslateUi(self, OptionsDialog):
        OptionsDialog.setWindowTitle(QCoreApplication.translate("OptionsDialog", u"Options", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("OptionsDialog", u"File", None))
        self.labelInputDirectory.setText(QCoreApplication.translate("OptionsDialog", u"Input Data Directory:", None))
        self.labelOutputDirectory.setText(QCoreApplication.translate("OptionsDialog", u"Output Data Directory:", None))
        self.pushButtonRootOutputChooser.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.pushButtonRootInputChooser.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.groupBox.setTitle(QCoreApplication.translate("OptionsDialog", u"Plots", None))
        self.labelLineWidth.setText(QCoreApplication.translate("OptionsDialog", u"Line Width:", None))
        self.label.setText(QCoreApplication.translate("OptionsDialog", u"Left Side Colour:", None))
        self.label_2.setText(QCoreApplication.translate("OptionsDialog", u"Right Side Colour:", None))
        self.label_3.setText(QCoreApplication.translate("OptionsDialog", u"Selection Colour:", None))
        self.lineEditLeftColour.setText(QCoreApplication.translate("OptionsDialog", u"#FFFFFF", None))
        self.labelLeftColour.setText("")
        self.lineEditRightColour.setText(QCoreApplication.translate("OptionsDialog", u"#FFFFFF", None))
        self.labelRightColour.setText("")
        self.lineEditSelectionColour.setText(QCoreApplication.translate("OptionsDialog", u"#FFFFFF", None))
        self.labelSelectionColour.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("OptionsDialog", u"OpenSim Model", None))
        self.checkBoxOptimiseKneeAxis.setText(QCoreApplication.translate("OptionsDialog", u"Perform knee-axis optimisation", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("OptionsDialog", u"Filtering", None))
        self.checkBoxFilterTRC.setText(QCoreApplication.translate("OptionsDialog", u"Filter TRC data", None))
        self.checkBoxFilterGRF.setText(QCoreApplication.translate("OptionsDialog", u"Filter GRF data", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("OptionsDialog", u"Inverse Kinematics", None))
        self.checkBoxCustomTaskSet.setText(QCoreApplication.translate("OptionsDialog", u"Use custom IK task set file", None))
        self.labelIKTaskSet.setText(QCoreApplication.translate("OptionsDialog", u"IK task set file:", None))
        self.pushButtonIKTaskSetChooser.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.pushButtonOK.setText(QCoreApplication.translate("OptionsDialog", u"OK", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("OptionsDialog", u"Cancel", None))
    # retranslateUi

