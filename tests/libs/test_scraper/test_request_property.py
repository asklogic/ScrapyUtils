import unittest
import requests

from ScrapyUtils.libs import Scraper, RequestScraper, Proxy


class RequestScraperPropertyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        proxy = Proxy(ip='101.101.101.101', port='336')
        self.proxy = proxy

        self.r = RequestScraper()


if __name__ == '__main__':
    unittest.main()
