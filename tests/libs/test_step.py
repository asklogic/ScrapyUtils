import unittest
from typing import List

from base.components.step import Step, StepSuit, ActionStep, ParseStep
from base.libs import RequestScraper, Task, Model, Field

from base.tool import xpathParse
from tests.core.test_command import Command


# test demo
class ItemTest(Model):
    name = Field()


class SimpleAction(ActionStep):

    def scraping(self, task):
        return 'info'


class SimpleParse(ParseStep):
    def parsing(self):
        for i in range(5):
            import time
            item = ItemTest()
            item.name = str(int(time.time()))
            yield item


# test scrapy www.kuaidaili.com
class IpModel(Model):
    ip = Field()


class SingleAction(ActionStep):
    def scraping(self, task: Task):
        return self.scraper.get(task.url)


class ParseIp(ParseStep):
    def parsing(self):
        ips = xpathParse(self.content, r'//*[@id="list"]/table/tbody/tr/td[1]')
        for ip in ips:
            m = IpModel()
            m.ip = ip
            yield m


# Test Step

# setup:
# common RequestScraper: r
# default task : t. url = 'http://ip.cn'
# command's log : syntax:  '[TEST_STEP]'

# case:
# test_demo : Step and StepSuit's demo
# test_init: property and init step
# test_failed_init:

class TestStep(unittest.TestCase):
    def setUp(self) -> None:
        r = RequestScraper()
        r.scraper_activate()
        self.r = r

        t = Task()
        t.url = 'http://ip.cn'
        self.t = t

        class TestStepCommand(Command):
            def syntax(self):
                return '[TEST_STEP]'

        self.log = TestStepCommand().log

    def test_demo(self):
        # simple action
        # change suit.content
        simple_action_suit = StepSuit([SimpleAction], self.r)
        simple_action_suit.scrapy(self.t)

        assert simple_action_suit.content == 'info'
        assert simple_action_suit.models == []

        # simple parse
        # add model in suit.model
        simple_parse_suit = StepSuit([SimpleParse], self.r)

        assert len(simple_parse_suit.models) == 0
        simple_parse_suit.scrapy(self.t)
        assert len(simple_parse_suit.models) == 5

        for model in simple_parse_suit.models:
            assert isinstance(model, ItemTest)

        # suit's property
        normal_suit = StepSuit([SimpleAction, SimpleParse], self.r)

        p = id(normal_suit.steps[0].context)
        for step in normal_suit.steps:
            assert id(step.context) == p

        p = id(normal_suit.steps[0].scraper)
        for step in normal_suit.steps:
            assert id(step.scraper) == p

    def test_init(self):

        suit = StepSuit([SimpleAction], self.r, self.log)

        # default property
        assert suit.context == {}
        assert suit.log == self.log
        assert suit.content == ''
        assert suit.models == []
        assert isinstance(suit.steps[0], SimpleAction)

    def test_failed_init(self):

        # step class
        with self.assertRaises(AssertionError) as ae:
            StepSuit([SimpleAction()], self.r)
        assert 'StepSuit need Step class.' in str(ae.exception)

        # scraper activated.
        # with self.assertRaises(AssertionError) as ae:
        #     pass

    def test_failed_scarping(self):
        class FailedAction(ActionStep):
            def scraping(self, task: Task):
                raise Exception('action failed')

        suit = StepSuit([FailedAction, SimpleParse], self.r, self.log)

        suit.scrapy(self.t)

        assert len(suit.models) == 0
        assert suit.content == ''

    def test_failed_check(self):
        class FailedCheckAction(ActionStep):
            def check(self, content):
                assert False

        from base import log

        log.line = 3

        suit = StepSuit([FailedCheckAction, SimpleParse], self.r, self.log)

        suit.scrapy(self.t)

        assert len(suit.models) == 0
        assert suit.content == ''

    def test_failed_parsing(self):
        class FailedParsing(ParseStep):

            def parsing(self):
                raise Exception('parse failed')

        suit = StepSuit([SimpleAction, FailedParsing], self.r, self.log)
        suit.scrapy(self.t)

        assert suit.content == 'info'
        assert len(suit.models) == 0

    @unittest.skip
    def test_scrapy_ip(self):
        """
        Scrapy ip from https://www.kuaidaili.com/free/inha/2/
        single page have 15 row,and will generate 15 models
        """
        suit = StepSuit([SingleAction, ParseIp], self.r)

        t = Task()
        t.url = 'https://www.kuaidaili.com/free/inha/2/'
        suit.scrapy(t)

        assert len(suit.models) == 15
        for m in suit.models:
            print(m.ip)

    def test_instable_page(self):
        """
        case 1
        60% requests will be forbidden
        """

        task_list = []
        for i in range(5):
            t = Task()
            t.url = r'http://127.0.0.1:8090/mock/random/violation'
            task_list.append(t)

        suit = StepSuit([SingleAction, SimpleParse], self.r, self.log)

        sum = []
        for t in task_list:
            suit.scrapy(t)

            sum.extend(suit.models)

        assert len(sum) < 5 * 5

    def test_dynamic_page(self):
        """
        case 2
        http status code is 200 but page is wrong

        must raise exception in check method
        """

        class CheckedAction(ActionStep):

            def scraping(self, task: Task):
                return self.scraper.get(task.url)

            def check(self, content):
                assert '200 and success' in content

        t = Task()
        t.url = 'http://127.0.0.1:8090/mock/failed'

        suit = StepSuit([CheckedAction, SimpleParse], self.r)

        suit.scrapy(t)

        assert suit.content == ''
        assert len(suit.models) == 0

    def test_dynamic_content(self):
        """
        case 3
        content uncertain
        """

        class PersonModel(Model):
            name = Field()

        class MockPersonParse(ParseStep):

            def parsing(self):
                names = xpathParse(self.content, r'//*[@class="person"]')
                for name in names:
                    m = PersonModel()
                    m.name = name
                    yield m

        t = Task()
        t.url = 'http://127.0.0.1:8090/mock/random/dynamic'

        suit = StepSuit([SingleAction, MockPersonParse], self.r)
        suit.scrapy(t)

        assert len(suit.models) >= 4

    def test_failed(self):
        # TODO
        pass

    def test_check(self):
        # TODO:
        pass

    def test_log(self):

        from tests.core.test_command import Command

        class TestStepCommand(Command):
            def syntax(self):
                return '[TEST_STEP]'

        log = TestStepCommand().log
        log.info('test_info')

        simple_action_suit = StepSuit([SimpleAction], self.r, log)
        simple_action_suit.scrapy(self.t)


if __name__ == '__main__':
    unittest.main()
