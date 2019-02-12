import logging


def setup_logger(logger_name, log_file, level=logging.INFO):
    multi_logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    multi_logger.setLevel(level)
    multi_logger.addHandler(file_handler)
    multi_logger.addHandler(stream_handler)


setup_logger('info', r'../logger/logs/info.log', level=logging.INFO)
setup_logger('debug', r'../logger/logs/debug.log', level=logging.DEBUG)
setup_logger('error', r'../logger/logs/error.log', level=logging.ERROR)
info = logging.getLogger('info').info
debug = logging.getLogger('debug').debug
error = logging.getLogger('error').error
