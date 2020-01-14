import unittest
import requests

from base.libs import Scraper, RequestScraper, Proxy


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        proxy = Proxy(ip='1.1.1.1', port='336')
        assert proxy.ip == '1.1.1.1'
        self.proxy = proxy

        self.r = RequestScraper()

    def test_property_activate(self):
        self.r.scraper_activate()

        assert self.r.activated is True

    def test_property_activate_default(self):
        assert self.r.activated is False

    # TODO: proxy_setter and get_proxy
    def test_property_proxy_default(self):
        assert self.r.proxy == {}

    def test_property_proxy_setter(self):
        self.r.proxy = self.proxy
        assert self.r.proxy != {}

    def test_property_header(self):
        """
        to test_request.py
        """

    def test_property_keep_alive(self):
        """
        to test_request.py
        """

    def test_property_req(self):
        assert self.r.req is None

        self.r.scraper_activate()

        assert self.r.req is not None

    def test_property_current(self):
        assert self.r.current is None

        self.r.scraper_activate()
        self.r.get('http://httpbin.org/')

        assert self.r.current is not None

    def test_proeprty_current_change(self):
        self.r.scraper_activate()
        self.r.get('http://httpbin.org/')
        assert self.r.current.url == 'http://httpbin.org/'

        self.r.get('http://httpbin.org/cookies')
        assert self.r.current.url == 'http://httpbin.org/cookies'

    def test_property_scheme(self):
        assert self.r.schemes == ['get', 'post']

    def test_method_activate(self):
        r: RequestScraper = RequestScraper()

        r.scraper_activate()

        assert r.activated is True
        assert r.req is not None
        assert isinstance(r.req, requests.Session)

    def test_method_activate_again(self):
        r = RequestScraper()
        r.scraper_activate()

        with self.assertRaises(Exception) as e:
            r.scraper_activate()
        assert 'Scraper must be not activated.' == str(e.exception)

        # def test_activate(self):

    #     """
    #     scraper methods
    #     """
    #     r = RequestScraper()
    #
    #     assert r.activated is False
    #
    #     with self.assertRaises(Exception) as e:
    #         r.scraper_clear()
    #
    #     with self.assertRaises(Exception) as e:
    #         r.scraper_quit()
    #
    #     with self.assertRaises(Exception) as e:
    #         r.get('http://127.0.0.1:8090/mock/get')
    #
    #     # ----------------------------------------------------------------------
    #
    #     r.scraper_activate()
    #     r.scraper_clear()
    #     r.get('http://127.0.0.1:8090/mock/get')
    #     r.scraper_quit()

    # def test_property_keep_alive_modify(self):
    #     r = RequestScraper()
    #
    #     r.keep_alive = False
    #
    #     assert r.keep_alive is False
    #     assert r.headers.get('Connection') == 'close'
    #
    #     r.keep_alive = True
    #     assert r.keep_alive is True
    #     assert r.headers.get('Connection') == 'keep-alive'

    def test_method_quit(self):
        """
        TODO : session's adapter closed.
        """
        r: RequestScraper = RequestScraper()
        r.scraper_activate()
        r.scraper_quit()

        assert r.req is not None

    def test_method_quit_again(self):

        r = RequestScraper()
        r.scraper_activate()

        r.scraper_quit()
        r.scraper_quit()

    def test_method_restart(self):
        r = RequestScraper()

        r.scraper_activate()

        id1 = id(r.req)

        r.scraper_clear()

        id2 = id(r.req)

        assert id1 != id2

    def test_method_get_requests(self):
        assert self.r.get_requests() is self.r.req

if __name__ == '__main__':
    unittest.main()
