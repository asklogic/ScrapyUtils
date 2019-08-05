from abc import ABCMeta, abstractmethod, abstractproperty
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Any
import typing
from urllib3.exceptions import InsecureRequestWarning

from selenium.webdriver import Firefox, FirefoxOptions
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import requests
import time
from .proxy import Proxy

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ScraperMeta(ABCMeta):

    def __new__(mcs, name, bases, attrs) -> Any:
        # quit

        # http function

        return super().__new__(mcs, name, bases, attrs)


def must_activated(func):
    def wrapper(obj, *args, **kwargs):
        if not obj.activated:
            raise Exception('Scraper must be activated')
        return func(obj, *args, **kwargs)

    return wrapper


class Scraper(object, metaclass=ScraperMeta):
    # property
    _timeout: int = 10
    _proxy: Proxy = None
    _activated: bool = False

    # settings
    schemes: List[str] = []

    @abstractmethod
    def __init__(self):
        pass

    @property
    def activated(self):
        return self._activated

    # TODO how to active
    @activated.setter
    def activated(self, value):
        self._activated = value

    @abstractmethod
    def scraper_activate(self):
        pass

    def get(self, url: str, **kw) -> str:
        return self._http('get', url, **kw)

    def post(self, url: str, data, **kw):
        return self._http('get', url, **kw)

    @must_activated
    def _http(self, scheme: str, url: str, **kw) -> str:
        """

        :param scheme:
        :param url:
        :param kw:
        :return:
        """

        if scheme not in self.schemes:
            raise Exception('Scraper hasn\'t scheme named {}'.format(scheme))

        func = getattr(self, '_' + scheme)
        return func(url, **kw)

    @property
    def proxy(self):
        return self._proxy

    @property
    def timeout(self):
        return self._timeout

    # abstract property
    @proxy.setter
    @abstractmethod
    def proxy(self, value):
        pass

    @timeout.setter
    @abstractmethod
    def timeout(self, value):
        self._timeout = value

    # abstract methods
    @abstractmethod
    def clear_session(self):
        """
        Scraper重置 删除所有Session
        :return:
        """

    @abstractmethod
    def quit(self):

        pass

    # other methods
    def restart(self):

        self.safe_quit()
        self.scraper_activate()

    @must_activated
    def safe_quit(self):
        try:
            self.quit()
            self.activated = False
        except Exception as e:
            raise Exception('some exception in safe quit', e)

    def __del__(self):
        if self.activated:
            self.safe_quit()


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
    # request property
    _headers: dict = {}
    _keep_alive: bool = True

    req: requests.Session = None
    current: requests.Response = None

    # setting
    schemes = ['get']

    def __init__(self):
        super().__init__()

        self.timeout = 10
        self.proxy = {}

        self.headers = headers

    # scraper property
    @property
    def proxy(self) -> dict:
        if self._proxy and self._proxy[0]:
            return {
                "http": r"http://{0}".format(":".join(self._proxy)),
                "https": r"http://{0}".format(":".join(self._proxy)),
            }
        else:
            return {}

    @proxy.setter
    def proxy(self, value):
        # TODO
        pass

    @Scraper.timeout.setter
    def timeout(self, value):
        self._timeout = int(value)

    # requests property
    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, value):
        if type(value) is dict:
            self._headers = value
        else:
            self._headers = headers

    @property
    def keep_alive(self):
        return self._keep_alive

    @keep_alive.setter
    def keep_alive(self, value):
        headers = self.headers
        if value:
            headers['Connection'] = 'keep-alive'
        else:
            headers['Connection'] = 'close'
        self.headers = headers

    # scraper methods
    def scraper_activate(self):
        req = requests.Session()
        req.keep_alive = self.keep_alive
        req.headers = self.headers
        self.req = req

        self.activated = True

    def clear_session(self):
        self.restart()

    def quit(self):
        self.req.close()

    # requests methods
    def get_session_object(self):
        return self.req

    # http
    def _get(self, url, **kwargs):
        """
        http - GET
        :param url: str
        :param status:  status_code's range.
        :return:
        """
        params = kwargs.get('params', {})
        status = kwargs.get('status', 300)
        timeout = kwargs.get('timeout', self.timeout)
        response = self.req.get(url=url, timeout=timeout, headers=self.headers, proxies=self.proxy,
                                params=params, stream=False, verify=False)
        self.current = response

        if response.status_code / 100 > status / 100:
            raise Exception('RequestScraper http status failed')

        return response.content.decode("utf-8")


