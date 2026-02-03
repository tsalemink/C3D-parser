
import sys
import ctypes

from c3d_parser.settings.general import (set_applications_settings, application_instance_exists,
    start_application_server, setup_marker_maps_dir)
from c3d_parser.settings.logging import initialise_logger, filter_c3d_warnings


def main():
    if sys.platform == 'win32':
        my_app_id = 'Motion_Connect.C3D_Parser'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    from c3d_parser.splashscreen import SplashScreen
    splash = SplashScreen()
    splash.show()

    splash.showMessage("Loading settings ...", 5)
    set_applications_settings(app)
    setup_marker_maps_dir()

    # Prevent multiple application instances.
    if application_instance_exists():
        print("C3D-Parser instance is already running.")
        sys.exit(1)
    app_server = start_application_server()

    splash.showMessage('Initialising logger ...', 20)
    initialise_logger()
    filter_c3d_warnings()

    splash.showMessage('Importing dependencies ...', 40)
    from c3d_parser.view.main_window import MainWindow
    splash.showMessage('Creating main window ...', 80)
    window = MainWindow()
    splash.showMessage('Showing main window ...', 90)
    window.show()

    splash.showMessage('Load complete ...', 100)
    splash.finish(window)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
