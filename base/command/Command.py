from typing import List
from abc import abstractmethod

from logging import DEBUG, WARN, ERROR, INFO
from base import core
import click, time
import sys
from base.exception import CmdRunException
from base.libs.setting import Setting
from base.log import act
import logging
import signal
from os.path import basename
import linecache


class Command(object):
    do_collect: bool = True
    exitcode: int = 0
    interrupt: bool = False

    def syntax(self) -> str:
        return '[Command]'

    def __init__(self):
        self.exitcode: int = 0
        self.interrupt: bool = False

    @property
    def log(self, **kwargs):
        # TODO: move to log.py
        class inner_log:
            @classmethod
            def info(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.info(message)

            @classmethod
            def warning(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.warning(message)

            @classmethod
            def error(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.error(message)

            @classmethod
            def debug(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.debug(message)

            @classmethod
            def exception(cls, component_name: str, exception: Exception):
                exception_name = exception.__class__.__name__
                component_name = '<{}>'.format(component_name)
                message = ' '.join([self.syntax(), component_name, 'Except Exception:', exception_name])
                act.error(message)

                current = exception.__traceback__

                # TODO: refact
                current_code = current.tb_frame.f_code

                while not basename(current_code.co_filename) in ('action.py', 'parse.py') and current.tb_next:
                    current = current.tb_next
                    current_code = current.tb_frame.f_code
                lines = [linecache.getline(current_code.co_filename, current.tb_lineno + x,
                                           current.tb_frame.f_globals).replace('\n', '')
                         for x in
                         (-2, -1, 0)]

                for line in (-2, -1, 0):
                    if not lines[2 + line].strip():
                        continue
                    msg = ''.join(('Line: ', str(current.tb_lineno + line), ' |', lines[2 + line]))
                    act.debug(msg)

        return inner_log

    @abstractmethod
    def signal_callback(self, signum, frame):
        pass

    def collect(self, scheme_name: str):
        # TODO
        pass

    @abstractmethod
    def options(self, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def failed(self):
        pass

    @abstractmethod
    def exit(self):
        pass




def sys_exit(exitcode: int):
    pass


def trigger(command_name: str, **kwargs):
    # get command class
    command: Command = get_command(command_name)

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGINT, command.signal_callback)
    signal.signal(signal.SIGTERM, command.signal_callback)

    # collect
    # command.collect(kwargs.get('target'))

    try:
        command.options(**kwargs)

        command.run()

    except Exception as e:
        command.failed()
        command.log.exception('Command', e)

    finally:
        command.exit()

    sys_exit(command.exitcode)


def get_command(command_name: str) -> Command:
    from base.command import registered

    # TODO: WTF?
    select_command = None
    for command in registered:
        if command_name in str(command):
            command_class = getattr(command, command_name.capitalize())
            select_command = command_class()
            break

    if not select_command:
        act.error('can not found registered Command %s' % command_name)
        sys.exit(0)

    return select_command


@click.group()
def cli():
    pass


@click.command()
@click.argument('target')
def thread(target: str):
    trigger('thread', target=target)
    # thread_run(target)
    # pass


@click.command()
@click.argument('target')
def single(target: str):
    trigger('single', target=target)


@click.command()
@click.argument('target')
def generate(target: str):
    # gen(target)
    trigger('generate', target=target)


@click.command()
@click.argument('target')
def check(target: str):
    trigger('check', target=target)


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
cli.add_command(check)
