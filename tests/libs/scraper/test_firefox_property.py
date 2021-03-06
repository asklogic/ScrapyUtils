import unittest

from base.libs import FireFoxScraper, Scraper, Proxy
from selenium.webdriver import Firefox, FirefoxOptions


class FirefoxPropertyTestCase(unittest.TestCase):
    f = None

    @classmethod
    def setUpClass(cls) -> None:
        f = FireFoxScraper(headless=False)
        f.scraper_activate()
        cls.f = f

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.f.scraper_quit()

    def test_init(self):
        pass

    def test_scraper_init(self):
        f = FireFoxScraper()

        # scraper

        assert f.proxy is None
        assert f._proxy is None
        assert f.timeout == 10
        assert f._timeout == 10
        assert f.activated is False
        assert f._activated is False

        # firefox

        assert f.image is False
        assert f._image is False
        assert f.headless is True
        assert f._headless is True

        assert f.firefox is None
        assert f.options is not None
        assert isinstance(f.options, FirefoxOptions)

        assert f.schemes == ['get']

    def test_activate(self):
        f = self.f

        assert f.activated is True
        assert f.firefox is not None

        assert isinstance(f.firefox, Firefox)

        f.scraper_clear()
        f.get('http://127.0.0.1:8090/mock/get')

        # self.f is static property.
        # f.scraper_quit()

    def test_activate_exception(self):
        f = FireFoxScraper()

        with self.assertRaises(Exception) as e:
            f.scraper_clear()

        with self.assertRaises(Exception) as e:
            f.get('http://127.0.0.1:8090/mock/get')

    def test_scraper_proxy(self):
        # TODO: proxy

        proxy_info = '116.140.24.128:11371'
        proxy = Proxy(ip=proxy_info.split(':')[0], port=proxy_info.split(':')[1])
        # f.proxy = proxy

        self.f.proxy = proxy

    def test_property_proxy_default(self):
        assert self.f.proxy == None

    def test_property_proxy_set(self):
        proxy_info = '117.30.209.184:32846'
        proxy = Proxy(ip=proxy_info.split(':')[0], port=proxy_info.split(':')[1])

        self.f.proxy = proxy

        assert self.f.proxy != None
        assert self.f.proxy.ip == '117.30.209.184'
        assert self.f.proxy.port == '32846'

    @unittest.skip
    def test_property_proxy_get(self):

        proxy_info = '14.115.205.182:34975'
        proxy = Proxy(ip=proxy_info.split(':')[0], port=proxy_info.split(':')[1])

        self.f.proxy = proxy


        content = self.f.get('http://ip.tool.chinaz.com/')

        assert self.f.proxy.ip in content


if __name__ == '__main__':
    unittest.main()
