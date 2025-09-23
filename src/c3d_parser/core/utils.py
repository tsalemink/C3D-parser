
import os

from c3d_parser.settings.logging import logger


def clear_directory(folder_path):
    """
    `shutil.rmtree` fails for OneDrive directories.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    permission_error_occurred = False

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except PermissionError as e:
                logger.error(e)
                permission_error_occurred = True

    if permission_error_occurred:
        logger.warn(f"You may need to delete the files listed above manually.")
