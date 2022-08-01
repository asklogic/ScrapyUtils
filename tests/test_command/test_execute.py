import unittest

from click.testing import CliRunner

from ScrapyUtils.command.execute import Execute
from ScrapyUtils.command import cli
from test_switch import mock_project_home


class CommandExecuteTestCase(unittest.TestCase):
    def test_something(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['execute', 'normal'])

        print(result)


if __name__ == '__main__':
    unittest.main()
