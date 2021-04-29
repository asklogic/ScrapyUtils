import unittest
import time

from base.command.entity import Command
from base.command.entity.thread_ import Thread

# tests: add sys.path
from tests import telescreen


class TestCommandThreadTestCase(unittest.TestCase):
    def test_demo(self):
        kwargs = {
            # 'scheme': 'atom',
            'scheme': 'atom'
        }

        command = Thread()
        command.command_alter(**kwargs)
        command.command_initial(**kwargs)
        command.command_process(**kwargs)

        pass

        while not command.finished() and True:
            time.sleep(0.2)

        command.stop()

        pass


if __name__ == '__main__':
    unittest.main()
