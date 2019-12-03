import unittest
import os

from typing import List
from queue import Queue

from click.testing import CliRunner
from base.command import Command
from base.core import PROJECT_PATH

from base.components import Pipeline, Step

from tests.core.test_command import mock_trigger

from tests.telescreen import tests_path

schemes_path = os.path.join(tests_path, 'mock_schemes')





class TestSingle(unittest.TestCase):

    def test_init(self):
        # params = {
        #     'scheme': 'atom',
        #     'path': schemes_path
        # }
        # command = Single()
        # mock_trigger(command, **params)

        from base.command.Command import single

        runner = CliRunner()

        input_data = ''
        result = runner.invoke(single, ['atom', '--path', r'E:\cloudWF\RFW\ScrapyUtils\tests\mock_schemes'],
                               input=input_data)

        print(result.output)

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
