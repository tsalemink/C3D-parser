import c3d_parser.splash_rc

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QSplashScreen, QProgressBar
from PySide6.QtGui import QPixmap, QFont, QPen, QColor


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self._message = ''
        pixmap = QPixmap(":/c3d_parser/splash.png")
        self.setPixmap(pixmap)

        self._font = QFont()
        self._font.setFamily('Arial')
        self._font.setPixelSize(16)
        self.setFont(self._font)

        self._margin = int(20 * self.devicePixelRatioF())
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setStyleSheet("QProgressBar { background: transparent; }")
        self._progress_bar.setGeometry(self._margin, 0, pixmap.width() - (2 * self._margin), 8)
        self._bar_position = QPoint(self._margin, pixmap.height() - self._margin - 4)
        self._text_y = pixmap.height() - int(60 * self.devicePixelRatioF())
        self._text_height = int(30 * self.devicePixelRatioF())

    def drawContents(self, painter):
        self._progress_bar.render(painter, self._bar_position)
        super(SplashScreen, self).drawContents(painter)

        pen = QPen()
        pen.setColor(QColor(100, 100, 100))
        painter.setPen(pen)
        painter.setFont(self._font)
        painter.drawText(0, self._text_y, self.width(), self._text_height, Qt.AlignmentFlag.AlignCenter, self._message)

    def showMessage(self, message, progress=0, alignment=Qt.AlignmentFlag.AlignCenter, color=Qt.GlobalColor.black):
        self._progress_bar.setValue(progress)
        self._message = message
        super(SplashScreen, self).showMessage('  ', Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
