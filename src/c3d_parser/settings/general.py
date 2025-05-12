
import os

from PySide6 import QtCore
from PySide6.QtNetwork import QLocalSocket, QLocalServer


APPLICATION_NAME = 'C3D-Parser'
ORGANISATION_NAME = 'Auckland Bioengineering Institute'

DEFAULT_STYLE_SHEET = ''
INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'


def set_applications_settings(app):
    app.setApplicationName(APPLICATION_NAME)
    app.setOrganizationName(ORGANISATION_NAME)
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.Format.IniFormat)


def get_data_directory():
    settings = QtCore.QSettings()
    fn = settings.fileName()

    return os.path.dirname(fn)


def get_app_directory(name):
    app_dir = get_data_directory()
    name_dir = os.path.join(app_dir, name)

    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    return name_dir


def application_instance_exists():
    socket = QLocalSocket()
    socket.connectToServer(APPLICATION_NAME)
    if socket.waitForConnected(100):
        socket.close()
        return True
    return False


def start_application_server():
    server = QLocalServer()
    try:
        QLocalServer.removeServer(APPLICATION_NAME)
    except:
        pass
    server.listen(APPLICATION_NAME)
    return server
