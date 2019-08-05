from unittest import TestCase, skip

from base.libs import Scraper, RequestScraper, FireFoxScraper, Proxy

import requests
import json


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

    def setUp(self) -> None:
        super().setUp()
        r = RequestScraper()
        r.scraper_activate()
        self.r = r

    @skip
    def test_test(self):
        def lived(func):
            def wrapper(*args, **kwargs):
                obj = args[0]
                if not obj.alive:
                    raise Exception('not alive')
                res = func(*args, **kwargs)

                return res

            return wrapper

        class Test():
            alive = False

            @lived
            def do(self):
                return 1

        t = Test()
        t.alive = True
        self.assertEqual(t.do(), 1)

    # property
    def test_init(self):
        r = RequestScraper()

        # default
        self.assertEqual(r.activated, False)

        with self.assertRaises(Exception) as e:
            self.assertIn("hasn't activated", str(e.exception))
            r.get('http://127.0.0.1:8090/mock/get')

        r.scraper_activate()
        self.assertEqual(r.activated, True)

        r.get('http://127.0.0.1:8090/mock/get')

        pass

    # feature
    def test_400_page(self):
        '''
        http state: 400
        '''
        r = RequestScraper()
        r.scraper_activate()
        with self.assertRaises(Exception) as e:
            # TODO custom exception
            r.get('http://127.0.0.1:8090/mock/error')

        r.get('http://127.0.0.1:8090/mock/error', status=500)

    def test_request_header(self):
        r = self.r

        # header update
        r.headers = {'custom': 'custom value'}
        content = r.get('http://127.0.0.1:8090/mock/header')
        header = json.loads(content)
        self.assertEqual(header['Custom'], 'custom value')

        # keep alive
        self.assertEqual(header['Connection'], 'keep-alive')
        r.keep_alive = False
        content = r.get('http://127.0.0.1:8090/mock/header')
        header = json.loads(content)
        self.assertEqual(header['Connection'], 'close')

    def test_request_post(self):
        # TODO
        pass

    def test_firefox_init(self):
        f = FireFoxScraper()
        # f.scraper_activate()
        pass
