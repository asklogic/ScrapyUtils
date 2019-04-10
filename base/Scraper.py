from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Any
import typing

from selenium.webdriver import Firefox, FirefoxOptions

import requests

requests.adapters.DEFAULT_RETRIES = 5


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
    'Accept': 'text/html,application/xhtml+xml,application/json,text/plain,*/*,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    "Content-Type": "application/x-www-form-urlencoded",
    # 'Connection': 'close',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}


class RequestScraper(Scraper):
    def __init__(self, activated=True):
        self.timeout: int = 10
        # TODO proxy_container
        self.current_proxy: str = {}
        self.proxies: Any = None

        # requests
        self._req: requests.Session = None
        self.last: requests.Response = None

        self.keep_alive = True
        # self.keep_alive = False
        self._headers = headers

        if activated:
            self.activate()

        if self.keep_alive:
            self._headers['Connection'] = 'keep-alive'

    def activate(self):
        self._req: requests.Session = requests.session()
        self._req.keep_alive = self.keep_alive
        self._req.headers = self._headers

    def get(self, url: str, params: Dict = None) -> str:
        res = self._req.get(url=url, timeout=self.timeout, headers=self._headers, proxies=self.current_proxy,
                            params=params, stream=False, verify=False)
        self.last = res
        return res.content.decode("utf-8")

    def post(self, url: str, data: Dict, params: Dict = None) -> str:
        res = self._req.post(url=url, data=data, timeout=self.timeout, headers=self._headers,
                             proxies=self.current_proxy,
                             params=params, stream=False, verify=False)
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

        self._req.close()
        self.activate()

    def quit(self):
        self.clear_session()


class FireFoxScraper(Scraper):
    def __init__(self, headless=True, image=False, activated=True):
        self.firefox: Firefox = None

        self.timeout = 7

        self.options: FirefoxOptions = FirefoxOptions()
        self.options.headless = headless

        self.options.set_preference('browser.sessionhistory.max_total_viewers', 1)
        if not image:
            self.options.set_preference('permissions.default.image', 2)

        if activated:
            self.activate()

    def start_tab(self):
        pass

    def activate(self):
        """
        启动Firefox Scraper
        :return:
        """
        self.firefox = Firefox(options=self.options)
        self.firefox.set_script_timeout(self.timeout)
        self.firefox.set_page_load_timeout(self.timeout)

        self.firefox.get("about:config")
        self.firefox.find_element_by_id("showWarningNextTime").click()
        self.firefox.find_element_by_id("warningButton").click()
        self.firefox.get("about:blank")

    def getDriver(self) -> Firefox:
        """
        拿到driver 对象
        :return:
        """
        return self.firefox
        pass

    def get(self, url: str) -> str:
        self.firefox.get(url=url)
        return self.firefox.page_source

    def set_proxy(self, proxy: Tuple[str, str]):
        """
        设置代理
        通过修改config内容 植入js修改浏览器代理
        :param proxy:
        :return:
        """
        self.firefox.get("about:config")
        js_content = """
        var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
        prefs.setIntPref("network.proxy.type", 1);
        prefs.setCharPref("network.proxy.http", "{0}");
        prefs.setIntPref("network.proxy.http_port", "{1}");
        prefs.setCharPref("network.proxy.ssl", "{0}");
        prefs.setIntPref("network.proxy.ssl_port", "{1}");
        """.format(proxy[0], proxy[1])

        js_content = js_content.strip().replace("\n", "")
        self.firefox.execute_script(js_content)

    def set_timeout(self, time: int):
        if self.firefox:
            self.firefox.set_page_load_timeout(time)
            self.firefox.set_script_timeout(time)

    def clear_session(self):
        """
        回到空白页 删除cookies
        :return:
        """
        self.firefox.get("about:blank")
        self.firefox.delete_all_cookies()

    def quit(self):
        if self.firefox:
            self.firefox.quit()
