import unittest

from ScrapyUtils.libs.scraper.request_scraper import RequestScraper

headers = {
    'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/json,text/plain,*/*,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    "Content-Type": "application/x-www-form-urlencoded",
    # 'Connection': 'close',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}


class RequestScraperTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.scraper = RequestScraper()
        self.scraper.scraper_attach()

    def test_scraper_attached(self):
        """Property attached: default to False """
        scraper = RequestScraper()
        assert scraper.attached is False

    def test_property_session(self):
        """Property session (Session): default is None"""
        scraper = RequestScraper()
        assert scraper.session is None

    def test_scraper_method_attach(self):
        """scraper_attach will create Session instance."""
        scraper = RequestScraper()
        scraper.scraper_attach()

        from requests import Session
        assert isinstance(self.scraper.session, Session)

    def test_mixin_method_get(self):
        """Http get"""

        assert self.scraper.last_response is None
        content = self.scraper.get(r'https://httpbin.org/get')

        assert self.scraper.last_response is not None


if __name__ == '__main__':
    unittest.main()
