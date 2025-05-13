
import logging
import traceback

from functools import wraps
from PySide6.QtWidgets import QMessageBox

from c3d_parser.core.c3d_parser import ParserError, CancelException
from c3d_parser.settings.general import APPLICATION_NAME


logger = logging.getLogger(APPLICATION_NAME)


def handle_runtime_error(f):
    """
    Decorator for gui actions so that all exceptions raised will notify the user.
    """
    @wraps(f)
    def do_runtime_error(self, *a, **kw):
        try:
            return f(self, *a, **kw)

        except ParserError as e:
            logger.error(e)
            QMessageBox.critical(self, 'Error', f'ParserError: {e}')

        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f'Unexpected error: {e}\n{tb}')
            QMessageBox.critical(self, 'Error', f'Unexpected error: {e}\n{tb}')

    return do_runtime_error
