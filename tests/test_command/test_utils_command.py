import unittest

import click

from ScrapyUtils.command import UtilsCommand


class UtilsCommandTestCase(unittest.TestCase):
    def test_default_method(self):
        """Methods testcases"""

        # execute must be implemented
        with self.subTest('not implemented'):
            with self.assertRaises(NotImplementedError):
                UtilsCommand.callback()

        # default command
        with self.subTest('default command'):
            command = UtilsCommand.click_command()

            assert isinstance(command, click.Command)


if __name__ == '__main__':
    unittest.main()
