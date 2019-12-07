import unittest

import signal
import os

from base.command import Command
from base.core.collect import collect_scheme
from base.command.thread import Thread


from tests.telescreen import tests_path, schemes_path


def mock_trigger(command, **kwargs):
    # get command class
    command: Command = command

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGINT, command.signal_callback)
    signal.signal(signal.SIGTERM, command.signal_callback)

    # collect
    if command.do_collect:
        collect_scheme(kwargs.get('scheme'))

    try:
        command.options(**kwargs)

        command.run()

    except Exception as e:
        command.failed()
        command.log.exception('Command', e)

    finally:
        command.exit()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_proxy(self):
        params = {
            'scheme': 'proxy_test',
            'path': schemes_path
        }

        command = Thread()
        mock_trigger(command, **params)




if __name__ == '__main__':
    unittest.main()
