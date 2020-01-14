import unittest
import signal
import os
import time
from os.path import basename

from abc import abstractmethod
from typing import Any

import linecache
import importlib

from tests.telescreen import tests_path

from base.libs import RequestScraper, Model
from base.components import Processor
from base.components.pipeline import Pipeline
from base.core.collect import collect_scheme

schemes_path = os.path.join(tests_path, 'mock_schemes')

from base.command import sys_exit
from base.command.thread import Thread
from base.command.generate import Generate
from unittest import mock
from base.command import Command

from click.testing import CliRunner

from base.core import collect


# mock
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

    sys_exit(command.exitcode)


class TestCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import shutil
        # shutil.rmtree(os.path.join(schemes_path, 'generate'))

    def test_atom(self):
        params = {
            'scheme': 'atom',
            'path': schemes_path
        }

        command = Thread()
        mock_trigger(command, **params)

        # block here

        from base.core.collect import models_pipeline as pipeline
        assert pipeline.suit.processors[0].name == 'Duplication'
        assert pipeline.suit.processors[1].name == 'Count'

        count = pipeline.suit.processors[1].count
        failed = len(pipeline.failed)

        assert count + failed > 5 * 10

    def test_atom_runner(self):
        runner = CliRunner()
        from base.command.Command import thread
        result = runner.invoke(thread, ['atom', '--path', r'E:\cloudWF\RFW\ScrapyUtils\tests\mock_schemes'])

        print(result.output)

    def test_proxy(self):
        params = {
            'scheme': 'proxy_test',
            'path': schemes_path
        }

        command = Thread()
        mock_trigger(command, **params)

    @unittest.skip
    def test_proxy_test_runner(self):
        runner = CliRunner()
        from base.command.Command import thread
        result = runner.invoke(thread, ['proxy_test', '--path', r'E:\cloudWF\RFW\ScrapyUtils\tests\mock_schemes'])

        print(result.output)

    def test_instable(self):
        runner = CliRunner()
        from base.command.Command import thread
        result = runner.invoke(thread, ['test_instable', '--line', '0'])

        print(result.output)

        from base.core.collect import models_pipeline

        print(models_pipeline.suit.processors[0].count)
        assert models_pipeline.suit.processors[0].count > 0

    def test_log(self):
        command = Thread()

        command.log.info('wtf!', 'Pipeline', 'Count')
        command.log.info('wtf!', 'Scrapy')
        command.log.info('wtf!', 'Core')
        command.log.info('wtf!', )


if __name__ == '__main__':
    unittest.main()
