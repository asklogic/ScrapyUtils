import unittest

from ScrapyUtils.libs.scraper.firefox_scraper import FireFoxScraper, set_firefox_path, set_driver_path


class MyTestCase(unittest.TestCase):
    scraper: FireFoxScraper

    @classmethod
    def setUpClass(cls) -> None:
        cls.scraper = FireFoxScraper(headless=True)
        cls.scraper.scraper_attach()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.scraper.scraper_detach()

    def test_method_get(self):
        """Method from http mixin"""
        content = self.scraper.get(r'http://127.0.0.1:9009/test/get')
        assert 'success mock get.' in content

    def test_scraper_property_attached(self):
        """Property from scraper"""
        self.assertTrue(self.scraper.attached)

    def test_scraper_method_detach(self):
        """Method from scraper"""
        scraper = FireFoxScraper(headless=True, attach=True)
        self.assertTrue(scraper.attached)

        scraper.scraper_detach()

        self.assertFalse(scraper.attached)

    def test_scraper_method_get_driver(self):
        """Method from scraper, return the webdriver instance"""
        from selenium.webdriver import Firefox

        self.assertIsInstance(self.scraper.get_driver(), Firefox)


if __name__ == '__main__':
    unittest.main()
