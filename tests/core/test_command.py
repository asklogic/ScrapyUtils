import unittest
import logging
import signal
import os

from abc import abstractmethod
from base.log import act
from typing import List, Any


class Command(object):
    do_collect: bool = True
    exitcode: int = 0
    interrupt: bool = False

    def syntax(self) -> str:
        return '[Command]'

    def __init__(self):
        pass

    def log(self):
        # TODO
        return act

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


from base.core import collect
from tests.telescreen import tests_path

schemes_path = os.path.join(tests_path, 'mock_schemes')

from base.libs import RequestScraper, Task, Scraper, Model
from base.components.step import Step, StepSuit
from base.components import Processor

from tests.core.test_scrapy import SingleAction, MockPersonParse
from base.libs.pipeline import BaseThreading, Pipeline, Consumer
from queue import Queue

count = 0


class GlobleCount(Processor):

    def process_item(self, model: Model) -> Any:
        global count
        count += 1


class ScrapyThread(Consumer):
    def __init__(self, task_queue: Queue, steps: List[Step], scraper: Scraper, pipeline: Pipeline):
        super(ScrapyThread, self).__init__(task_queue)

        self.suit = StepSuit(steps, scraper)
        self.pipeline = pipeline

    def consuming(self, current: Task):
        self.suit.scrapy(current)
        # TODO refact models deque
        for model in self.suit.models:
            self.pipeline.push(model)
        self.suit.models.clear()


from base.core import collect, collect_steps, collect_processors


class CommandTest(Command):
    pipeline: Pipeline = None
    steps: List[Step] = None

    task_queue: Queue = None

    def syntax(self) -> str:
        return '[TEST]'

    def options(self, **kwargs):
        atom = os.path.join(schemes_path, 'atom')

        # TODO: default step
        steps = collect_steps(atom)

        # TODO: default processor
        processors = collect_processors(atom)

        # test parse
        # processors.append(GlobleCount)

        pipeline = Pipeline(processors)

        self.steps = steps
        self.pipeline = pipeline

        # TODO: resume tasks
        self.task_queue = Queue()

        tasks = [Task(url='http://127.0.0.1:8090/mock/random/dynamic') for i in range(10)]
        for task in tasks:
            self.task_queue.put(task)

    def run(self):
        # profile

        # task and active scraper

        scraper = RequestScraper

        # init ScrapyThread
        scrapy_threads = []
        for i in range(3):
            scraper = RequestScraper()
            scraper.scraper_activate()
            scrapy_threads.append(ScrapyThread(self.task_queue, self.steps, scraper, self.pipeline))

        for thread in scrapy_threads:
            thread.start()


def get_command(obj) -> Command:
    # mock
    return obj


def sys_exit(exitcode: int):
    pass


def trigger(command_name: str, **kwargs):
    # get command class
    command: Command = get_command(command_name)

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
        # command.log.error('Other Exception')
        command.failed()
        raise e

    finally:
        command.exit()

    sys_exit(command.exitcode)


class TestCommand(unittest.TestCase):

    def test_atom(self):
        command = CommandTest()
        trigger(command, **{'scheme': 'atom'})

        import time
        time.sleep(0.2)

        failed = len(command.pipeline.failed)
        count = command.pipeline.suit.processors[1].count

        assert count + failed > 6 * 10


if __name__ == '__main__':
    unittest.main()
