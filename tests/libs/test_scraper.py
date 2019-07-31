from unittest import TestCase, skip

from base.libs import Scraper, RequestScraper

import requests


# class RequestScraper(object):
#
#     def __init__(self):
#         self._req = requests.Session()
#         pass
#
#     def get(self):
#         pass
#
#     pass


class TestScraper(TestCase):

    def test_test(self):
        pass

    def test_init(self):
        r = RequestScraper()
        r.get('http://127.0.0.1:8090/mock/get')
        pass

    pass
