import logging
import prettytable

from logging import DEBUG, INFO, WARNING, ERROR
from logging import Logger, getLogger, StreamHandler, Formatter

from linecache import getlines

# pretty table
tb = prettytable.PrettyTable(border=False)
tb.field_names = ['line', 'content']


def error_lines(logger, message: str, exception: Exception):
    message = ' - '.join((message, str(exception.__class__.__name__)))
    tb.clear_rows()

    current_traceback = exception.__traceback__

    # forward to the bottom
    while current_traceback.tb_next:
        current_traceback = current_traceback.tb_next

    current_content = getlines(current_traceback.tb_frame.f_code.co_filename)
    for index, line_content in enumerate(current_content[
                                         current_traceback.tb_frame.f_lineno - 1:current_traceback.tb_frame.f_lineno + 1]):
        tb.add_row((index, line_content.strip()))
    logger.error('\n'.join((message, tb.get_string())))


def set_stream_logger(logger_name: str, formatter: Formatter):
    """设置通用日志"""
    logger = getLogger(logger_name)
    logger.setLevel(DEBUG)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(DEBUG)

    logger.addHandler(stream_handler)


common_loggers = ['common', 'ScrapyUtils']
"""通用日志"""

command_loggers = ['command', 'execute', 'generate', 'download', 'parsing']
"""命令日志列表"""
command_format = Formatter('%(asctime)s [%(name)s] (%(levelname)s): %(message)s', r'%Y/%m/%d %H:%M:%S')
"""命令日志格式"""

# 设置命令日志格式, 通用日志
[set_stream_logger(logger_name, command_format) for logger_name in command_loggers + common_loggers]

core_loggers = ['preload', 'load', 'scrape', 'persist', 'pipeline', ]
"""爬虫核心的日志列表"""
core_format = Formatter('%(asctime)s [%(levelname)s] <%(name)s @ %(threadName)s>: %(message)s', r'%H:%M:%S')
"""爬虫核心的日志格式"""

[set_stream_logger(logger_name, core_format) for logger_name in core_loggers]

component_loggers = ['component']
"""组件以及其他通用组件的日志"""
component_format = Formatter('%(asctime)s [%(levelname)s] <%(name)s> in %(funcName)s: %(message)s', r'%H:%M:%S')
"""组件的日志格式"""

[set_stream_logger(logger_name, component_format) for logger_name in component_loggers]

if __name__ == '__main__':
    print('logger test!')

    getLogger('command').info('infos')
    getLogger('generate').debug('debug')

    getLogger('preload').debug('debug')
    getLogger('load').info('infos')
    getLogger('scrape').error('error')

    getLogger('component').error('error')
