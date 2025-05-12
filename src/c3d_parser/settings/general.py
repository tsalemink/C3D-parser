
from PySide6 import QtCore


APPLICATION_NAME = 'C3D-Parser'
ORGANISATION_NAME = 'Auckland Bioengineering Institute'

DEFAULT_STYLE_SHEET = ''
INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'


def set_applications_settings(app):
    app.setApplicationName(APPLICATION_NAME)
    app.setOrganizationName(ORGANISATION_NAME)
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.Format.IniFormat)


def get_data_directory():
    settings = QSettings()
    fn = settings.fileName()

    return os.path.dirname(fn)


def _get_app_directory(name):
    app_dir = get_data_directory()
    name_dir = os.path.join(app_dir, name)

    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    return name_dir
