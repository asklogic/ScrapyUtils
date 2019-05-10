from typing import List
import os
from logging import DEBUG, WARN, ERROR, INFO
from abc import abstractmethod
from base.engine import thread_run, single_run
from base import core
import click, time
import threading
from base.generate.generator import generate as gen

from base.libs.setting import Setting
from base.log import act

PROJECT_PATH = os.path.dirname(os.getcwd())


class Command(object):
    require_target = False
    setting: Setting

    exitcode: int
    interrupt: bool = False

    def syntax(self):
        return '[Command]'

    def log(self, msg, level=INFO, step=''):
        # TODO Level

        step = '<%s>' % step if step else step
        message = ' '.join((self.syntax(), step, msg))
        # message = ' '.join((x for x in (self.syntax(), step, msg) if x))
        act.log(level=level, msg=message)

    def signal_callback(signum, frame, self):
        pass

    def __init__(self):
        self.setting = None
        self.exitcode = 0

    def build_setting(self, target: str = None):
        if self.require_target:
            assert target, 'no target'
            setting = core.build_setting(target)
            self.setting = setting

    @abstractmethod
    def options(self, **kw):
        '''
        init command property.
        :param kw:
        :return:
        '''
        pass

    @abstractmethod
    def run(self, **kw):
        pass

    @abstractmethod
    def failed(self):
        '''
        process command's property when some thing error
        :return:
        '''
        pass

    def exit(self):
        '''
        default exit. always run in command finish
        :return:
        '''
        time.sleep(1)


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

    import signal
    signal.signal(signal.SIGINT, command.signal_callback)

    command.build_setting(kwargs.get('target'))

    try:
        command.options(**kwargs)
    except AssertionError as ae:
        import logging
        command.log(level=logging.ERROR, msg='' + str(ae))


    try:
        command.run()
    except Exception as e:
        print('exception in run', e, e.__class__)
        command.failed()

        pass
    finally:
        command.exit()
    print('exit')
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
