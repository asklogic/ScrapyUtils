import unittest

from base.libs import Scraper, RequestScraper, Proxy


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        proxy = Proxy(ip='1.1.1.1', port='336')
        assert proxy.ip == '1.1.1.1'
        self.proxy = proxy

    def test_activate(self):
        """
        scraper methods
        """
        r = RequestScraper()

        with self.assertRaises(Exception) as e:
            r.scraper_clear()

        with self.assertRaises(Exception) as e:
            r.scraper_quit()

        with self.assertRaises(Exception) as e:
            r.get('http://127.0.0.1:8090/mock/get')

        # ----------------------------------------------------------------------

        r.scraper_activate()
        r.scraper_clear()
        r.get('http://127.0.0.1:8090/mock/get')
        r.scraper_quit()

    def test_request_init(self):
        r = RequestScraper()

        # scraper

        assert r.proxy == {}
        assert r._proxy is None
        assert r.timeout == 10
        assert r._timeout == 10
        assert r.activated is False
        assert r._activated is False

        # request

        assert r.headers != {}
        assert isinstance(r.headers, dict)
        assert isinstance(r._headers, dict)
        assert r.keep_alive is True
        assert r._keep_alive is True

        assert r.req is None
        assert r.current is None
        assert r.schemes == ['get', 'post']

    def test_request_proxy(self):
        r = RequestScraper()

        assert r.proxy == {}
        r.proxy = self.proxy
        assert r.proxy != {}

    def test_property_header(self):
        r = RequestScraper()
        assert isinstance(r.headers, dict)

    def test_property_keep_alive(self):
        r = RequestScraper()

        # default : True
        assert r.keep_alive is True
        assert r.headers.get('Connection') == 'keep-alive'

        r.keep_alive = False

        assert r.keep_alive is False
        assert r.headers.get('Connection') == 'close'

        r.keep_alive = True
        assert r.keep_alive is True
        assert r.headers.get('Connection') == 'keep-alive'

    def test_scraper_activate(self):
        r: RequestScraper = RequestScraper()

        assert r.activated is False
        assert r.req is None
        assert r.current is None

        r.scraper_activate()

        assert r.activated is True
        assert r.req is not None

        import requests
        assert isinstance(r.req, requests.Session)

    def test_scraper_quit(self):
        r: RequestScraper = RequestScraper()

        assert r.req is None

        r.scraper_activate()

        assert r.req is not None

        r.scraper_quit()
        assert r.req is not None

    def test_scraper_restart(self):
        r = RequestScraper()

        r.scraper_activate()

        id1 = id(r.req)

        r.scraper_clear()

        id2 = id(r.req)

        assert id1 != id2

    def test_scraper_activate_again(self):
        r = RequestScraper()
        r.scraper_activate()

        with self.assertRaises(Exception) as e:
            r.scraper_activate()

    def test_scraper_quit_again(self):
        r = RequestScraper()
        r.scraper_activate()

        r.scraper_quit()
        with self.assertRaises(Exception) as e:
            r.scraper_quit()


if __name__ == '__main__':
    unittest.main()
