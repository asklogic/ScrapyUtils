import unittest

from ScrapyUtils.core import *

from ScrapyUtils.libs import Task, Proxy
from ScrapyUtils.components import *

scheme_preload('TestCommonProcessor')


def mock_run(processor, kwargs):
    processors = []
    if type(processor) is []:
        processors.extend(processor)
    else:
        processors.append(processor)

    set_processors(processors)

    scheme_initial(kwargs)

    scheme_start()


def process_model(number=10):
    pipeline = get_pipeline()
    for i in range(10):
        pipeline.push(Proxy())


class MyCustomProcessor(Processor):
    pass


class ErrorInitProcessor(Processor):

    def __init__(self, step_suit=None):
        super(ErrorInitProcessor, self).__init__()
        raise Exception()


class CommonProcessorTestCase(unittest.TestCase):
    def test_demo(self):
        mock_run(processor=MyCustomProcessor, kwargs={})
        process_model(10)

    def test_error(self):
        with self.assertRaises(Exception) as e:
            mock_run(ErrorInitProcessor, {})
            process_model(10)


if __name__ == '__main__':
    unittest.main()
