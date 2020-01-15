import click
import signal
import sys
import os

from abc import abstractmethod

from base.core import *
from base.exception import CommandExit
from base.log import Wrapper as log


def get_command(command_name: str):
    module = __import__('base.command.' + command_name, fromlist=['base', 'command'])

    command = getattr(module, command_name.capitalize())

    return command()


class Command(object):
    exitcode: int = 0
    interrupt: bool = False

    do_collect: bool = True

    def syntax(self) -> str:
        return '[Command]'

    def __init__(self):
        self.exitcode: int = 0
        self.interrupt: bool = False
        self.do_collect = True

    @abstractmethod
    def signal_callback(self, signum, frame):
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
    sys.exit(exitcode)


def trigger(command_name: str, **kwargs):
    # get command class
    command: Command = get_command(command_name)

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGTERM, command.signal_callback)
    signal.signal(signal.SIGINT, command.signal_callback)

    # collect. -> core.collect
    if command.do_collect:
        collect_scheme(kwargs.get('scheme'))
        log.info('collected scheme:{}'.format(kwargs.get('scheme')))

    try:

        command.options(**kwargs)
        log.info('options finish.')

        command.run()
        log.info('run finish.')

    except CommandExit as ex:
        pass
    except Exception as e:
        command.failed()
        log.exception('Command', e)

    finally:
        command.exit()
        log.info('command exited.')

    sys_exit(command.exitcode)


# command's group
@click.group()
def cli():
    pass


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
def command_thread(scheme: str, path, line):
    trigger('thread', scheme=scheme, path=path, line=line)


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
def command_single(scheme: str, path):
    trigger('single', scheme=scheme, path=path)


@click.command()
@click.argument('scheme')
def command_generate(scheme: str):
    trigger('generate', scheme=scheme)


@click.command()
@click.argument('target')
def command_check(target: str):
    trigger('check', target=target)


cli.add_command(command_thread)
cli.add_command(command_single)
cli.add_command(command_generate)
cli.add_command(command_check)
