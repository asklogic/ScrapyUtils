import unittest

from base.components import StepSuit
from base.libs import RequestScraper, Scraper

from base.core import collect
from tests.telescreen import tests_path


def mock_wrapper():
    return RequestScraper()


class StepSuitTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        collect.collect_scheme('atom')

        cls.scraper = collect.scrapers()
        cls.steps = collect.steps_class

    def test_init(self):
        suit = StepSuit(self.steps, self.scraper)

        assert suit.scraper and isinstance(suit.scraper, Scraper)
        assert suit.steps is None
        assert suit.steps_class is self.steps

    def test_init_step(self):
        suit = StepSuit([], self.scraper)

    def test_init_scraper(self):
        with self.assertRaises(AssertionError) as ae:
            suit = StepSuit(self.steps, collect.scrapers)
        assert 'StepSuit need a Scraper Instance.' in str(ae.exception)

    def test_method_suit_activate(self):
        """
        initialize steps and activate scraper instance.
        """
        # suit = StepSuit([], self.scraper)
        suit = StepSuit(self.steps, self.scraper)

        assert suit.scraper.activated is False
        assert suit.steps is None

        suit.suit_activate()
        assert suit.scraper.activated is True
        assert suit.steps is not None

        assert len(suit.steps) == 4

    def test_method_suit_exit(self):
        """
        TODO: step instance exit.
        """
        suit = StepSuit(self.steps, self.scraper)
        suit.suit_activate()

        assert suit.scraper.activated is True
        assert suit.steps is not None

        suit.suit_exit()
        assert suit.scraper.activated is False

    # 太弱智就不写了
    def test_property_scraper(self):
        pass

    def test_property_steps(self):
        pass


if __name__ == '__main__':
    unittest.main()
