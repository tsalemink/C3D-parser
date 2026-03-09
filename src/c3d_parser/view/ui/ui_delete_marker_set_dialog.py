# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'delete_marker_set_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DeleteMarkerSetDialog(object):
    def setupUi(self, DeleteMarkerSetDialog):
        if not DeleteMarkerSetDialog.objectName():
            DeleteMarkerSetDialog.setObjectName(u"DeleteMarkerSetDialog")
        DeleteMarkerSetDialog.resize(400, 116)
        self.verticalLayout = QVBoxLayout(DeleteMarkerSetDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(DeleteMarkerSetDialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.comboBoxMarkerSet = QComboBox(self.groupBox)
        self.comboBoxMarkerSet.setObjectName(u"comboBoxMarkerSet")

        self.verticalLayout_2.addWidget(self.comboBoxMarkerSet)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonDelete = QPushButton(DeleteMarkerSetDialog)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")

        self.horizontalLayout.addWidget(self.pushButtonDelete)

        self.pushButtonClose = QPushButton(DeleteMarkerSetDialog)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(DeleteMarkerSetDialog)
        self.pushButtonClose.clicked.connect(DeleteMarkerSetDialog.accept)

        self.pushButtonClose.setDefault(True)


        QMetaObject.connectSlotsByName(DeleteMarkerSetDialog)
    # setupUi

    def retranslateUi(self, DeleteMarkerSetDialog):
        DeleteMarkerSetDialog.setWindowTitle(QCoreApplication.translate("DeleteMarkerSetDialog", u"Dialog", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("DeleteMarkerSetDialog", u"Select the marker set you would like to delete:", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("DeleteMarkerSetDialog", u"Delete", None))
        self.pushButtonClose.setText(QCoreApplication.translate("DeleteMarkerSetDialog", u"Close", None))
    # retranslateUi

