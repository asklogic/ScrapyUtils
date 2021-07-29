import unittest
from typing import List
from collections import deque

from ScrapyUtils.components import StepSuit, Action, Step, ComponentSuit, Parse, Component
from ScrapyUtils.libs import RequestScraper, Task, Scraper, Model


class ActionTest(Action):
    pass


class CountAction(Action):
    count = 0

    def scraping(self, task: Task, scraper: Scraper) -> str:
        self.count += 1


class CountParse(Parse):
    count = 0

    def parsing(self, content: str) -> List[Model]:
        self.count += 1


task = Task(url='1', param=5)


class StepSuitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.suit = StepSuit()

        self.scraper = RequestScraper()
        self.scraper.scraper_attach()

        self.scraper_without_attach = RequestScraper()

    def test_attribute_target_component_default(self):
        """Default attribute target_components is Step"""
        self.assertEqual(self.suit.target_components, Step)

    def test_property_components_default(self):
        """Default property components: []"""
        self.assertEqual(self.suit.components, [])

    def test_property_context_default(self):
        """Default context: {}"""
        self.assertEqual(self.suit.context, {})

    def test_property_scraper_default(self):
        """Default scraper: None"""
        self.assertEqual(self.suit.scraper, None)

    def test_method_add_component_wrong_type(self):
        """Wrong type will return None"""
        res = self.suit.add_component(Component())

        self.assertEqual(res, None)

    def test_method_set_scraper(self):
        """set scraper"""
        self.suit.set_scraper(self.scraper)
        self.assertIs(self.scraper, self.suit.scraper)

    def test_method_set_scraper_auto_attach(self):
        """set_scraper will attach scraper if scraper hasn't attached."""
        self.assertFalse(self.scraper_without_attach.attached)

        self.suit.set_scraper(self.scraper_without_attach)

        self.assertIs(self.suit.scraper, self.scraper_without_attach)
        self.assertTrue(self.suit.scraper.attached)
        self.assertTrue(self.scraper_without_attach.attached)

    def test_method_set_scraper_incorrect(self):
        """set_scraper in wrong type"""
        with self.assertRaises(AssertionError) as ae:
            self.suit.set_scraper(RequestScraper)
        self.assertIn('Need Scraper instance.', str(ae.exception))

    def test_method_add_component(self):
        """Method add_component will append step into suit.components"""
        step = ActionTest()
        res = self.suit.add_component(step)

        self.assertIs(res, step)
        self.assertEqual(len(self.suit.components), 1)


if __name__ == '__main__':
    unittest.main()
