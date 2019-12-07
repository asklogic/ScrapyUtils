import unittest

from base.libs import Scraper, RequestScraper, FireFoxScraper
import json


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.r = RequestScraper()
        self.r.scraper_activate()

    def test_request_header(self):
        """
        RequestScraper custom headers.
        """

        # default header.
        assert len(self.r.headers) is 7

        h = self.r.headers
        header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))

        # Flask test server add host.
        assert len(header) is 8

    def test_request_header_update(self):
        """
        add new header. Session update the header.
        """

        # update headers.
        self.r.headers = {'custom': 'custom value'}
        assert len(self.r.headers) is 1
        header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))

        # server add header
        assert len(header) is 9
        assert header.get('Custom') is not None
        assert header.get('Custom') == 'custom value'

    def test_request_header_restart(self):
        """
        custom header activated when RequestScraper restart.
        """

        self.r.headers = {}

        # restart.
        self.r.restart()
        assert len(self.r.headers) is 0
        header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))

        # Flask test server add host and encoding.
        assert len(header) is 2

    def test_request_keep_alive(self):
        """
        property keep_alive. update scraper's header.
        """

        header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))

        # default.
        assert self.r.keep_alive is True
        assert self.r.headers.get('Connection') == 'keep-alive'
        assert header.get('Connection') == 'keep-alive'

        # modify keep_alive.
        self.r.keep_alive = False
        header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))

        assert self.r.keep_alive is False
        assert self.r.headers.get('Connection') == 'close'
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

    def test_get_400_accept(self):
        # TODO. to range.
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
