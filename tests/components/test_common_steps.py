import unittest

# from ScrapyUtils.core.collect import scheme_preload, scheme_start, scheme_initial, scheme_exit
from ScrapyUtils.core import *

from ScrapyUtils.components import *
from ScrapyUtils.libs import Task, Proxy


class MyCustomStep(ActionStep):
    pass


class ErrorInitAction(ActionStep):

    def __init__(self, step_suit=None):
        raise Exception()


class CountActionStep(ActionStep):

    def __init__(self, step_suit=None):
        super().__init__(step_suit)

        self.count = 0

    def scraping(self, task: Task):
        self.count += 1


scheme_preload('atom')


def mock_run(step, kwargs):
    steps = []
    if type(step) is []:
        steps.extend(step)
    else:
        steps.append(step)

    set_steps([step, ])

    scheme_initial(kwargs)

    scheme_start()


def process_model(number=10):
    suit = get_suits()[0]

    for i in range(number):
        suit.closure_scrapy()(Task())
        # suit.closure_scrapy()(Proxy())


class CommonComponentsTestCase(unittest.TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        scheme_exit()

    # def test_failed(self):
    #     with self.assertRaises(Exception) as e:
    #         mock_run(ErrorInitAction, {})

    def test_demo(self):
        mock_run(MyCustomStep, {})

        # suit = get_suits()[0]
        # suit.closure_scrapy()(Task())
        process_model()

    def test_count(self):
        mock_run(CountActionStep, {})
        process_model()

        assert get_suits()[0].steps[0].count == 10

    def test_simple_suit(self):
        suit = StepSuit(MyCustomStep)

        url = 'https://www.google.com/'
        suit.simple_task(url)


if __name__ == '__main__':
    unittest.main()
