import unittest

from ScrapyUtils.components import StepSuit, Action, Step, ComponentSuit


class ActionTest(Action):
    pass


class StepSuitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.suit = StepSuit()

    def test_sample(self):
        assert issubclass(StepSuit, ComponentSuit)
        assert isinstance(self.suit, ComponentSuit)

    def test_attribute_components_default(self):
        """Default attribute components: []"""

        assert self.suit.components == []

    def test_attribute_target_component_default(self):
        """Default attribute target_component s: Step"""

        assert self.suit.target_components == Step

    def test_attribute_context_default(self):
        """Default attribute target_components: {}"""

        assert self.suit.context == {}

    def test_attribute_scraper_default(self):
        """Default attribute scraper: {}"""

        assert self.suit.scraper == None

    def test_method_set_scraper(self):
        """Method set_scraper for suit"""
        from ScrapyUtils.libs import RequestScraper

        r = RequestScraper()
        r.scraper_attach()

        assert self.suit.scraper == None
        self.suit.set_scraper(r)
        assert self.suit.scraper == r

    def test_method_set_scraper_auto_attach(self):
        """Method set_scraper will attach scraper if hasn't attached."""
        from ScrapyUtils.libs import RequestScraper

        r = RequestScraper()

        assert self.suit.scraper == None
        self.suit.set_scraper(r)

        assert self.suit.scraper == r
        assert self.suit.scraper.attached == True

    def test_method_add_component(self):
        """Method add_component will append step into suit.components"""

        assert self.suit.components == []
        res = self.suit.add_component(ActionTest)

        assert res

        assert len(self.suit.components) == 1
        assert self.suit.components[0].__class__ == ActionTest

    def test_method_add_component_wrong_type(self):
        """If add a wrong object the method will skip and return None"""

        res = self.suit.add_component(dict())

        assert not res
        assert res == None

    def test_method_generate(self):
        """TODO:"""
        assert False

    def test_method_generate_error(self):
        """TODO:"""
        assert False

    def test_function_do_scraper(self):
        """TODO:"""
        assert False

    def test_function_do_scraper_error(self):
        """TODO:"""
        assert False


if __name__ == '__main__':
    unittest.main()

