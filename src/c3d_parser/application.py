
import sys

from PySide6.QtWidgets import QApplication

from c3d_parser.view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Auckland Bioengineering Institute")
    app.setApplicationName("C3D Parser")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
