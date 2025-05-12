
import os
import logging

from c3d_parser.settings.general import APPLICATION_NAME, get_app_directory


logger = logging.getLogger(APPLICATION_NAME)


def get_log_directory():
    return get_app_directory('logs')


def initialise_logger():
    log_file = os.path.join(get_log_directory(), 'c3d_parser.log')

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d/%m/%Y - %H:%M:%S')

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y - %H:%M:%S')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
