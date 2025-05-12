
import sys

from PySide6.QtWidgets import QApplication

from c3d_parser.view.main_window import MainWindow
from c3d_parser.settings.general import set_applications_settings, application_instance_exists, start_application_server


def main():
    app = QApplication(sys.argv)
    set_applications_settings(app)

    # Prevent multiple application instances.
    if application_instance_exists():
        print("C3D-Parser instance is already running.")
        sys.exit(1)
    app_server = start_application_server()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
