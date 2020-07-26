import logging
import linecache

from os.path import basename
from logging import DEBUG, INFO, WARNING, ERROR

common_format = logging.Formatter(r'%(asctime)s [%(levelname)s]|%(message)s', r'%H:%M:%S')
basic_format = logging.Formatter(r" * %(message)s", r'%H:%M:%S')


class LogWrapper:
    log: logging.Logger
    syntax: str
    line: int = 3

    def __init__(self, log, syntax='[Log]', line=3):
        """
        Args:
            log:
            syntax:
            line:
        """
        self.log = log
        self.syntax = syntax
        self.line = line

    def _msg(self, msg, *args):
        """
        Args:
            msg:
            *args:
        """
        component = ' - '.join(args)
        component_msg = ''.join(['<', component, '>']) if component else ''
        message = ' '.join((x for x in (self.syntax, component_msg, msg) if x))
        return message

    def info(self, msg, *args, **kwargs):
        """
        Args:
            msg:
            *args:
            **kwargs:
        """
        self.log.info(msg=self._msg(msg, *args), **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Args:
            msg:
            *args:
            **kwargs:
        """
        self.log.debug(msg=self._msg(msg, *args), **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Args:
            msg:
            *args:
            **kwargs:
        """
        self.log.warning(msg=self._msg(msg, *args), **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Args:
            msg:
            *args:
            **kwargs:
        """
        self.log.error(msg=self._msg(msg, *args), **kwargs)

    def exception(self, component_name: str, exception: Exception, line: int = None):
        """
        Args:
            component_name (str):
            exception (Exception):
            line (int):
        """
        if not line:
            line = self.line

        exception_name = exception.__class__.__name__
        component_name = '<{}>'.format(component_name)
        message = ' '.join([self.syntax, component_name, exception_name, '-', str(exception)])
        self.log.error(message)

        current = exception.__traceback__

        # TODO: refact
        current_code = current.tb_frame.f_code

        while not basename(current_code.co_filename) in ('action.py', 'parse.py') and current.tb_next:
            current = current.tb_next
            current_code = current.tb_frame.f_code
        lines = [linecache.getline(current_code.co_filename, current.tb_lineno + x,
                                   current.tb_frame.f_globals).replace('\n', '')
                 for x in
                 tuple(range(0, line * -1, -1))]

        for line_index in tuple(range(0, line * -1, -1)):
            if lines[line_index + line - 1].strip():
                msg = ''.join(
                    ('Line: ', str(current.tb_lineno - line_index - line), ' |', lines[line_index + line - 1]))
                self.log.debug(msg)


def set_syntax(syntax):
    """
    Args:
        syntax:
    """
    common.syntax = syntax


def set_line(line):
    """
    Args:
        line:
    """
    common.line = line


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


# build common
logger = logging.getLogger('common')
logger.setLevel(DEBUG)

sh = logging.StreamHandler()
sh.setLevel(DEBUG)
sh.setFormatter(common_format)
logger.addHandler(sh)

common = LogWrapper(logger)
common.syntax = '[Common]'

# build basic
logger = logging.getLogger('basic')
logger.setLevel(DEBUG)

sh = logging.StreamHandler()
sh.setLevel(DEBUG)
sh.setFormatter(basic_format)
logger.addHandler(sh)

basic = LogWrapper(logger)
basic.syntax = ''




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
