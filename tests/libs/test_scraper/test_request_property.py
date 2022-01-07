import unittest
import requests

from ScrapyUtils.libs.scraper.request_scraper import Scraper, RequestScraper


class RequestScraperPropertyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.r = RequestScraper()

    def test_mixin_property_timeout(self):
        """Common mixin property: timeout. Default is 10"""

        assert self.r.timeout == 10

    def test_mixin_method_set_timeout(self):
        """Common mixin method set_timeout"""
        timeout = 30

        self.r.set_timeout(timeout)
        assert self.r.timeout == timeout

    def test_mixin_property_headers(self):
        """Requests mixin Property: headers"""
        assert self.r.headers is not None

        assert len(self.r.headers) == 7

    def test_mixin_method_set_headers(self):
        """Requests mixin method set_headers"""

        headers = {
            'test_key': 'test_value'
        }
        self.r.set_headers(headers)

        assert self.r.headers == headers

        self.r.scraper_attach()
        assert self.r.session.headers == headers

    def test_mixin_keep_alive(self):
        """Requests mixin property: keep_alive. Default is True"""

        assert self.r.keep_alive == True

    def test_mixin_method_keep_alive(self):
        """Requests method set_keep_alive"""

        self.r.set_keep_alive(False)
        assert self.r.keep_alive is False


if __name__ == '__main__':
    unittest.main()
