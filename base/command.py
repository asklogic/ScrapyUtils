from typing import List

from base.engine import thread_run, single_run
import click
from base.generate.generator import generate as gen
import os

from base.libs.setting import Setting
from base.log import act

PROJECT_PATH = os.path.dirname(os.getcwd())


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


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)


# def build_run(config_file, args: str):
#     if len(args) < 3:
#         raise KeyError("set correct arguments")
#
#     # config = Config(config_file, args[2])
#     if args[1] == "single":
#         single_run(args[2])
#     elif args[1] == 'thread':
#         thread_run(args[2])

class Command(object):
    require_target = False
    assert_args: List[str] = ()

    setting: Setting
    exitcode: int

    def syntax(self):
        return '[Command]'

    def log(self, msg, level=0, step='globle'):
        # TODO Level
        from logging import DEBUG

        step = '<%s>' % step if step else step
        message = ' '.join((self.syntax(), step, msg))
        # message = ' '.join((x for x in (self.syntax(), step, msg) if x))
        act.log(level=DEBUG, msg=message)

    def __init__(self):
        self.setting = None
        self.exitcode = -1

    def build(self, **kw):
        pass

    def check_args(self, **kw):
        for args in self.assert_args:
            assert kw.get(args), "doesn't have arguments %s" % args
            setattr(self, args, kw.get(args))
        pass

    def run(self):
        pass

    def exit(self):
        pass
