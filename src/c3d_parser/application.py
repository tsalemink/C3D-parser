
import sys
import ctypes

from PySide6.QtWidgets import QApplication

from c3d_parser.view.main_window import MainWindow
from c3d_parser.settings.general import (set_applications_settings, application_instance_exists,
    start_application_server, setup_marker_maps_dir)
from c3d_parser.settings.logging import initialise_logger, filter_c3d_warnings


def main():
    if sys.platform == 'win32':
        my_app_id = 'Motion_Connect.C3D_Parser'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    app = QApplication(sys.argv)
    set_applications_settings(app)
    setup_marker_maps_dir()

    # Prevent multiple application instances.
    if application_instance_exists():
        print("C3D-Parser instance is already running.")
        sys.exit(1)
    app_server = start_application_server()

    initialise_logger()
    filter_c3d_warnings()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
