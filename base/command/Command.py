from typing import List
import os
from logging import DEBUG, WARN, ERROR, INFO
from abc import abstractmethod
from base.engine import thread_run, single_run
from base import core
import click
from base.generate.generator import generate as gen

from base.libs.setting import Setting
from base.log import act

PROJECT_PATH = os.path.dirname(os.getcwd())


class Command(object):
    require_target = False

    setting: Setting
    exitcode: int

    def syntax(self):
        return '[Command]'

    def log(self, msg, level=INFO, step=''):
        # TODO Level

        step = '<%s>' % step if step else step
        message = ' '.join((self.syntax(), step, msg))
        # message = ' '.join((x for x in (self.syntax(), step, msg) if x))
        act.log(level=level, msg=message)

    def __init__(self):
        self.setting = None
        self.exitcode = -1

    def build(self, **kwargs):
        if self.require_target:
            assert kwargs.get('target'), 'no target'

            target = kwargs.get('target')
            setting = core.build_setting(target)

            self.setting = setting

    @abstractmethod
    def run(self):
        pass

    def exit(self):
        pass


def get_command(command_name: str) -> Command:
    try:
        module = __import__('base.command.' + command_name, fromlist=['base', 'command'])

        command_class = getattr(module, command_name.capitalize())

        command = command_class()
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError('can not found Command %s' % command_name)

    return command


def sys_exit(exitcode: int):
    pass


def trigger(command_name: str, **kwargs):
    command = get_command(command_name)
    command.build(**kwargs)
    command.run()

    command.exit()

    sys_exit(command.exitcode)


@click.group()
def cli():
    pass


@click.command()
@click.argument('target')
def thread(target: str):
    thread_run(target)
    pass


@click.command()
@click.argument('target')
def single(target: str):
    single_run('target')
    pass


@click.command()
@click.argument('target')
def generate(target: str):
    gen(target)
    pass


@click.command()
@click.argument('target')
def check(target: str):
    trigger('check', target=target)


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
cli.add_command(check)
