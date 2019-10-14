import unittest

from threading import Event
from typing import *

from base.components import Processor
from base.libs import Task, Model, Field
from queue import Queue, Empty
from collections import deque
from threading import Thread
import threading
import time

import threading
import time
import os
import json


class BaseThreading(threading.Thread):

    def __init__(self, event: Event = threading.Event()):

        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._stopped_event = threading.Event()

    def run(self) -> None:
        """
        demo
        :return:
        """
        while True:
            self.wait()
            time.sleep(1)
            print('run')

    @property
    def event(self):
        return self._stopped_event

    def wait(self):
        self.event.wait()

    def stop(self):
        self._stopped_event.clear()

    def start(self):
        if self.isAlive():
            self._stopped_event.set()
        else:
            threading.Thread.start(self)
            self._stopped_event.set()


project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
temp = os.path.join(project_path, 'tests', 'temp_dir')

class ProcessorSuit(object):
    _processors: List[Processor]

    def __init__(self, processors: List[type(Processor)]):
        assert isinstance(processors, Iterable)
        for processor in processors:
            # assert isinstance(processor, Processor), 'Processor must be init'
            assert issubclass(processor, Processor), 'Processor class'

        self._processors = []
        # init
        for processor in processors:
            try:
                current = processor()
                self._processors.append(current)
            except Exception as e:
                pass
                # TODO : log out
            finally:
                pass
                # TODO : log out

    @property
    def processors(self):
        return self._processors

    def process(self, model):
        current = model
        next = None
        # FIXME: linked?
        for processor in self.processors:
            if not isinstance(current, processor.target):
                continue

            next = processor.process_item(current)

            if next is False:
                break
            elif next is None:
                continue
            else:
                current = next


class PipelineConsumer(BaseThreading):
    _queue: Queue
    _failed: set
    _suit: ProcessorSuit

    _exit: bool = False

    def __init__(self, queue: Queue, failed: set, suit: ProcessorSuit):
        super(PipelineConsumer, self).__init__()

        self._queue = queue
        self._failed = failed

        self._suit = suit

    @property
    def queue(self):
        return self._queue

    def run(self) -> None:
        while not self._exit:
            # FIXME: loop or decorator?
            try:
                model = self.queue.get(block=True, timeout=1)
            except Empty as em:
                continue

            try:
                self._process(model=model)
            except Exception as e:
                # other exception in process_item method
                self._failed.add(model)

                # TODO: necessary process
                # failed in process. break down all process
                break

    def _process(self, model):
        self._suit.process(model)

    def exit(self):
        self.stop()
        self._exit = True


class Pipeline(object):
    _queue: Queue
    _failed: set

    _suit: ProcessorSuit
    consumer: PipelineConsumer

    def __init__(self, processors: List[type(Processor)]) -> None:
        # processor
        for processor in processors:
            assert issubclass(processor, Processor)

        self._queue = Queue()
        self._failed = set()

        # init processor (processor's on_start method)
        suit = ProcessorSuit(processors)
        # TODO: log out
        self._suit = suit

        # consumer
        self.consumer = PipelineConsumer(self.queue, self.failed, suit)
        self.consumer.start()

    def _start_processor(self):
        """
        in processor suit
        """
        pass

    def _exit_processor(self):
        pass

    @property
    def queue(self):
        return self._queue

    @property
    def failed(self):
        return self._failed

    @property
    def suit(self):
        return self._suit

    def push(self, obj):
        self.queue.put_nowait(obj)

    def size(self) -> int:
        return self.queue.qsize()

    def pop(self) -> object:
        return self.queue.get_nowait()

    def process(self, model: Model):
        pass

    def exit(self):
        # exit consumer
        self.consumer.exit()

        #
        for processor in self._suit.processors:
            processor.on_exit()

        while self.queue.qsize() > 0:
            self.failed.add(self.queue.get())


class Person(Model):
    name = Field()
    age = Field()
    address = Field()


import faker

f = faker.Faker(locale='zh_CN')


