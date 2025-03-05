
from PySide6 import QtWidgets

from c3d_parser.view.ui.ui_subject_info_dialog import Ui_SubjectInfoDialog


class SubjectInfoDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SubjectInfoDialog, self).__init__(parent)
        self._ui = Ui_SubjectInfoDialog()
        self._ui.setupUi(self)

    def subject_height(self):
        return self._ui.doubleSpinBoxHeight.value()

    def subject_weight(self):
        return self._ui.doubleSpinBoxWeight.value()
