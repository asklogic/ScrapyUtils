import unittest

from base.libs import Scraper, RequestScraper, FireFoxScraper
import json


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.r = RequestScraper()
        self.r.scraper_activate()

    def test_request_header(self):
        """
        RequestScraper custom headers
        """
        r = self.r

        # default header
        assert len(r.headers) is 7

        h = r.headers
        header: dict = json.loads(r.get('http://127.0.0.1:8090/mock/header'))

        # add host
        assert len(header) is 8
        assert header.get('Custom') is None

        # update headers.
        r.headers = {'custom': 'custom value'}
        assert len(r.headers) is 1
        header: dict = json.loads(r.get('http://127.0.0.1:8090/mock/header'))

        # server add header
        assert len(header) is 9
        assert header.get('Custom') is not None
        assert header.get('Custom') == 'custom value'

        # restart.
        r.restart()
        assert len(r.headers) is 1
        header: dict = json.loads(r.get('http://127.0.0.1:8090/mock/header'))

        # server add host and encoding.
        assert len(header) is 3

        r.headers = None
        r.restart()

        # keep alive

        header: dict = json.loads(r.get('http://127.0.0.1:8090/mock/header'))

        assert r.keep_alive is True
        assert r.headers.get('Connection') == 'keep-alive'
        assert header.get('Connection') == 'keep-alive'

        r.keep_alive = False
        header: dict = json.loads(r.get('http://127.0.0.1:8090/mock/header'))

        assert r.keep_alive is False
        assert r.headers.get('Connection') == 'close'
        assert header.get('Connection') == 'close'

    def test_request_proxy(self):
        pass

    def test_get_200(self):
        content = self.r.get('http://127.0.0.1:8090/mock/get')
        assert 'success info' in content

    def test_get_400(self):
        # TODO custom exception
        with self.assertRaises(Exception) as e:
            content = self.r.get('http://127.0.0.1:8090/mock/error')

        assert 'RequestScraper http status failed' in str(e.exception)
        assert '403' in str(e.exception)

        content = self.r.get('http://127.0.0.1:8090/mock/error', status=500)
        assert '403 failed' in content

    def test_request_post(self):
        data = {'post_data': 'the post data'}

        with self.assertRaises(Exception) as e:
            self.r.post('http://127.0.0.1:8090/mock/get', data=data)
        assert '405' in str(e.exception)

        # FIXME: request session's data
        content = self.r.post('http://127.0.0.1:8090/mock/post/data', data=data)

        assert 'the post data' in content


if __name__ == '__main__':
    unittest.main()