class Test_processor(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        faker_persons = set()
        for i in range(500):
            [faker_persons.add(Person(name=f.name(), age=f.random_int(10, 50), address=f.address())) for x in range(10)]

        cls.faker_persons = faker_persons

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        import shutil
        # careful
        shutil.rmtree(temp)

    def test_test(self):
        t = BaseThreading()

        assert True

    def test_init(self):
        class TestProcessor(Processor):
            def process_item(self, model: Model) -> Any:
                return model

        class AdultCount(Processor):
            count = 0

            def process_item(self, model: Person) -> Any:
                if model.age > 18:
                    self.count += 1
                return model

        t = Task(url='http://127.0.0.1:8090')

        processors = [TestProcessor]
        pipeline = Pipeline(processors)

        [pipeline.push(t) for x in range(500)]
        assert pipeline.size() == 500

        # pipeline.pop()
        import time
        time.sleep(0.2)

        assert pipeline.size() == 0
        pipeline.exit()
        assert pipeline.consumer._exit is True


        p = Pipeline([AdultCount])
        [p.push(x) for x in self.faker_persons]
        time.sleep(0.2)
        p.exit()

        # FIXME: private property?
        assert p.consumer._suit.processors[0].count is not 100
        assert p.consumer._suit.processors[0].count > 50

    def test_processor(self):
        class FailedInitProcessor(Processor):
            def on_start(self):
                raise Exception('Failed in on_start method.')

        p = Pipeline([FailedInitProcessor])

        assert p._suit.processors == []

        class FailedProcessor(Processor):

            def process_item(self, model: Model) -> Any:
                raise Exception('Failed in process_item method')

        p = Pipeline([FailedProcessor])

        [p.push(Task()) for i in range(10000)]
        # has start consuming
        assert not p.size() is 10000
        p.exit()

        # failed models in pipeline's failed set.
        # error models and remain models.
        assert len(p.failed) == 10000

        class FailedExitProcessor(Processor):
            def on_exit(self) -> Any:
                raise Exception('Failed in on_exit method.')

        p = Pipeline([FailedExitProcessor])
        # TODO: how to log out ?

    def test_file_processor(self):


        class FileProcessor(Processor):
            path: str
            name: str
            index: int

            def on_start(self):
                # init
                self.index = 0
                self.name = str(int(time.time()))[3:]
                self.path = temp

                # check file permission
                assert os.path.exists(self.path)
                assert os.path.isdir(self.path)
                # TODO

                # check exist file and load data
                pass

                # temp:
                self.name = 'mock_data'

            def process_item(self, model: Model) -> Any:
                self._append(model)

            def _append(self, model: Model):
                if len(self.data) >= 100000:
                    self.dump()
                self.data.append(model.pure_data)

            def dump(self):
                name = os.path.join(self.path, ''.join([self.name, '-', str(self.index), '.json']))
                with open(name, 'w') as f:
                    json.dump(self.data, f)
                self.data.clear()

            def on_exit(self):
                if self.data:
                    self.dump()

        p = Pipeline([FileProcessor])

        assert len(p.suit.processors) == 1

        [p.push(x) for x in self.faker_persons]
        time.sleep(0.005)
        p.exit()

        mock_data_path = os.path.join(project_path, 'tests', 'temp_dir',
                                      ''.join(['mock_data', '-', '0', '.json']))

        assert os.path.exists(mock_data_path)

        with open(mock_data_path, 'r') as file:
            dump_data = json.load(file)
        assert len(p.failed) + len(dump_data) == 5000

    def test_processor_suit(self):
        class NormalProcessor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1
                return model

        class FalseProcessor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1
                return False

        class BlankProcessor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1

        class ExceptionProcesssor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1
                raise Exception()

        class TargetProcessor(Processor):
            count = 0
            target = Person

            def process_item(self, model: Model) -> Any:
                self.count += 1

        t = Task(url='http://xx.cn')

        # processor class
        with self.assertRaises(TypeError) as te:
            ProcessorSuit([NormalProcessor()])
        # abort
        # assert 'Processor must be init' in str(te.exception)

        normal = NormalProcessor
        blank = BlankProcessor
        error = ExceptionProcesssor
        tar = TargetProcessor
        false = FalseProcessor

        suit0 = ProcessorSuit([normal])
        suit0.process(t)
        assert suit0.processors[0].count == 1

        suit1 = ProcessorSuit([normal, tar])
        suit1.process(t)
        assert suit1.processors[0].count == 1
        assert suit1.processors[1].count == 0

        suit2 = ProcessorSuit([blank])
        suit2.process(t)
        assert suit2.processors[0].count == 1

        suit3 = ProcessorSuit([blank, normal])
        suit3.process(t)
        assert suit3.processors[0].count == 1
        assert suit3.processors[1].count == 1

        suit4 = ProcessorSuit([false, blank, normal])
        suit4.process(t)
        assert suit4.processors[0].count == 1
        assert suit4.processors[1].count == 0
        assert suit4.processors[1].count == 0


if __name__ == '__main__':
    unittest.main()
