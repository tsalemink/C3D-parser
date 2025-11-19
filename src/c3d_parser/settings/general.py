
import os
import sys
import shutil

from PySide6 import QtCore
from PySide6.QtNetwork import QLocalSocket, QLocalServer

from c3d_parser import __version__


APPLICATION_NAME = 'C3D-Parser'
ORGANISATION_NAME = 'Auckland Bioengineering Institute'
VERSION = __version__

DEFAULT_STYLE_SHEET = ''
INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'

script_directory = os.path.dirname(os.path.abspath(__file__))
internal_maps_dir = os.path.join(script_directory, 'marker_maps')


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


def is_frozen():
    return getattr(sys, 'frozen', False)


def get_marker_maps_dir():
    return get_app_directory('marker_sets')


def setup_marker_maps_dir():
    maps_directory = get_marker_maps_dir()
    if not os.listdir(maps_directory):
        _copy_marker_maps(maps_directory)
    return maps_directory


def _copy_marker_maps(target_directory):
    for file_name in os.listdir(internal_maps_dir):
        source = os.path.join(internal_maps_dir, file_name)
        destination = os.path.join(target_directory, file_name)
        if os.path.isfile(source):
            shutil.copy2(source, destination)
