from typing import *

from ScrapyUtils.libs import Scraper

try:
    from requests import Session, Response
except ImportError as e:
    # TODO: libs log
    pass

default_headers = {
    'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/json,text/plain,*/*,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Language': 'en-us',
    "Content-Type": "application/x-www-form-urlencoded",
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}


class RequestSettingMixin(object):
    _headers: Dict[str, str] = None
    _keep_alive: bool = True

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, value):
        if type(value) is dict:
            self._headers = value
        else:
            self._headers = default_headers

    @property
    def keep_alive(self):
        return self._keep_alive

    @keep_alive.setter
    def keep_alive(self, value):
        if value:
            self.headers['Connection'] = 'keep-alive'
            self._keep_alive = True

        else:
            self.headers['Connection'] = 'close'
            self._keep_alive = False


class RequestScraper(Scraper, RequestSettingMixin):
    current: Response = None
    req: Session = None

    def __init__(self, headers: dict = None, **kwargs):
        self.headers = headers if headers else default_headers.copy()

        super(RequestScraper, self).__init__(**kwargs)

    def _attach(self) -> NoReturn:
        """
        Create the requests.Session instance.

        Modify session in RequestSettingMixin.
        Session.keep_alive : True
        Session.headers : default_header
        """
        req = Session()

        req.keep_alive = self.keep_alive
        req.headers = self.headers

        self.req = req

    def _detach(self) -> NoReturn:
        """
        Close the requests.Session adapters.
        """
        self.req.close()

    def _clear(self):
        """
        Clear: restart it.
        """
        self.scraper_restart()

    def get_driver(self) -> Session:
        """
        requests.Session.
        """
        return self.req
