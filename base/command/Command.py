# from typing import List
# from abc import abstractmethod
#
# import click
# import sys
# import os
# import signal
#
# from base.log import Wrapper as log
# from base.core.collect import collect_scheme
# from base.exception import CommandExit
#
#
# class Command(object):
#     exitcode: int = 0
#     interrupt: bool = False
#
#     do_collect: bool = True
#
#     def syntax(self) -> str:
#         return '[Command]'
#
#     def __init__(self):
#         self.exitcode: int = 0
#         self.interrupt: bool = False
#
#     @abstractmethod
#     def signal_callback(self, signum, frame):
#         pass
#
#     def collect(self, scheme_name: str):
#         # TODO
#         pass
#
#     @abstractmethod
#     def options(self, **kwargs):
#         pass
#
#     @abstractmethod
#     def run(self):
#         pass
#
#     @abstractmethod
#     def failed(self):
#         pass
#
#     @abstractmethod
#     def exit(self):
#         pass
#
#
# def sys_exit(exitcode: int):
#     pass
#
#
# def trigger(command_name: str, **kwargs):
#     # get command class
#     command: Command = get_command(command_name)
#
#     # register signal
#     # TODO: windows and linux
#     signal.signal(signal.SIGTERM, command.signal_callback)
#     signal.signal(signal.SIGINT, command.signal_callback)
#
#     # collect. -> core.collect
#     if command.do_collect:
#         collect_scheme(kwargs.get('scheme'))
#         log.info('collected scheme:{}'.format(kwargs.get('scheme')))
#
#     try:
#
#         command.options(**kwargs)
#         log.info('options finish.')
#
#         command.run()
#         log.info('run finish.')
#
#     except CommandExit as ex:
#         pass
#     except Exception as e:
#         command.failed()
#         log.exception('Command', e)
#
#     finally:
#         command.exit()
#         log.info('command exited.')
#
#     sys_exit(command.exitcode)
#
#
# def get_command(command_name: str) -> Command:
#     from base.command import registered
#
#     # TODO: WTF?
#     select_command = None
#     for command in registered:
#         if command_name in str(command):
#             command_class = getattr(command, command_name.capitalize())
#
#             # TODO: command to singleton
#             select_command = command_class()
#             break
#
#     if not select_command:
#         log.error('can not found registered Command %s' % command_name)
#         sys.exit(0)
#
#     return select_command
#
#
# @click.group()
# def cli():
#     pass
#
#
# @click.command()
# @click.argument('scheme')
# @click.option('path', '--path', default=os.getcwd(), type=click.Path())
# @click.option('line', '--line', default=3)
# def thread(scheme: str, path, line):
#     trigger('thread', scheme=scheme, path=path, line=line)
#
#     # thread_run(target)
#     # pass
#
#
# @click.command()
# @click.argument('scheme')
# @click.option('path', '--path', default=os.getcwd(), type=click.Path())
# def single(scheme: str, path):
#     trigger('single', scheme=scheme, path=path)
#
#
# @click.command()
# @click.argument('scheme')
# def generate(scheme: str):
#     trigger('generate', scheme=scheme)
#
#
# @click.command()
# @click.argument('target')
# def check(target: str):
#     trigger('check', target=target)
#
#
# cli.add_command(thread)
# cli.add_command(single)
# cli.add_command(generate)
# cli.add_command(check)