# class RequestScraper(Scraper):
#     schemes = ['get']
#
#     def __init__(self, activated=True):
#         self.timeout: int = 10
#         # TODO proxy_container
#         self.current_proxy: str = {}
#         self.proxies: Any = None
#
#         # requests
#         self._req: requests.Session = None
#         self.last: requests.Response = None
#
#         self.keep_alive = True
#         # self.keep_alive = False
#         self._headers = headers
#
#         # if activated:
#         #     self.activate()
#
#         if self.keep_alive:
#             self._headers['Connection'] = 'keep-alive'
#
#     def activate(self):
#         self._req: requests.Session = requests.session()
#         self._req.keep_alive = self.keep_alive
#         self._req.headers = self._headers
#
#         self.activated = True
#
#     def _get(self, url: str, params: Dict = None) -> str:
#         res = self._req.get(url=url, timeout=self.timeout, headers=self._headers, proxies=self.current_proxy,
#                             params=params, stream=False, verify=False)
#         self.last = res
#         return res.content.decode("utf-8")
#
#     def post(self, url: str, data: Dict, params: Dict = None) -> str:
#         res = self._req.post(url=url, data=data, timeout=self.timeout, headers=self._headers,
#                              proxies=self.current_proxy,
#                              params=params, stream=False, verify=False)
#         self.last = res
#         return res.content.decode("utf-8")
#
#     def get_current(self) -> requests.Response:
#         return self.last
#
#     def get_status_code(self):
#         return self.last.status_code
#
#     def set_proxy(self, proxy: Tuple[str, str]):
#         self.current_proxy = {
#             "http": r"http://{0}".format(":".join(proxy)),
#             "https": r"http://{0}".format(":".join(proxy)),
#         }
#
#     def set_timeout(self, time: int):
#         self.timeout = time
#
#     def clear_session(self):
#         self.current_proxy = {}
#
#         self._req.close()
#         self.activate()
#
#     def quit(self):
#         self.clear_session()


class FireFoxScraper(Scraper):
    # firefox property
    _image: bool = False
    _headless: bool = False

    firefox: Firefox = None
    options: FirefoxOptions = None

    def __init__(self, image=False, headless=True):
        super().__init__()
        self.options = FirefoxOptions()

        # 缓存页面
        # 重要 disk.enable 磁盘缓存 默认为过期再删除
        self.options.set_preference('browser.sessionhistory.max_total_viewers', 1)
        self.options.set_preference('network.http.use-cache', 'false')
        self.options.set_preference("network.http.use-cache", False)
        self.options.set_preference("browser.cache.memory.enable", False)
        self.options.set_preference("browser.cache.disk.enable", False)
        self.options.set_preference("network.dns.disableIPv6", True)
        self.options.set_preference("Content.notify.interval", 750000)
        self.options.set_preference("content.notify.backoffcount", 3)

        # 默认为无图模式 无头模式
        self.image = image
        self.headless = headless

    def scraper_activate(self):

        self.firefox = Firefox(options=self.options)
        self.firefox.set_script_timeout(self.timeout)
        self.firefox.set_page_load_timeout(self.timeout)

        # set config
        self.firefox.get("about:config")
        self.firefox.find_element_by_id("showWarningNextTime").click()
        self.firefox.find_element_by_id("warningButton").click()
        self.firefox.get("about:blank")

        self.activated = True

    # firefox property
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if value:
            self._image = True
            self.options.set_preference('permissions.default.image', 2)
        else:
            self._image = False
            self.options.set_preference('permissions.default.image', 0)

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, value):
        if value:
            self._headless = True
            self.options.headless = True
        else:
            self._headless = False
            self.options.headless = False

    # scraper property

    @Scraper.proxy.setter
    def proxy(self, proxy):
        self._proxy = (proxy.ip, proxy.port)

        self.firefox.get("about:config")
        js_content = """
        var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
        prefs.setIntPref("network.proxy.type", 1);
        prefs.setCharPref("network.proxy.http", "{0}");
        prefs.setIntPref("network.proxy.http_port", "{1}");
        prefs.setCharPref("network.proxy.ssl", "{0}");
        prefs.setIntPref("network.proxy.ssl_port", "{1}");
        """.format(proxy.ip, proxy.port)

        js_content = js_content.strip().replace("\n", "")
        self.firefox.execute_script(js_content)

    @Scraper.timeout.setter
    def timeout(self, value):
        self._timeout = int(value)
        self.firefox.set_script_timeout(self.timeout)
        self.firefox.set_page_load_timeout(self.timeout)

    # scraper function
    def clear_session(self):
        self.firefox.get("about:blank")
        self.firefox.delete_all_cookies()

    def quit(self):
        self.firefox.quit()

    # firefox function
    def get_driver(self) -> Firefox:
        return self.firefox


