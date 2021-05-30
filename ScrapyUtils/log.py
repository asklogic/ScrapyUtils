import logging
import linecache
import prettytable

from logging import DEBUG, INFO, WARNING, ERROR
from logging import Logger, getLogger, StreamHandler, Formatter

from linecache import getlines

common_time_format = '%m.%d %H:%M:%S'
common_format_str = r'%(asctime)s [%(levelname)s] %(message)s'

common_format = logging.Formatter(r'%(asctime)s [%(levelname)s] %(message)s', r'%H:%M:%S')
basic_format = logging.Formatter(r" * %(message)s", r'%H:%M:%S')

# pretty table
tb = prettytable.PrettyTable(border=False)
"""common prettytable"""

tb.field_names = ['line', 'content']


def error_lines(logger, message: str, exception: Exception):
    message = ' - '.join((message, str(exception.__class__.__name__)))
    tb.clear_rows()

    current_traceback = exception.__traceback__

    # forward to
    while current_traceback.tb_next:
        current_traceback = current_traceback.tb_next

    current_content = getlines(current_traceback.tb_frame.f_code.co_filename)
    for index, line_content in enumerate(current_content[
                                         current_traceback.tb_frame.f_lineno - 1:current_traceback.tb_frame.f_lineno + 1]):
        tb.add_row((index, line_content.strip()))
    logger.error('\n'.join((message, tb.get_string())))


def set_log_file_name(file_name):
    """
    Args:
        file_name:
    """
    logger = common.log
    if not '.out' in file_name:
        file_name = file_name + '.out'
    fh = logging.FileHandler(filename=file_name)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(r"%(asctime)s [%(levelname)s]|%(message)s", r'%H:%M:%S'))

    logger.addHandler(fh)


def build_defalut_logger(logger_name: str,
                         format_str: str = common_format_str,
                         time_format: str = common_time_format,
                         level=DEBUG) -> Logger:
    logger = getLogger(logger_name)
    logger.setLevel(level)

    stream = StreamHandler()
    stream.setFormatter(Formatter(format_str, time_format))
    stream.setLevel(level)

    # fs = FileHandler()

    logger.addHandler(stream)

    return logger


build_defalut_logger('core', format_str='(%(levelname)s) %(message)s', time_format='%H:%M:%S')
build_defalut_logger('base', format_str=' * %(message)s', time_format='%H:%M:%S')

build_defalut_logger('scheme_state', format_str="[%(state)s in '%(method)s'] - %(message)s", time_format='%H:%M:%S')
build_defalut_logger('scheme_load', format_str='(%(levelname)s) %(message)s', time_format='%H:%M:%S')
# build_defalut_logger('Common')

common = getLogger('core')
basic = getLogger('base')

if __name__ == '__main__':
    print('logger test!')

    common.info('hello')
    common.info('scraper', 'System')
    common.info('listener', 'System')
    common.info('success. temp text')
    common.info('failed. temp text')

    basic.info('basic')
    basic.info('port: 1234')
    basic.info('output: /base/log.py')
