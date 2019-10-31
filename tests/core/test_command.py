import unittest
import signal
import os
import time
from os.path import basename

from abc import abstractmethod
from base.log import act
from typing import Any

import linecache


class Command(object):
    do_collect: bool = True
    exitcode: int = 0
    interrupt: bool = False

    def syntax(self) -> str:
        return '[Command]'

    def __init__(self):
        self.exitcode: int = 0
        self.interrupt: bool = False

    @property
    def log(self, **kwargs):
        # TODO: move to log.py
        class inner_log:
            @classmethod
            def info(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.info(message)

            @classmethod
            def warning(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.warning(message)

            @classmethod
            def error(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.error(message)

            @classmethod
            def debug(cls, msg: str, *args):
                component = ' - '.join(args)
                component_msg = ''.join(['<', component, '>']) if component else ''
                message = ' '.join([self.syntax(), component_msg, msg])
                act.debug(message)

            @classmethod
            def exception(cls, component_name: str, exception: Exception):
                exception_name = exception.__class__.__name__
                component_name = '<{}>'.format(component_name)
                message = ' '.join([self.syntax(), component_name, 'Except Exception:', exception_name])
                act.error(message)

                current = exception.__traceback__

                # TODO: refact
                current_code = current.tb_frame.f_code

                while not basename(current_code.co_filename) in ('action.py', 'parse.py') and current.tb_next:
                    current = current.tb_next
                    current_code = current.tb_frame.f_code
                lines = [linecache.getline(current_code.co_filename, current.tb_lineno + x,
                                           current.tb_frame.f_globals).replace('\n', '')
                         for x in
                         (-2, -1, 0)]

                for line in (-2, -1, 0):
                    if not lines[2 + line].strip():
                        continue
                    msg = ''.join(('Line: ', str(current.tb_lineno + line), ' |', lines[2 + line]))
                    act.debug(msg)

        return inner_log

    @abstractmethod
    def signal_callback(self, signum, frame):
        pass

    def collect(self, scheme_name: str):
        # TODO
        pass

    @abstractmethod
    def options(self, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def failed(self):
        pass

    @abstractmethod
    def exit(self):
        pass


from base.core import collect_profile
from tests.telescreen import tests_path

from base.libs import RequestScraper, Model
from base.components import Processor
from base.components.pipeline import Pipeline
from base.core import collect_steps, collect_processors

schemes_path = os.path.join(tests_path, 'mock_schemes')

from base.command import sys_exit
from base.command.thread import Thread, ScrapyThread

from unittest import mock


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

    def test_atom(self):
        params = {
            'scheme': 'atom',
            'path': os.path.join(schemes_path, 'atom')
        }

        command = Thread()
        mock_trigger(command, **params)

        # block here

        failed = len(command.pipeline.failed)
        assert command.pipeline.suit.processors[0].name == 'Duplication'
        assert command.pipeline.suit.processors[1].name == 'Count'
        count = command.pipeline.suit.processors[1].count

        assert count + failed > 5 * 10

    def test_log(self):
        command = Thread()

        command.log.info('wtf!', 'Pipeline', 'Count')
        command.log.info('wtf!', 'Scrapy')
        command.log.info('wtf!', 'Core')
        command.log.info('wtf!', )

    def test_thread_consumer(self):
        atom = os.path.join(schemes_path, 'atom')

        steps = collect_steps(atom)
        task_queue = collect_profile(atom)['task_queue']
        pipeline = Pipeline(collect_processors(atom))
        scraper = RequestScraper()
        scraper.scraper_activate()

        consumer = ScrapyThread(task_queue, steps, scraper, pipeline)
        consumer.start()

        time.sleep(1)

        consumer.stop()

    @unittest.skip
    def test_kuaidaili(self):
        pass


if __name__ == '__main__':
    unittest.main()
