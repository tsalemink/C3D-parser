
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidget, QMenu, QStyledItemDelegate
from PySide6.QtGui import QAction


class CustomListWidget(QListWidget):
    include_trial = Signal(str)
    exclude_trial = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegate(CustomDelegate())

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            if (item.flags() & Qt.ItemIsEnabled):
                menu = QMenu(self)

                static_action = QAction("Static", self)
                dynamic_action = QAction("Dynamic", self)
                static_action.triggered.connect(lambda: self.set_item_category(item, "Static"))
                dynamic_action.triggered.connect(lambda: self.set_item_category(item, "Dynamic"))

                include_trial_action = QAction("Include Trial", self)
                exclude_trial_action = QAction("Exclude Trial", self)
                include_trial_action.triggered.connect(lambda: self.include_trial.emit(item.text()))
                exclude_trial_action.triggered.connect(lambda: self.exclude_trial.emit(item.text()))

                menu.addAction(static_action)
                menu.addAction(dynamic_action)
                menu.addSeparator()
                menu.addAction(include_trial_action)
                menu.addAction(exclude_trial_action)

                menu.exec_(event.globalPos())

    def set_item_category(self, item, category):
        item.setData(Qt.UserRole, category)
        self.viewport().update()


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        painter.save()
        category = index.data(Qt.UserRole)

        if category == "Static":
            painter.setPen(Qt.darkBlue)
        else:
            painter.setPen(Qt.darkMagenta)

        rect = option.rect.adjusted(0, 0, -5, 0)
        painter.drawText(rect, Qt.AlignRight, category)
        painter.restore()
