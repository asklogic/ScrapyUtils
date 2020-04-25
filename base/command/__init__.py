import click
import signal
import sys
import os

from abc import abstractmethod

from base.core import *
from base.exception import CommandExit
from base.log import Wrapper as log
from base.log import set_syntax, set_line

from ._base import Command, ComponentMixin

# registered command

from .check import Check
from .generate import Generate
from .single import Single
from .thread_ import Thread

command_map = {
    'check': Check,
    'generate': Generate,
    'single': Single,
    'thread': Thread,
}


# function

def trigger(command_name: str, **kwargs):
    # get command class
    command: ComponentMixin or Command = command_map[command_name]

    set_syntax(command.syntax())

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGTERM, command.signal_callback)
    signal.signal(signal.SIGINT, command.signal_callback)
    log.info('starting command {}'.format(command.__name__))

    # collect. -> core.collect
    if command.do_collect:
        collect_scheme_preload(kwargs.get('scheme'))

        if kwargs.get('confirm'):
            input('Press any key to continue.')

        collect_scheme_initial()

        command.suits = get_suits()
        command.tasks = get_tasks()
        command.pipeline = get_pipeline()
        command.config = get_config()
        command.proxy = get_proxy()

        # TODO: proxy start.
        if command.proxy:
            command.proxy.start()

    try:
        log.debug('command running...')

        command.run(kwargs)
        log.debug('command finish.')

    except CommandExit as ex:
        log.info('Command Exit.')

    except Exception as e:
        command.failed()
        log.exception('Command', e)

    finally:
        log.info('command exiting...')

        command.exit()
        log.info('command exited.')

    sys_exit(command.exitcode)


def sys_exit(exitcode: int):
    sys.exit(exitcode)


# command's group
@click.group()
def cli():
    pass


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
def thread(scheme: str, path, line):
    trigger('thread', scheme=scheme, path=path, line=line, confirm=True)


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
def single(scheme: str, path):
    trigger('single', scheme=scheme, path=path)


@click.command()
@click.argument('scheme')
def generate(scheme: str):
    trigger('generate', scheme=scheme, confirm=True)


@click.command()
@click.argument('target')
def check(target: str):
    trigger('check', target=target)


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
cli.add_command(check)
