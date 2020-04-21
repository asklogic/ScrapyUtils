import logging
import linecache

from os.path import basename
from logging import DEBUG, INFO, WARNING, ERROR

# global

line = 3

# ScrapyUtil Default logger
sh = logging.StreamHandler()
sh.setLevel(DEBUG)
sh.setFormatter(logging.Formatter(r"%(asctime)s [%(levelname)s]|%(message)s", r'%m/%d %H:%M:%S'))

logger = logging.getLogger('Log')
logger.setLevel(DEBUG)
logger.addHandler(sh)


class Wrapper:
    log = logger
    syntax: str = '[Log]'
    line: int = 3

    @classmethod
    def _msg(cls, msg, *args):
        component = ' - '.join(args)
        component_msg = ''.join(['<', component, '>']) if component else ''
        message = ' '.join((x for x in (cls.syntax, component_msg, msg) if x))
        return message

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.log.info(msg=cls._msg(msg, *args), **kwargs)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.log.debug(msg=cls._msg(msg, *args), **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls.log.warning(msg=cls._msg(msg, *args), **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.log.error(msg=cls._msg(msg, *args), **kwargs)

    @classmethod
    def exception(cls, component_name: str, exception: Exception, line: int = None):
        if not line:
            line = cls.line

        exception_name = exception.__class__.__name__
        component_name = '<{}>'.format(component_name)
        message = ' '.join([cls.syntax, component_name, exception_name,'-' ,str(exception)])
        cls.log.error(message)

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
                cls.log.debug(msg)


def set_syntax(syntax):
    Wrapper.syntax = syntax


def set_line(line):
    Wrapper.line = line


# class ThreadLog(Wrapper):
#
#     @classmethod
#     def syntax(self):
#         return '[Thread]'


default = Wrapper
current = Wrapper

if __name__ == '__main__':
    print('logger test!')
    #
    # StatusLog.info('info')
    # StatusLog.warning('warning')
    # StatusLog.debug('debug')
    # StatusLog.error("error")

    # ActLog.error("[Scheme] TestAction failed")

    Wrapper.info('info', 'Core', 'Check')
    Wrapper.info('info', 'Core')
    Wrapper.info('info')

    set_syntax('[Thread]')

    Wrapper.info('thread')
    Wrapper.info('thread', 'Core')
