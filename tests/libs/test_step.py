import unittest

from base.components.step import Step, StepSuit, ActionStep, ParseStep
from base.libs import RequestScraper, Task
from base.components import Model, Field

from base.tool import xpathParse


class ItemTest(Model):
    name = Field()


class SimpleAction(ActionStep):

    def scraping(self, task):
        return 'info'


# Scrapy www.kuaidaili.com
class SimpleParse(ParseStep):
    def parsing(self):
        for i in range(5):
            import time
            item = ItemTest()
            item.name = str(int(time.time()))
            yield item


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


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        r = RequestScraper()
        r.scraper_activate()
        self.r = r

        t = Task()
        t.url = 'http://ip.cn'
        self.t = t

    def test_init(self):
        """
        step and step suit with some useful case
        """

        # simple action
        # change suit.content
        simple_action_suit = StepSuit([SimpleAction], self.r)

        simple_action_suit.scrapy(self.t)

        assert simple_action_suit.content == 'info'
        assert simple_action_suit.models == []

        # simple parse
        # add model in suit.model

        simple_parse_suit = StepSuit([SimpleParse], self.r)

        simple_parse_suit.scrapy(self.t)

        assert len(simple_parse_suit.models) == 5
        for model in simple_parse_suit.models:
            assert isinstance(model, ItemTest)

        # property

        normal_suit = StepSuit([SimpleAction, SimpleParse], self.r)

        p = id(normal_suit.steps[0].context)
        for step in normal_suit.steps:
            assert id(step.context) == p

        p = id(normal_suit.steps[0].scraper)
        for step in normal_suit.steps:
            assert id(step.scraper) == p

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
        # [print(x.ip) for x in suit.models]
        # self.fail()

    def test_instable_page(self):
        """
        case 1
        60% requests will be forbidden
        """

        task_list = []
        for i in range(10):
            t = Task()
            t.url = r'http://127.0.0.1:8090/mock/random/violation'
            task_list.append(t)

        suit = StepSuit([SingleAction], self.r)

        for t in task_list:
            suit.scrapy(t)

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

        suit = StepSuit([CheckedAction], self.r)

        suit.scrapy(t)

        assert suit.content == ''


if __name__ == '__main__':
    unittest.main()
