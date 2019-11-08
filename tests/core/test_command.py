import unittest
import signal
import os
import time
from os.path import basename

from abc import abstractmethod
from typing import Any

import linecache

from base.core import collect_profile
from tests.telescreen import tests_path

from base.libs import RequestScraper, Model
from base.components import Processor
from base.components.pipeline import Pipeline
from base.core import collect_steps, collect_processors

schemes_path = os.path.join(tests_path, 'mock_schemes')

from base.command import sys_exit
from base.command.thread import Thread, ScrapyThread
from base.command.generate import Generate
from unittest import mock
from base.command import Command

from click.testing import CliRunner


# mock
def mock_trigger(command, **kwargs):
    # get command class
    command: Command = command

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGINT, command.signal_callback)
    signal.signal(signal.SIGTERM, command.signal_callback)

    # collect
    # command.collect(kwargs.get('target'))

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
        shutil.rmtree(os.path.join(schemes_path, 'generate'))

    def test_atom(self):
        params = {
            'scheme': 'atom',
            'path': schemes_path
        }

        command = Thread()
        mock_trigger(command, **params)

        # block here

        failed = len(command.pipeline.failed)
        assert command.pipeline.suit.processors[0].name == 'Duplication'
        assert command.pipeline.suit.processors[1].name == 'Count'
        count = command.pipeline.suit.processors[1].count

        assert count + failed > 5 * 10

    def test_atom_runner(self):
        runner = CliRunner()
        from base.command.Command import thread
        result = runner.invoke(thread, ['atom', '--path', r'E:\cloudWF\RFW\ScrapyUtils\tests\mock_schemes'])

        print(result.output)

    def test_log(self):
        command = Thread()

        command.log.info('wtf!', 'Pipeline', 'Count')
        command.log.info('wtf!', 'Scrapy')
        command.log.info('wtf!', 'Core')
        command.log.info('wtf!', )

    def test_thread_consumer(self):
        from base.command import Command

        atom = os.path.join(schemes_path, 'atom')

        steps = collect_steps(atom)
        task_queue = collect_profile(atom)['task_queue']

        # don't print out
        # pipeline = Pipeline(collect_processors(atom))
        pipeline = Pipeline([])

        scraper = RequestScraper()
        scraper.scraper_activate()
        scraper.timeout = 1

        consumer = ScrapyThread(task_queue, steps, scraper, pipeline, Command().log)
        consumer.start()

        # TODO
        # time.sleep(1)

        consumer.join(10)

        consumer.stop()

    # @unittest.skip
    def test_generate(self):
        params = {
            'scheme': 'generate',
            'path': schemes_path
        }

        command = Generate()
        mock_trigger(command, **params)

    @unittest.skip
    def test_kuaidaili(self):
        pass


if __name__ == '__main__':
    unittest.main()
