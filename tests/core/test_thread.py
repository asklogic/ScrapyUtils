import unittest

import threading
import time

from queue import Queue
from typing import List

from base.libs.thread import BaseThreading, Consumer, ThreadSuit
from base.components import StepSuit, Step, Pipeline
from base.libs import RequestScraper, Scraper, Task

from base.command.thread import ScrapyConsumer


class TestThread(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()

        for i in range(1, 100):
            self.queue.put(Task())

    def test_base_thread(self):
        """
        BaseThreading
        """

        base = BaseThreading()

        base.start()
        base.stop()

    def test_base_property(self):
        # parameter : event
        # critical: same event. start and stop keep the same action.

        base1 = BaseThreading()
        base2 = BaseThreading()

        assert id(base1.event) == id(base2.event)

        event = threading.Event()
        base = BaseThreading(event)

        # property : _stopped_event
        assert base.event is event
        assert id(base.event) == id(event)

        # ----------------------------------------------------------------------

        # property : daemon

        assert base1.daemon == base2.daemon == base.daemon is True

        # assert
        with self.assertRaises(AssertionError) as e:
            BaseThreading(object())
        assert 'need event instance.' in str(e.exception)

        # ----------------------------------------------------------------------

        # kwargs:
        # name
        n = BaseThreading(**{'name': 'custom_name'})
        assert n.getName() == 'custom_name'

    def test_consumer(self):
        # ----------------------------------------------------------------------

        # method : consuming
        # block after consuming() done.

        class Demo(Consumer):
            count = 0

            def consuming(self, obj):
                self.count += 1

        demo = Demo(self.queue, delay=0.2)
        demo.start()
        time.sleep(0.5)

        assert demo.count == 2

        # ----------------------------------------------------------------------

        # TODO. Exception in consuming

        class ExceDemo(Consumer):

            def consuming(self, obj):
                raise Exception()

        exce = ExceDemo(self.queue)
        exce.start()
        time.sleep(0.5)

    def test_consumer_property(self):
        # ----------------------------------------------------------------------

        # parameter : queue
        consumer = Consumer(Queue())

        with self.assertRaises(AssertionError) as e:
            Consumer(object())
        assert 'Consumer need queue object.' in str(e.exception)

        # property : queue
        the_queue = Queue()
        the_consumer = Consumer(the_queue)

        assert id(the_queue) == id(the_consumer.queue)

        # ----------------------------------------------------------------------

        # parameter : delay
        # default : 1
        assert consumer.delay == 1
        assert Consumer(the_queue, 2).delay == 2

        # ----------------------------------------------------------------------

        # parameter : lock
        the_lock = threading.Lock()
        the_consumer = Consumer(the_queue, lock=the_lock)

        assert id(the_lock) == id(the_consumer.lock)

        # ----------------------------------------------------------------------

    def test_scrapy_consumer(self):
        kw = {
            'queue': self.queue,
            'delay': 0.2,
        }
        suit = StepSuit([], RequestScraper())
        pipeline = Pipeline([])

        consumer = ScrapyConsumer(suit, pipeline, **kw)
        assert self.queue.qsize() == 99

        consumer.start()
        time.sleep(0.5)
        assert self.queue.qsize() == 97

    def test_scrapy_consumer_property(self):

        # ----------------------------------------------------------------------

        the_queue = Queue()
        kw = {
            'queue': the_queue,
        }
        suit = StepSuit([], RequestScraper())
        pipeline = Pipeline([])

        # ----------------------------------------------------------------------

        # parameter : suit

        consumer = ScrapyConsumer(suit, pipeline, **kw)
        assert id(suit) == id(consumer.suit)

        # ----------------------------------------------------------------------

        # parameter : pipeline

        # ----------------------------------------------------------------------

        # assert parameter.

        assert id(pipeline) == id(consumer.pipeline)

        with self.assertRaises(AssertionError) as e1:
            ScrapyConsumer(object(), pipeline, **kw)
        assert 'ScrapyConsumer need StepSuit.' in str(e1.exception)

        with self.assertRaises(AssertionError) as e2:
            ScrapyConsumer(suit, object(), **kw)
        assert 'ScrapyConsumer need Pipeline.' in str(e2.exception)

        # ----------------------------------------------------------------------

        # consumer parameter:

        consumer = ScrapyConsumer(suit, pipeline, **kw)

        assert id(consumer.queue) == id(the_queue)
        # default
        assert consumer.delay == 1
        assert consumer.lock
        # assert isinstance(consumer.lock, threading.Lock)

        the_lock = threading.Lock()
        kw = {
            'queue': the_queue,
            'delay': 2.5,
            'lock': the_lock,
        }
        consumer = ScrapyConsumer(suit, pipeline, **kw)
        assert id(consumer.queue) == id(the_queue)
        assert consumer.delay == 2.5
        assert id(consumer.lock) == id(the_lock)

        # ----------------------------------------------------------------------

    @unittest.skip
    def test_mock_thread(self):
        import random
        class MockThread(Consumer):

            def __init__(self, **kw):
                super(MockThread, self).__init__(**kw)

            def consuming(self, obj):
                delay = random.randint(5, 20) / 200

                print(self.name, 'scraping!', 'delay', delay)
                time.sleep(delay)

        lock = threading.Lock()

        queue = Queue()
        [queue.put(i) for i in range(10)]

        c1 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-1')
        c2 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-2')
        c3 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-3')
        c4 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-4')

        c1.start()
        c2.start()
        c3.start()
        c4.start()

        queue.join()
        assert queue.qsize() == 0

    def test_consumer_suit(self):

        # ----------------------------------------------------------------------

        kw = {
            'queue': self.queue,
            'delay': 0.2,
        }
        suit = StepSuit([], RequestScraper())
        pipeline = Pipeline([])
        kwargs = {
            'queue': self.queue,
            'delay': 0.2,
            'suit': suit,
            'pipeline': pipeline
        }

        # ----------------------------------------------------------------------
        # normal

        consumers = []

        for i in range(10):
            consumer = ScrapyConsumer(suit, pipeline, **kw)
            consumers.append(consumer)

        [x.start() for x in consumers]
        # few moment later.
        [x.stop() for x in consumers]

        # ----------------------------------------------------------------------

        kwargs = {
            'queue': self.queue,
            'delay': 0.2,
            'suit': suit,
            'pipeline': pipeline
        }

        thread_suit = ThreadSuit(ScrapyConsumer, 15, kwargs)

        # ----------------------------------------------------------------------

    def test_consumer_suit_property(self):
        # ----------------------------------------------------------------------

        kwargs = {
            'queue': self.queue,
            'delay': 0.2,
            'suit': StepSuit([], RequestScraper()),
            'pipeline': Pipeline([])
        }

        # ----------------------------------------------------------------------

        # parameter : thread_class

        suit = ThreadSuit(ScrapyConsumer, 5, kwargs, ['suit'])

        first_consumer = suit.consumers[0]
        assert isinstance(first_consumer, ScrapyConsumer)

        # consumer parameter
        assert id(self.queue) == id(first_consumer.queue)
        assert first_consumer.delay == 0.2

        # ----------------------------------------------------------------------

        # parameter : number
        assert len(suit.consumers) == 5

        # ----------------------------------------------------------------------

        # assert
        with self.assertRaises(AssertionError) as ae:
            ThreadSuit(object(), 5, kwargs)
        assert 'ThreadSuit need BaseThreading class.' in str(ae.exception)

        # ----------------------------------------------------------------------

        # property : consumers

        assert suit.consumers

        assert id(suit.consumers[0].event) != id(suit.consumers[1].event)
        assert id(suit.consumers[0].suit) != id(suit.consumers[1].suit)

        # ----------------------------------------------------------------------


if __name__ == '__main__':
    # unittest.main()

    time.sleep(5)
