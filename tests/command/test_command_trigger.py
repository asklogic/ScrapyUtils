import unittest
import os
import signal

from tests.telescreen import tests_path

schemes_path = os.path.join(tests_path, 'mock_schemes')

from base.command import Command, ComponentMixin

from base.log import Wrapper as log

from base.command import command_map

from base.log import set_syntax

from base.components import *

from base.core import *


# mock
def mock_trigger(command_name: str, **kwargs):
    # get command class
    """
    Args:
        command_name (str):
        **kwargs:
    """
    if type(command_name) == str:
        command: Command = command_map.get(command_name)
    # mock: get command by command name
    else:
        command = command_name

    if not command:
        log.error('command {} not exist.'.format(command_name))
        # mock: return to sys.exit
        return

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGINT, command.signal_callback)
    signal.signal(signal.SIGTERM, command.signal_callback)

    if command.do_collect:
        command: ComponentMixin or Command
        # stage 1: prepare
        collect_scheme_preload(kwargs.get('scheme'))

        if kwargs.get('confirm'):
            input('Press any key to continue.')

        # stage 2: initial
        # global variable to command
        collect_scheme_initial()

        command.suits = get_suits()
        command.tasks = get_tasks()
        command.pipeline = get_pipeline()
        command.config = get_config()
        command.proxy = get_proxy()

        # TODO: proxy start.
        if command.proxy:
            command.proxy.execute()
        set_syntax(command.syntax)

    try:
        # stage 3: run
        command.run()

    except Exception as e:
        command.failed()
        log.exception('Command', e)

    finally:
        # stage 4: exit
        command.exit()

    # mock: no sys exit
    # sys_exit(command.exitcode)


class TestCommandTrigger(unittest.TestCase):
    def test_function_get_command_error(self):
        mock_trigger('not_exist', **{'scheme': 'atom'})

    def test_collect_scheme_demo(self):
        collect_scheme_preload('atom')
        collect_scheme_initial()

        [x.scraper_quit() for x in get_scraper()]

    # def test_collect_init_fox(self):
    #     collect_scheme_prepare('Fox')
    #     collect_scheme_initial()
    #
    #     [x.scraper_quit() for x in get_scraper()]


if __name__ == '__main__':
    unittest.main()
