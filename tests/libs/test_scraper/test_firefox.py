import unittest

from ScrapyUtils.libs.scraper.firefox_scraper import FireFoxScraper
from ScrapyUtils.libs.scraper.firefox_scraper import set_firefox_path, set_driver_path, exit_all_firefox_webdriver
from tests.libs.test_scraper import cookie_test_url


class MyTestCase(unittest.TestCase):
    scraper: FireFoxScraper

    @classmethod
    def setUpClass(cls) -> None:
        set_firefox_path(r'firefox\App\Firefox\firefox.exe')

        cls.scraper = FireFoxScraper(headless=False)
        cls.scraper.scraper_attach()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.scraper.scraper_detach()
        exit_all_firefox_webdriver()

    def test_method_get(self):
        """Method from http mixin"""
        content = self.scraper.get(r'http://127.0.0.1:9009/test/get')
        assert 'success mock get.' in content

    def test_scraper_property_attached(self):
        """Property from scraper"""
        self.assertTrue(self.scraper.attached)

    def test_scraper_method_detach(self):
        """Method from scraper"""
        scraper = FireFoxScraper(headless=False, attach=True)
        self.assertTrue(scraper.attached)

        scraper.scraper_detach()

        self.assertFalse(scraper.attached)

    def test_scraper_method_get_driver(self):
        """Method from scraper, return the webdriver instance"""
        from selenium.webdriver import Firefox

        self.assertIsInstance(self.scraper.get_driver(), Firefox)

    def test_scraper_method_clear(self):
        """Method from scraper"""
        scraper = FireFoxScraper(headless=False, attach=True)
        scraper.get(cookie_test_url)

        self.assertIsNotNone(scraper.get_driver().get_cookies())

        scraper.scraper_clear()

        self.assertEqual(scraper.get_driver().get_cookies(), [])

    def test_scraper_method_restart(self):
        """Method from scraper"""
        scraper = FireFoxScraper(headless=False, attach=True)
        scraper.get(cookie_test_url)

        self.assertIsNotNone(scraper.get_driver().get_cookies())

        scraper.scraper_restart()

        self.assertEqual(scraper.get_driver().get_cookies(), [])
        self.assertEqual(scraper.get_driver().current_url, r'about:blank')


if __name__ == '__main__':
    unittest.main()
