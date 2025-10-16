# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'marker_set_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MarkerSetDialog(object):
    def setupUi(self, MarkerSetDialog):
        if not MarkerSetDialog.objectName():
            MarkerSetDialog.setObjectName(u"MarkerSetDialog")
        MarkerSetDialog.resize(480, 622)
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
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(12)
        self.comboBoxT10 = QComboBox(self.groupBox)
        self.comboBoxT10.setObjectName(u"comboBoxT10")
        self.comboBoxT10.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxT10, 2, 1, 1, 1)

        self.comboBoxT2 = QComboBox(self.groupBox)
        self.comboBoxT2.setObjectName(u"comboBoxT2")
        self.comboBoxT2.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxT2, 1, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 14, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 9, 0, 1, 1)

        self.comboBoxLKNEM = QComboBox(self.groupBox)
        self.comboBoxLKNEM.setObjectName(u"comboBoxLKNEM")
        self.comboBoxLKNEM.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLKNEM, 10, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout.addWidget(self.label_24, 10, 2, 1, 1)

        self.comboBoxRPSI = QComboBox(self.groupBox)
        self.comboBoxRPSI.setObjectName(u"comboBoxRPSI")
        self.comboBoxRPSI.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRPSI, 6, 3, 1, 1)

        self.comboBoxLTIB = QComboBox(self.groupBox)
        self.comboBoxLTIB.setObjectName(u"comboBoxLTIB")
        self.comboBoxLTIB.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLTIB, 12, 1, 1, 1)

        self.comboBoxSACR = QComboBox(self.groupBox)
        self.comboBoxSACR.setObjectName(u"comboBoxSACR")
        self.comboBoxSACR.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxSACR, 4, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 11, 0, 1, 1)

        self.comboBoxLKNE = QComboBox(self.groupBox)
        self.comboBoxLKNE.setObjectName(u"comboBoxLKNE")
        self.comboBoxLKNE.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLKNE, 9, 1, 1, 1)

        self.comboBoxLPSI = QComboBox(self.groupBox)
        self.comboBoxLPSI.setObjectName(u"comboBoxLPSI")
        self.comboBoxLPSI.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLPSI, 6, 1, 1, 1)

        self.comboBoxLHEE = QComboBox(self.groupBox)
        self.comboBoxLHEE.setObjectName(u"comboBoxLHEE")
        self.comboBoxLHEE.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLHEE, 15, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.comboBoxLKAX = QComboBox(self.groupBox)
        self.comboBoxLKAX.setObjectName(u"comboBoxLKAX")
        self.comboBoxLKAX.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLKAX, 11, 1, 1, 1)

        self.comboBoxRASI = QComboBox(self.groupBox)
        self.comboBoxRASI.setObjectName(u"comboBoxRASI")
        self.comboBoxRASI.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRASI, 5, 3, 1, 1)

        self.comboBoxLTHI = QComboBox(self.groupBox)
        self.comboBoxLTHI.setObjectName(u"comboBoxLTHI")
        self.comboBoxLTHI.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLTHI, 7, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)

        self.comboBoxLANK = QComboBox(self.groupBox)
        self.comboBoxLANK.setObjectName(u"comboBoxLANK")
        self.comboBoxLANK.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLANK, 13, 1, 1, 1)

        self.label_25 = QLabel(self.groupBox)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout.addWidget(self.label_25, 11, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)

        self.comboBoxC7 = QComboBox(self.groupBox)
        self.comboBoxC7.setObjectName(u"comboBoxC7")
        self.comboBoxC7.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxC7, 0, 1, 1, 1)

        self.comboBoxLPAT = QComboBox(self.groupBox)
        self.comboBoxLPAT.setObjectName(u"comboBoxLPAT")
        self.comboBoxLPAT.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLPAT, 8, 1, 1, 1)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout.addWidget(self.label_23, 9, 2, 1, 1)

        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout.addWidget(self.label_19, 5, 2, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 6, 2, 1, 1)

        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout.addWidget(self.label_21, 7, 2, 1, 1)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 15, 0, 1, 1)

        self.label_30 = QLabel(self.groupBox)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout.addWidget(self.label_30, 16, 2, 1, 1)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 16, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 10, 0, 1, 1)

        self.label_29 = QLabel(self.groupBox)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout.addWidget(self.label_29, 15, 2, 1, 1)

        self.comboBoxMAN = QComboBox(self.groupBox)
        self.comboBoxMAN.setObjectName(u"comboBoxMAN")
        self.comboBoxMAN.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxMAN, 3, 1, 1, 1)

        self.label_28 = QLabel(self.groupBox)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout.addWidget(self.label_28, 14, 2, 1, 1)

        self.comboBoxLMED = QComboBox(self.groupBox)
        self.comboBoxLMED.setObjectName(u"comboBoxLMED")
        self.comboBoxLMED.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLMED, 14, 1, 1, 1)

        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout.addWidget(self.label_22, 8, 2, 1, 1)

        self.comboBoxLTOE = QComboBox(self.groupBox)
        self.comboBoxLTOE.setObjectName(u"comboBoxLTOE")
        self.comboBoxLTOE.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLTOE, 16, 1, 1, 1)

        self.comboBoxRTHI = QComboBox(self.groupBox)
        self.comboBoxRTHI.setObjectName(u"comboBoxRTHI")
        self.comboBoxRTHI.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRTHI, 7, 3, 1, 1)

        self.label_27 = QLabel(self.groupBox)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout.addWidget(self.label_27, 13, 2, 1, 1)

        self.comboBoxLASI = QComboBox(self.groupBox)
        self.comboBoxLASI.setObjectName(u"comboBoxLASI")
        self.comboBoxLASI.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxLASI, 5, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 12, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 13, 0, 1, 1)

        self.label_26 = QLabel(self.groupBox)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout.addWidget(self.label_26, 12, 2, 1, 1)

        self.comboBoxRPAT = QComboBox(self.groupBox)
        self.comboBoxRPAT.setObjectName(u"comboBoxRPAT")
        self.comboBoxRPAT.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRPAT, 8, 3, 1, 1)

        self.comboBoxRKNE = QComboBox(self.groupBox)
        self.comboBoxRKNE.setObjectName(u"comboBoxRKNE")
        self.comboBoxRKNE.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRKNE, 9, 3, 1, 1)

        self.comboBoxRKNEM = QComboBox(self.groupBox)
        self.comboBoxRKNEM.setObjectName(u"comboBoxRKNEM")
        self.comboBoxRKNEM.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRKNEM, 10, 3, 1, 1)

        self.comboBoxRKAX = QComboBox(self.groupBox)
        self.comboBoxRKAX.setObjectName(u"comboBoxRKAX")
        self.comboBoxRKAX.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRKAX, 11, 3, 1, 1)

        self.comboBoxRTIB = QComboBox(self.groupBox)
        self.comboBoxRTIB.setObjectName(u"comboBoxRTIB")
        self.comboBoxRTIB.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRTIB, 12, 3, 1, 1)

        self.comboBoxRANK = QComboBox(self.groupBox)
        self.comboBoxRANK.setObjectName(u"comboBoxRANK")
        self.comboBoxRANK.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRANK, 13, 3, 1, 1)

        self.comboBoxRMED = QComboBox(self.groupBox)
        self.comboBoxRMED.setObjectName(u"comboBoxRMED")
        self.comboBoxRMED.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRMED, 14, 3, 1, 1)

        self.comboBoxRHEE = QComboBox(self.groupBox)
        self.comboBoxRHEE.setObjectName(u"comboBoxRHEE")
        self.comboBoxRHEE.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRHEE, 15, 3, 1, 1)

        self.comboBoxRTOE = QComboBox(self.groupBox)
        self.comboBoxRTOE.setObjectName(u"comboBoxRTOE")
        self.comboBoxRTOE.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxRTOE, 16, 3, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonImport = QPushButton(MarkerSetDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout.addWidget(self.pushButtonImport)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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
        self.label_6.setText(QCoreApplication.translate("MarkerSetDialog", u"LASI:", None))
        self.label_15.setText(QCoreApplication.translate("MarkerSetDialog", u"LMED:", None))
        self.label_10.setText(QCoreApplication.translate("MarkerSetDialog", u"LKNE:", None))
        self.label_4.setText(QCoreApplication.translate("MarkerSetDialog", u"MAN:", None))
        self.label_24.setText(QCoreApplication.translate("MarkerSetDialog", u"RKNEM:", None))
        self.label_12.setText(QCoreApplication.translate("MarkerSetDialog", u"LKAX:", None))
        self.label_7.setText(QCoreApplication.translate("MarkerSetDialog", u"LPSI:", None))
        self.label_2.setText(QCoreApplication.translate("MarkerSetDialog", u"T2:", None))
        self.label_8.setText(QCoreApplication.translate("MarkerSetDialog", u"LTHI:", None))
        self.label_25.setText(QCoreApplication.translate("MarkerSetDialog", u"RKAX:", None))
        self.label_5.setText(QCoreApplication.translate("MarkerSetDialog", u"SACR:", None))
        self.label_9.setText(QCoreApplication.translate("MarkerSetDialog", u"LPAT:", None))
        self.label_23.setText(QCoreApplication.translate("MarkerSetDialog", u"RKNE:", None))
        self.label_19.setText(QCoreApplication.translate("MarkerSetDialog", u"RASI:", None))
        self.label_20.setText(QCoreApplication.translate("MarkerSetDialog", u"RPSI:", None))
        self.label_21.setText(QCoreApplication.translate("MarkerSetDialog", u"RTHI:", None))
        self.label_16.setText(QCoreApplication.translate("MarkerSetDialog", u"LHEE:", None))
        self.label_30.setText(QCoreApplication.translate("MarkerSetDialog", u"RTOE:", None))
        self.label_17.setText(QCoreApplication.translate("MarkerSetDialog", u"LTOE:", None))
        self.label.setText(QCoreApplication.translate("MarkerSetDialog", u"C7:", None))
        self.label_11.setText(QCoreApplication.translate("MarkerSetDialog", u"LKNEM:", None))
        self.label_29.setText(QCoreApplication.translate("MarkerSetDialog", u"RHEE:", None))
        self.label_28.setText(QCoreApplication.translate("MarkerSetDialog", u"RMED:", None))
        self.label_22.setText(QCoreApplication.translate("MarkerSetDialog", u"RPAT:", None))
        self.label_27.setText(QCoreApplication.translate("MarkerSetDialog", u"RANK:", None))
        self.label_3.setText(QCoreApplication.translate("MarkerSetDialog", u"T10:", None))
        self.label_13.setText(QCoreApplication.translate("MarkerSetDialog", u"LTIB:", None))
        self.label_14.setText(QCoreApplication.translate("MarkerSetDialog", u"LANK:", None))
        self.label_26.setText(QCoreApplication.translate("MarkerSetDialog", u"RTIB:", None))
        self.pushButtonImport.setText(QCoreApplication.translate("MarkerSetDialog", u"Import", None))
        self.pushButtonSave.setText(QCoreApplication.translate("MarkerSetDialog", u"Save", None))
    # retranslateUi

