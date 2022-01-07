import unittest

from ScrapyUtils.libs import Scraper


class ScraperTestCase(unittest.TestCase):
    def test_initial(self):
        Scraper()

    def test_initial_attach(self):
        """Initial with scraper_attach()"""
        scraper = Scraper(attach=True)

        assert scraper.attached is True

    def test_attribute_activated(self):
        """The default attached is False."""
        scraper = Scraper()

        assert scraper.attached is False

    def test_method_attach(self):
        """Scraper attach method to create driver.

        The state attached will be True.
        """
        scraper = Scraper()

        scraper.scraper_attach()

        assert scraper.attached is True

    def test_method_detach(self):
        """Scraper detach method to destroy driver."""
        scraper = Scraper()
        scraper.scraper_attach()
        assert scraper.attached is True

        scraper.scraper_detach()

        assert scraper.attached is False

    def test_scraper_method_chaining(self):
        """Scraper's method"""
        scraper = Scraper()
        assert isinstance(scraper.scraper_attach(), Scraper)
        assert isinstance(scraper.scraper_detach(), Scraper)
        assert isinstance(scraper.scraper_clear(), Scraper)
        assert isinstance(scraper.scraper_restart(), Scraper)


if __name__ == '__main__':
    unittest.main()
