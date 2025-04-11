# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'marker_set_import_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MarkerSetImportDialog(object):
    def setupUi(self, MarkerSetImportDialog):
        if not MarkerSetImportDialog.objectName():
            MarkerSetImportDialog.setObjectName(u"MarkerSetImportDialog")
        MarkerSetImportDialog.resize(360, 120)
        self.verticalLayout = QVBoxLayout(MarkerSetImportDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(MarkerSetImportDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_2)

        self.comboBoxMarkerSet = QComboBox(self.groupBox)
        self.comboBoxMarkerSet.setObjectName(u"comboBoxMarkerSet")

        self.horizontalLayout.addWidget(self.comboBoxMarkerSet)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(MarkerSetImportDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(MarkerSetImportDialog)
        self.buttonBox.accepted.connect(MarkerSetImportDialog.accept)
        self.buttonBox.rejected.connect(MarkerSetImportDialog.reject)

        QMetaObject.connectSlotsByName(MarkerSetImportDialog)
    # setupUi

    def retranslateUi(self, MarkerSetImportDialog):
        MarkerSetImportDialog.setWindowTitle(QCoreApplication.translate("MarkerSetImportDialog", u"Import Marker Set", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("MarkerSetImportDialog", u"Import markers mappings from existing marker set.", None))
        self.label_2.setText(QCoreApplication.translate("MarkerSetImportDialog", u"Marker Set:", None))
    # retranslateUi

