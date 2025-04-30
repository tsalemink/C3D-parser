# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'options_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        if not OptionsDialog.objectName():
            OptionsDialog.setObjectName(u"OptionsDialog")
        OptionsDialog.resize(450, 200)
        self.verticalLayout = QVBoxLayout(OptionsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(OptionsDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.labelLineWidth = QLabel(self.groupBox)
        self.labelLineWidth.setObjectName(u"labelLineWidth")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelLineWidth)

        self.doubleSpinBoxLineWidth = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxLineWidth.setObjectName(u"doubleSpinBoxLineWidth")
        self.doubleSpinBoxLineWidth.setValue(1.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBoxLineWidth)

        self.labelInputDirectory = QLabel(self.groupBox)
        self.labelInputDirectory.setObjectName(u"labelInputDirectory")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelInputDirectory)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditRootInput = QLineEdit(self.groupBox)
        self.lineEditRootInput.setObjectName(u"lineEditRootInput")

        self.horizontalLayout_2.addWidget(self.lineEditRootInput)

        self.pushButtonRootInputChooser = QPushButton(self.groupBox)
        self.pushButtonRootInputChooser.setObjectName(u"pushButtonRootInputChooser")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRootInputChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonRootInputChooser.setSizePolicy(sizePolicy)
        self.pushButtonRootInputChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout_2.addWidget(self.pushButtonRootInputChooser)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.labelOutputDirectory = QLabel(self.groupBox)
        self.labelOutputDirectory.setObjectName(u"labelOutputDirectory")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelOutputDirectory)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditRootOutput = QLineEdit(self.groupBox)
        self.lineEditRootOutput.setObjectName(u"lineEditRootOutput")

        self.horizontalLayout.addWidget(self.lineEditRootOutput)

        self.pushButtonRootOutputChooser = QPushButton(self.groupBox)
        self.pushButtonRootOutputChooser.setObjectName(u"pushButtonRootOutputChooser")
        sizePolicy.setHeightForWidth(self.pushButtonRootOutputChooser.sizePolicy().hasHeightForWidth())
        self.pushButtonRootOutputChooser.setSizePolicy(sizePolicy)
        self.pushButtonRootOutputChooser.setStyleSheet(u"padding: 3px 8px;")

        self.horizontalLayout.addWidget(self.pushButtonRootOutputChooser)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(OptionsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(OptionsDialog)
        self.buttonBox.accepted.connect(OptionsDialog.accept)
        self.buttonBox.rejected.connect(OptionsDialog.reject)

        QMetaObject.connectSlotsByName(OptionsDialog)
    # setupUi

    def retranslateUi(self, OptionsDialog):
        OptionsDialog.setWindowTitle(QCoreApplication.translate("OptionsDialog", u"Options", None))
        self.groupBox.setTitle(QCoreApplication.translate("OptionsDialog", u"Plots", None))
        self.labelLineWidth.setText(QCoreApplication.translate("OptionsDialog", u"Line Width:", None))
        self.labelInputDirectory.setText(QCoreApplication.translate("OptionsDialog", u"Input Data Directory:", None))
        self.pushButtonRootInputChooser.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.labelOutputDirectory.setText(QCoreApplication.translate("OptionsDialog", u"Output Data Directory:", None))
        self.pushButtonRootOutputChooser.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
    # retranslateUi

