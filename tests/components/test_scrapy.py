from unittest import TestCase

from typing import *

from base.libs import Model, Field
from base.components.proceesor import Processor
from base.components.step import StepSuit, ActionStep, ParseStep

from base.libs.scraper import RequestScraper
from base.libs.task import Task

from base.components.pipeline import Pipeline


class MockModel(Model):
    name = Field()


from base.tool import xpathParse


class PersonModel(Model):
    name = Field()


count = 0


class MockPersonParse(ParseStep):

    def parsing(self):
        names = xpathParse(self.content, r'//*[@class="person"]')

        for name in names:
            m = PersonModel()
            m.name = name
            global count
            count += 1
            yield m


class SingleAction(ActionStep):
    def scraping(self, task: Task):
        """
        Args:
            task (Task):
        """
        return self.scraper.get(task.url)


class Count(Processor):
    count = 0

    def process_item(self, model: Model) -> Any:
        """
        Args:
            model (Model):
        """
        self.count += 1


def scrapy(suit: StepSuit, task: Task, pipeline: Pipeline):
    """
    Args:
        suit (StepSuit):
        task (Task):
        pipeline (Pipeline):
    """
    suit.scrapy(task)

    # TODO refact models deque
    for model in suit.models:
        pipeline.push(model)

    suit.models.clear()


class TestScrapy(TestCase):

    def setUp(self) -> None:
        r = RequestScraper()
        r.scraper_activate()
        self.scraper = r

        task = Task()
        task.url = 'test url'
        task.param = {'key': 'key value'}
        self.task = task

    def tearDown(self) -> None:
        super().tearDown()

    def test_scrapy(self):
        #
        suit = StepSuit([SingleAction, MockPersonParse], self.scraper)

        tasks = [Task(url='http://127.0.0.1:8090/mock/random/dynamic') for i in range(10)]

        pipeline = Pipeline([Count])

        for task in tasks:
            scrapy(suit, task, pipeline)

        pipeline.stop()

        failed = len(pipeline.failed)
        processed = pipeline.suit.schemes[0].mock_count

        assert (failed + processed) == count

    def test_log(self):
        pass
