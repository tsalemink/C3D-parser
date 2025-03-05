# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'subject_info_dialog.ui'
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
    QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_SubjectInfoDialog(object):
    def setupUi(self, SubjectInfoDialog):
        if not SubjectInfoDialog.objectName():
            SubjectInfoDialog.setObjectName(u"SubjectInfoDialog")
        SubjectInfoDialog.resize(400, 200)
        self.verticalLayout = QVBoxLayout(SubjectInfoDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(SubjectInfoDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelHeight = QLabel(self.frame)
        self.labelHeight.setObjectName(u"labelHeight")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHeight.sizePolicy().hasHeightForWidth())
        self.labelHeight.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.labelHeight)

        self.doubleSpinBoxHeight = QDoubleSpinBox(self.frame)
        self.doubleSpinBoxHeight.setObjectName(u"doubleSpinBoxHeight")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxHeight.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxHeight.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxHeight.setMinimumSize(QSize(280, 0))
        self.doubleSpinBoxHeight.setMaximum(999.990000000000009)

        self.horizontalLayout.addWidget(self.doubleSpinBoxHeight)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelWeight = QLabel(self.frame_2)
        self.labelWeight.setObjectName(u"labelWeight")
        sizePolicy.setHeightForWidth(self.labelWeight.sizePolicy().hasHeightForWidth())
        self.labelWeight.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.labelWeight)

        self.doubleSpinBoxWeight = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBoxWeight.setObjectName(u"doubleSpinBoxWeight")
        sizePolicy1.setHeightForWidth(self.doubleSpinBoxWeight.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxWeight.setSizePolicy(sizePolicy1)
        self.doubleSpinBoxWeight.setMinimumSize(QSize(280, 0))
        self.doubleSpinBoxWeight.setMaximum(999.990000000000009)

        self.horizontalLayout_2.addWidget(self.doubleSpinBoxWeight)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(SubjectInfoDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SubjectInfoDialog)
        self.buttonBox.accepted.connect(SubjectInfoDialog.accept)
        self.buttonBox.rejected.connect(SubjectInfoDialog.reject)

        QMetaObject.connectSlotsByName(SubjectInfoDialog)
    # setupUi

    def retranslateUi(self, SubjectInfoDialog):
        SubjectInfoDialog.setWindowTitle(QCoreApplication.translate("SubjectInfoDialog", u"Subject Information", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("SubjectInfoDialog", u"Please enter the following subject information:", None))
        self.labelHeight.setText(QCoreApplication.translate("SubjectInfoDialog", u"Height (cm)", None))
        self.labelWeight.setText(QCoreApplication.translate("SubjectInfoDialog", u"Weight (kg)", None))
    # retranslateUi

