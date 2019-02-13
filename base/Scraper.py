from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Any
import typing

import requests

requests.adapters.DEFAULT_RETRIES


class BaseScraper(object):
    pass


class Scraper(BaseScraper, metaclass=ABCMeta):
    timeout: int = 10
    current_proxy: Tuple[str, str] = ("", "")

    @abstractmethod
    def __init__(self):
        """
        自定义的Scraper构造方法 需要实现
        """
        pass

    @abstractmethod
    def activate(self):
        '''
        激活Scraper
        :return:
        '''
        pass

    @abstractmethod
    def get(self, url: str) -> str:
        """
        访问url 返回网页内容
        :return: 网页内容
        """
        pass

    @abstractmethod
    def set_proxy(self, proxy: Tuple[str, str]):
        """
        设置当前代理信息
        :param proxy: 代理信息
        :return:
        """

    @abstractmethod
    def set_timeout(self, time: int):
        """
        设置单一请求超时
        :param time:
        :return:
        """

    @abstractmethod
    def clear_session(self):
        """
        Scraper重置 删除所有Session
        :return:
        """

    @abstractmethod
    def quit(self):
        """
        Scraper 安全退出
        :return:
        """
        pass

        # FIXME


headers = {
    'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    "Content-Type": "application/x-www-form-urlencoded",

    # 'Connection': 'close',
    'Cache-Control': 'max-age=0',
}


class RequestScraper(Scraper):
    def __init__(self, activated=True):
        self.timeout: int = 10
        # TODO proxy_container
        self.current_proxy: str = {}
        self.proxies: Any = None

        # requests
        self._req: requests.Session = requests.session()
        self.last: requests.Response = None
        self._headers = headers

        if activated:
            self.activate()

    def activate(self):
        self._req.headers = self._headers
        self._req.keep_alive = False

    def get(self, url: str, params: Dict = None) -> str:
        res = self._req.get(url=url, timeout=self.timeout, headers=self._headers, proxies=self.current_proxy,
                            params=params)
        self.last = res
        return res.content.decode("utf-8")

    def post(self, url: str, data: Dict, params: Dict = None) -> str:
        res = self._req.post(url=url, data=data, timeout=self.timeout, headers=self._headers,
                             proxies=self.current_proxy,
                             params=params)
        self.last = res
        return res.content.decode("utf-8")

    def origin_get(self) -> requests.Response:
        return self.last

    def set_proxy(self, proxy: Tuple[str, str]):
        self.current_proxy = {
            "http": r"http://{0}".format(":".join(proxy)),
            "https": r"http://{0}".format(":".join(proxy)),
        }

    def set_timeout(self, time: int):
        self.timeout = time

    def clear_session(self):
        self.current_proxy = {}
        self._headers = headers
        # self.last = None
        self._req.close()

    def quit(self):
        self.clear_session()
