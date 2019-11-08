from typing import List
from abc import abstractmethod

import click, time
import sys
import os
from base.log import logger, Wrapper
import signal


class Command(object):
    exitcode: int = 0
    interrupt: bool = False

    do_collect: bool = True

    def syntax(self) -> str:
        return '[Command]'

    def __init__(self):
        self.exitcode: int = 0
        self.interrupt: bool = False

    @property
    def log(self, **kwargs):
        class ThreadLogger(Wrapper):
            @classmethod
            def syntax(self):
                return '[Thread]'

        return ThreadLogger

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
    signal.signal(signal.SIGTERM, command.signal_callback)
    signal.signal(signal.SIGINT, command.signal_callback)

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
        logger.error('can not found registered Command %s' % command_name)
        sys.exit(0)

    return select_command


@click.group()
def cli():
    pass


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
def thread(scheme: str, path):
    trigger('thread', scheme=scheme, path=path)

    # thread_run(target)
    # pass


@click.command()
@click.argument('target')
def single(target: str):
    trigger('single', target=target)


@click.command()
@click.argument('scheme')
def generate(scheme: str):
    trigger('generate', scheme=scheme)


@click.command()
@click.argument('target')
def check(target: str):
    trigger('check', target=target)


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
cli.add_command(check)
