import unittest

from ScrapyUtils.libs import RequestScraper
import json

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
        self.r = RequestScraper()
        self.r.scraper_attach()

    def test_initial(self):
        RequestScraper()

    def test_initial_param_header(self):
        mock_headers = {
            'key_0': 'value_0'
        }

        r = RequestScraper(headers=mock_headers)

    def test_case_default_header(self):
        """RequestScraper custom headers."""

        # default header.
        assert len(self.r.headers) is 7
        assert self.r.headers == headers

        # same header
        assert self.r.headers is self.r.req.headers

    def test_case_get_header(self):
        """get true header that server will accept."""

        print(self.r.headers)

        header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))

        # Flask test server add host.
        assert len(header) is 8

    def test_request_header_update(self):
        """add new header. Session update the header."""

        # update headers.
        self.r.headers = {'custom': 'custom value'}
        assert len(self.r.headers) is 1
        header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))

        # server add header
        print(len(header))
        assert len(header) is 9
        assert header.get('Custom') is not None
        assert header.get('Custom') == 'custom value'

    def test_request_header_restart(self):
        """custom header activated when RequestScraper restart."""
        scraper = RequestScraper()
        scraper.scraper_attach()

        scraper.headers = {}

        # restart.
        scraper.scraper_restart()
        assert len(scraper.headers) is 0
        assert len(scraper.get_driver().headers) is 0
        header: dict = json.loads(scraper.get('http://127.0.0.1:8090/mock/header'))

        # Flask test server add host and encoding.
        print(header)
        assert len(header) is 2
    #
    # @unittest.skip
    # def test_request_keep_alive(self):
    #     """property keep_alive. update scraper's header."""
    #
    #     header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))
    #
    #     # default.
    #     assert self.r.keep_alive is True
    #     assert self.r.headers.get('Connection') == 'keep-alive'
    #     assert header.get('Connection') == 'keep-alive'
    #
    #     # modify keep_alive.
    #     self.r.keep_alive = False
    #     header: dict = json.loads(self.r.get('http://127.0.0.1:8090/mock/header'))
    #
    #     assert self.r.keep_alive is False
    #     assert self.r.headers.get('Connection') == 'close'
    #     assert header.get('Connection') == 'close'
    #
    # def test_request_proxy(self):
    #     pass
    #
    def test_case_get_200(self):
        content = self.r.get('http://127.0.0.1:8090/mock/get')
        assert 'success info' in content

    def test_case_get_400(self):
        # TODO custom exception
        with self.assertRaises(Exception) as e:
            content = self.r.get('http://127.0.0.1:8090/mock/error')

        assert 'RequestScraper http status Exception' in str(e.exception)
        assert '403' in str(e.exception)

    def test_case_get_400_accept(self):
        # TODO. to range.
        content = self.r.get('http://127.0.0.1:8090/mock/error', status_limit=500)
        assert '403 failed' in content

    def test_method_request_post(self):
        data = {'post_data': 'the post data'}

        with self.assertRaises(Exception) as e:
            self.r.post('http://127.0.0.1:8090/mock/get', data=data)
        assert '405' in str(e.exception)

        # FIXME: request session's data
        content = self.r.post('http://127.0.0.1:8090/mock/post/data', data=data)

        assert 'the post data' in content


if __name__ == '__main__':
    unittest.main()
