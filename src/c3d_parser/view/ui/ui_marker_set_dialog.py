# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'marker_set_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MarkerSetDialog(object):
    def setupUi(self, MarkerSetDialog):
        if not MarkerSetDialog.objectName():
            MarkerSetDialog.setObjectName(u"MarkerSetDialog")
        MarkerSetDialog.resize(280, 588)
        self.verticalLayout = QVBoxLayout(MarkerSetDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(MarkerSetDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_2.addWidget(self.label_18)

        self.lineEditName = QLineEdit(self.groupBox_2)
        self.lineEditName.setObjectName(u"lineEditName")

        self.horizontalLayout_2.addWidget(self.lineEditName)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(MarkerSetDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBoxC7 = QComboBox(self.groupBox)
        self.comboBoxC7.setObjectName(u"comboBoxC7")
        self.comboBoxC7.setEditable(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBoxC7)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.comboBoxT2 = QComboBox(self.groupBox)
        self.comboBoxT2.setObjectName(u"comboBoxT2")
        self.comboBoxT2.setEditable(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBoxT2)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.comboBoxT10 = QComboBox(self.groupBox)
        self.comboBoxT10.setObjectName(u"comboBoxT10")
        self.comboBoxT10.setEditable(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBoxT10)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.comboBoxMAN = QComboBox(self.groupBox)
        self.comboBoxMAN.setObjectName(u"comboBoxMAN")
        self.comboBoxMAN.setEditable(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBoxMAN)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.comboBoxSACR = QComboBox(self.groupBox)
        self.comboBoxSACR.setObjectName(u"comboBoxSACR")
        self.comboBoxSACR.setEditable(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comboBoxSACR)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.comboBoxASI = QComboBox(self.groupBox)
        self.comboBoxASI.setObjectName(u"comboBoxASI")
        self.comboBoxASI.setEditable(True)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.comboBoxASI)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.comboBoxPSI = QComboBox(self.groupBox)
        self.comboBoxPSI.setObjectName(u"comboBoxPSI")
        self.comboBoxPSI.setEditable(True)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.comboBoxPSI)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_8)

        self.comboBoxTHI = QComboBox(self.groupBox)
        self.comboBoxTHI.setObjectName(u"comboBoxTHI")
        self.comboBoxTHI.setEditable(True)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.comboBoxTHI)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_9)

        self.comboBoxPAT = QComboBox(self.groupBox)
        self.comboBoxPAT.setObjectName(u"comboBoxPAT")
        self.comboBoxPAT.setEditable(True)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.comboBoxPAT)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_10)

        self.comboBoxKNE = QComboBox(self.groupBox)
        self.comboBoxKNE.setObjectName(u"comboBoxKNE")
        self.comboBoxKNE.setEditable(True)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.comboBoxKNE)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_11)

        self.comboBoxKNEM = QComboBox(self.groupBox)
        self.comboBoxKNEM.setObjectName(u"comboBoxKNEM")
        self.comboBoxKNEM.setEditable(True)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.comboBoxKNEM)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_12)

        self.comboBoxKAX = QComboBox(self.groupBox)
        self.comboBoxKAX.setObjectName(u"comboBoxKAX")
        self.comboBoxKAX.setEditable(True)

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.comboBoxKAX)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.label_13)

        self.comboBoxTIB = QComboBox(self.groupBox)
        self.comboBoxTIB.setObjectName(u"comboBoxTIB")
        self.comboBoxTIB.setEditable(True)

        self.formLayout.setWidget(12, QFormLayout.FieldRole, self.comboBoxTIB)

        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(13, QFormLayout.LabelRole, self.label_14)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(14, QFormLayout.LabelRole, self.label_15)

        self.comboBoxANK = QComboBox(self.groupBox)
        self.comboBoxANK.setObjectName(u"comboBoxANK")
        self.comboBoxANK.setEditable(True)

        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.comboBoxANK)

        self.comboBoxMED = QComboBox(self.groupBox)
        self.comboBoxMED.setObjectName(u"comboBoxMED")
        self.comboBoxMED.setEditable(True)

        self.formLayout.setWidget(14, QFormLayout.FieldRole, self.comboBoxMED)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(15, QFormLayout.LabelRole, self.label_16)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")

        self.formLayout.setWidget(16, QFormLayout.LabelRole, self.label_17)

        self.comboBoxHEE = QComboBox(self.groupBox)
        self.comboBoxHEE.setObjectName(u"comboBoxHEE")
        self.comboBoxHEE.setEditable(True)

        self.formLayout.setWidget(15, QFormLayout.FieldRole, self.comboBoxHEE)

        self.comboBoxTOE = QComboBox(self.groupBox)
        self.comboBoxTOE.setObjectName(u"comboBoxTOE")
        self.comboBoxTOE.setEditable(True)

        self.formLayout.setWidget(16, QFormLayout.FieldRole, self.comboBoxTOE)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonImport = QPushButton(MarkerSetDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout.addWidget(self.pushButtonImport)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonSave = QPushButton(MarkerSetDialog)
        self.pushButtonSave.setObjectName(u"pushButtonSave")

        self.horizontalLayout.addWidget(self.pushButtonSave)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(MarkerSetDialog)

        self.pushButtonSave.setDefault(True)


        QMetaObject.connectSlotsByName(MarkerSetDialog)
    # setupUi

    def retranslateUi(self, MarkerSetDialog):
        MarkerSetDialog.setWindowTitle(QCoreApplication.translate("MarkerSetDialog", u"Custom Marker Set", None))
        self.groupBox_2.setTitle("")
        self.label_18.setText(QCoreApplication.translate("MarkerSetDialog", u"Marker Set Name:", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("MarkerSetDialog", u"C7:", None))
        self.label_2.setText(QCoreApplication.translate("MarkerSetDialog", u"T2:", None))
        self.label_3.setText(QCoreApplication.translate("MarkerSetDialog", u"T10:", None))
        self.label_4.setText(QCoreApplication.translate("MarkerSetDialog", u"MAN:", None))
        self.label_5.setText(QCoreApplication.translate("MarkerSetDialog", u"SACR:", None))
        self.label_6.setText(QCoreApplication.translate("MarkerSetDialog", u"ASI:", None))
        self.label_7.setText(QCoreApplication.translate("MarkerSetDialog", u"PSI:", None))
        self.label_8.setText(QCoreApplication.translate("MarkerSetDialog", u"THI:", None))
        self.label_9.setText(QCoreApplication.translate("MarkerSetDialog", u"PAT:", None))
        self.label_10.setText(QCoreApplication.translate("MarkerSetDialog", u"KNE:", None))
        self.label_11.setText(QCoreApplication.translate("MarkerSetDialog", u"KNEM:", None))
        self.label_12.setText(QCoreApplication.translate("MarkerSetDialog", u"KAX:", None))
        self.label_13.setText(QCoreApplication.translate("MarkerSetDialog", u"TIB:", None))
        self.label_14.setText(QCoreApplication.translate("MarkerSetDialog", u"ANK:", None))
        self.label_15.setText(QCoreApplication.translate("MarkerSetDialog", u"MED:", None))
        self.label_16.setText(QCoreApplication.translate("MarkerSetDialog", u"HEE:", None))
        self.label_17.setText(QCoreApplication.translate("MarkerSetDialog", u"TOE:", None))
        self.pushButtonImport.setText(QCoreApplication.translate("MarkerSetDialog", u"Import", None))
        self.pushButtonSave.setText(QCoreApplication.translate("MarkerSetDialog", u"Save", None))
    # retranslateUi