# class FireFoxScraper(Scraper):
#     def __init__(self, headless=True, image=False, activated=True):
#         self.firefox: Firefox = None
#
#         self.timeout = 7
#
#         self.options: FirefoxOptions = FirefoxOptions()
#         self.options.headless = headless
#
#         self.options.set_preference('browser.sessionhistory.max_total_viewers', 1)
#         if not image:
#             self.options.set_preference('permissions.default.image', 2)
#
#         if activated:
#             self.activate_scraper()
#
#     def start_tab(self):
#         pass
#
#     def get_status_code(self) -> int:
#         # FIXME selenium 无法判断状态码
#         return 200
#
#     def activate_scraper(self):
#         """
#         启动Firefox Scraper
#         :return:
#         """
#         self.firefox = Firefox(options=self.options)
#         self.firefox.set_script_timeout(self.timeout)
#         self.firefox.set_page_load_timeout(self.timeout)
#
#         self.firefox.get("about:config")
#         self.firefox.find_element_by_id("showWarningNextTime").click()
#         self.firefox.find_element_by_id("warningButton").click()
#         self.firefox.get("about:blank")
#
#     def getDriver(self) -> Firefox:
#         """
#         拿到driver 对象
#         :return:
#         """
#         return self.firefox
#         pass
#
#     def get(self, url: str) -> str:
#         self.firefox.get(url=url)
#         return self.firefox.page_source
#
#     def set_proxy(self, proxy: Tuple[str, str]):
#         """
#         设置代理
#         通过修改config内容 植入js修改浏览器代理
#         :param proxy:
#         :return:
#         """
#         self.firefox.get("about:config")
#         js_content = """
#         var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
#         prefs.setIntPref("network.proxy.type", 1);
#         prefs.setCharPref("network.proxy.http", "{0}");
#         prefs.setIntPref("network.proxy.http_port", "{1}");
#         prefs.setCharPref("network.proxy.ssl", "{0}");
#         prefs.setIntPref("network.proxy.ssl_port", "{1}");
#         """.format(proxy[0], proxy[1])
#
#         js_content = js_content.strip().replace("\n", "")
#         self.firefox.execute_script(js_content)
#
#     def set_timeout(self, time: int):
#         if self.firefox:
#             self.firefox.set_page_load_timeout(time)
#             self.firefox.set_script_timeout(time)
#
#     def clear_session(self):
#         """
#         回到空白页 删除cookies
#         :return:
#         """
#         self.firefox.get("about:blank")
#         self.firefox.delete_all_cookies()
#
#     def quit(self):
#         if self.firefox:
#             self.firefox.quit()
#
#     def block_mark(self, id: str, timeout: int = 5):
#         mark = str(int(time.time()))[-4:]
#
#         js = "document.getElementById('{}').innerText = '{}'".format(id, mark)
#         self.getDriver().execute_script(js)
#
#         while timeout > 0:
#             try:
#                 if mark != self.getDriver().find_element_by_id(id).text:
#                     return True
#
#                 time.sleep(0.2)
#                 timeout = timeout - 0.2
#             except NoSuchElementException as e:
#                 pass
#         raise Exception('block timeout')


def block_mark(id: str, driver: Firefox, timeout: int = 5):
    mark = str(int(time.time()))[-4:]

    js = "document.getElementById('{}').innerText = '{}'".format(id, mark)
    driver.execute_script(js)

    while timeout > 0:
        try:
            if mark != driver.find_element_by_id(id).text:
                return True

            time.sleep(0.2)
            timeout = timeout - 0.2
        except NoSuchElementException as e:
            pass
    raise Exception('block timeout')
