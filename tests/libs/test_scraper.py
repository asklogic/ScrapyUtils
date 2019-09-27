from unittest import TestCase, skip

from base.libs import Scraper, RequestScraper, FireFoxScraper, Proxy

import requests
import json


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

    # RequestScraper test case

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

        content = r.get('http://127.0.0.1:8090/mock/get')
        assert 'success info' in content

    # custom header
    def test_request_header(self):
        """
        RequestScraper custom headers
        """
        r = self.r

        # update headers
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

    # http status
    def test_400_response(self):
        """
        http state: 400
        raise Exception if http response status greater than status code in get method
        default status is 300
        """
        r = self.r

        with self.assertRaises(Exception) as e:
            r.get('http://127.0.0.1:8090/mock/error')

        # TODO custom exception
        assert 'RequestScraper http status failed' in str(e.exception)
        assert '403' in str(e.exception)

        content = r.get('http://127.0.0.1:8090/mock/error', status=500)
        assert '403 failed' in content

    def test_500_response(self):
        r = self.r

        with self.assertRaises(Exception) as e:
            r.get('http://127.0.0.1:8090/mock/failed')

        assert 'RequestScraper http status failed' in str(e.exception)
        assert '503' in str(e.exception)

        content = r.get('http://127.0.0.1:8090/mock/failed', status=600)
        assert '503 failed' in content

    # @skip
    def test_request_post(self):
        r = self.r
        data = {'post_data': 'the post data'}

        with self.assertRaises(Exception) as e:
            r.post('http://127.0.0.1:8090/mock/get', data=data)
        assert '405' in str(e.exception)

        # FIXME: request session's data
        content = r.post('http://127.0.0.1:8090/mock/post/data', data=data)

        assert 'the post data' in content

    # FireFoxScraper test case

    # TODO : block or await
    def test_firefox_init(self):
        f = FireFoxScraper()
        # f.headless = False

        with self.assertRaises(Exception) as e:
            self.assertIn("hasn't activated", str(e.exception))
            f.get('http://127.0.0.1:8090/mock/get')

        f.scraper_activate()
        self.assertEqual(f.activated, True)

        content = f.get('http://127.0.0.1:8090/mock/get')
        assert 'success info' in content
