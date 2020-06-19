import unittest

from base.command.entity import Command

# tests: add sys.path
from tests import telescreen


class MyTestCase(unittest.TestCase):
    def test_property_do_collect(self):
        command = Command()
        assert command.do_collect is True

    def test_method_collect(self):
        kwargs = {
            'scheme': 'atom'
        }

        command = Command()
        command.command_collect(**kwargs)


if __name__ == '__main__':
    unittest.main()
