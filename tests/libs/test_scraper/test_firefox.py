import unittest
import os

from ScrapyUtils.libs.scraper.firefox_scraper import FireFoxScraper
from ScrapyUtils.libs.scraper.firefox_scraper import set_firefox_path, set_driver_path, exit_all_firefox_webdriver
from tests.test_switch import firefox_scraper_switch, http_switch

cookie_test_url = 'http://httpbin.org/cookies'
driver_path = os.path.join('firefox', 'geckodriver.exe')


@unittest.skipUnless(condition=firefox_scraper_switch and http_switch, reason='start firefox browser')
class FirefoxTestCase(unittest.TestCase):
    scraper: FireFoxScraper

    def setUp(self) -> None:
        set_driver_path(driver_path)

    @classmethod
    def tearDownClass(cls) -> None:
        exit_all_firefox_webdriver()

    def test_method_attach_common(self):
        """Methods in scraper attach"""
        scraper = FireFoxScraper()

        with self.subTest(msg='scraper attach'):
            assert scraper.attached is False
            scraper.scraper_attach()
            assert scraper.attached is True

        with self.subTest(msg='scraper get'):
            content = scraper.get(r'https://httpbin.org/get')
            assert 'headers' in content

        with self.subTest(msg='scraper get driver'):
            from selenium.webdriver import Firefox
            self.assertIsInstance(self.scraper.get_driver(), Firefox)

        with self.subTest(msg='scraper detach'):
            assert scraper.attached is True
            scraper.scraper_detach()
            assert scraper.attached is False

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
