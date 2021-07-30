import unittest

from ScrapyUtils.libs import Scraper


class ScraperTestCase(unittest.TestCase):
    def test_import(self):
        from ScrapyUtils.libs import Scraper

    def test_initial(self):
        Scraper()

    def test_initial_attach(self):
        scraper = Scraper(attach=True)

        assert scraper.attached is True


    def test_attribute_activated(self):
        """The default attached is False.
        """

        scraper = Scraper()

        assert scraper._attached is False
        assert scraper.attached is False

    def test_method_attach(self):
        """Scraper attach method to create driver.

        The state attached will be True.
        """
        scraper = Scraper()

        scraper.scraper_attach()

        assert scraper.attached is True

    def test_method_detach(self):
        """Scraper detach method to destroy driver.

          The state attached will be Fasle.
          """
        scraper = Scraper()
        scraper.scraper_attach()
        assert scraper.attached is True

        scraper.scraper_detach()

        assert scraper.attached is True



if __name__ == '__main__':
    unittest.main()
