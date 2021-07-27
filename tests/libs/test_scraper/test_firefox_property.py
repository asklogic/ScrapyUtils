import unittest

from ScrapyUtils.libs import FireFoxScraper
from selenium.webdriver import Firefox, FirefoxOptions


class FirefoxPropertyTestCase(unittest.TestCase):
    """Testcase without attach."""

    @classmethod
    def setUpClass(cls) -> None:
        f = FireFoxScraper(headless=True)
        # f.scraper_attach()
        cls.f = f

    def setUp(self) -> None:
        self.scraper = FireFoxScraper()

    def test_property_attached(self):
        """Property attached: default False """
        self.assertFalse(self.scraper.attached)

    # mixin
    def test_property_options(self):
        """Property options is FirefoxOptions instance"""
        self.assertIsInstance(self.scraper.options, FirefoxOptions)

    def test_property_binary(self):
        """Property binary is FirefoxOptions instance"""
        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

        self.assertIsNotNone(self.scraper.binary)
        self.assertIsInstance(self.scraper.binary, FirefoxBinary)

        # TODO: binary or options.binary
        self.scraper.options.binary = self.scraper.binary
        # print(self.scraper.options.binary_location)
        self.assertIsInstance(self.scraper.options.binary, FirefoxBinary)

    def test_property_driver_path(self):
        """Property driver_path is path of WebDriver: default is firefox/geckodriver.exe or firefox/geckodriver if Linux"""
        import platform
        if 'Win' in platform.system():
            self.assertEqual(self.scraper.driver_path, r'firefox\geckodriver.exe')

    def test_mixin_method_set_headless(self):
        """Method of headless mixin, change the property of firefox_options and WebDriver will attach in headless"""
        self.scraper.set_headless(False)
        self.assertFalse(self.scraper.options.headless)

        self.scraper.set_headless(True)
        self.assertTrue(self.scraper.options.headless)

    def test_mixin_method_set_image(self):
        """Method of mixin, options.set_preference."""
        pass

    def test_mixin_method_set_javascript(self):
        """Method of mixin, options.set_preference."""
        pass

    def test_mixin_property_timeout_default(self):
        """Property of timeout mixin, the timeout of page and scripts, default is 10"""
        self.assertEqual(self.scraper.timeout, 10)

    def test_mixin_method_set_timeout(self):
        """Method of timeout mixin"""
        self.scraper.set_timeout(5)
        self.assertEqual(self.scraper.timeout, 5)
        pass

    def test_argument_headless(self):
        """Argument headless, default is False"""
        self.assertFalse(self.scraper.options.headless)

        scraper = FireFoxScraper(headless=True)
        self.assertTrue(scraper.options.headless)

    def test_argument_image(self):
        """TODO: Argument image, default is False"""

    def test_argument_js(self):
        """TODO: Argument image, default is False"""

    # @unittest.skip
    def test_argument_attach(self):
        """Argument attach, default is False"""
        scraper = FireFoxScraper(headless=True, attach=True)

        self.assertTrue(scraper.attached)
        self.assertIsNotNone(scraper.firefox)


if __name__ == '__main__':
    unittest.main()
