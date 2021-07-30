# -*- coding: utf-8 -*-
"""Request scraper module.

RequestScraper Bases on Requests.Session and support some common methods.

RequestScraper is the default scraper of ScrapyUtils.

默认Scraper，如果不设置自定义Scraper将默认启动RequestScraper.

Todo:
    * log out.
    * RequestsScraper proxy, timeout mixin.
    * unittest.

"""
from copy import deepcopy
from typing import *

from ScrapyUtils.libs.scraper import Scraper

try:
    from requests import Session, Response

    from requests import adapters, packages
    from urllib3.exceptions import InsecureRequestWarning

    # default common setting.
    adapters.DEFAULT_RETRIES = 5
    packages.urllib3.disable_warnings(InsecureRequestWarning)
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


class RequestsBase:
    timeout: Union[int, float] = 10
    headers: Dict[str, str] = {}
    req: Session = None


class RequestsKeepAliveMixin(RequestsBase):
    _keep_alive: bool = True

    def set_keep_alive(self, state: bool):
        self._keep_alive = bool(state)
        self.headers['Connection'] = 'keep-alive' if bool(state) else 'close'


class RequestsHeadersMixin(RequestsBase):
    _headers = deepcopy(default_headers)

    def set_headers(self, headers: Dict[str, str]):
        self._headers = headers if headers else default_headers.copy()


class RequestsTimeoutMixin(RequestsBase):
    timeout = 10

    def set_timeout(self, timeout: Union[int, float] = 10):
        self.timeout = timeout


class RequestHttpMixin(RequestsBase):
    current: Response = None
    req: Session = None

    def get(self, url: str, params: Dict = None, timeout: int = None, status_limit: int = 400):
        timeout = timeout if timeout else self.timeout

        response = self.req.get(url=url, timeout=timeout, params=params, headers=self.headers,
                                stream=False, verify=False)

        self.current = response
        if response.status_code > status_limit:
            raise Exception('RequestScraper http status Exception. status code: ' + str(response.status_code))

        return response.text

    def post(self, url: str, params: Dict = None, data: Dict = None, json=None, timeout: int = None,
             status_limit: int = 300):
        timeout = timeout if timeout else self.timeout

        # TODO: proxy
        response = self.req.post(url=url, data=data, json=json, timeout=timeout, params=params, headers=self.headers,
                                 stream=False, verify=False)
        self.current = response

        if response.status_code > status_limit:
            raise Exception('RequestScraper http status Exception. status code: ' + str(response.status_code))

        return response.text


class RequestScraper(
    RequestsBase,
    RequestsHeadersMixin,
    RequestsKeepAliveMixin,
    RequestsTimeoutMixin,
    RequestHttpMixin,
    Scraper
):
    def __init__(self,
                 headers: Dict[str, str] = None,
                 keep_alive: bool = True,
                 timeout: Union[int, float] = 10,
                 attach: bool = False):
        headers = headers if headers else default_headers.copy()

        self.set_headers(headers)
        self.set_keep_alive(keep_alive)
        self.set_timeout(timeout)

        Scraper.__init__(self, attach)

    def _attach(self) -> NoReturn:
        """
        Create the requests.Session instance.

        Modify session in RequestSettingMixin.
        Session.headers : default_header
        """
        req = Session()

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
