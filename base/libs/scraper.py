from abc import ABCMeta, abstractmethod, abstractproperty
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Any, Callable
import typing
from urllib3.exceptions import InsecureRequestWarning

# from appium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import requests
import time
from .proxy import Proxy

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ScraperMeta(ABCMeta):

    def __new__(mcs, name, bases, attrs) -> Any:
        # quit

        return super().__new__(mcs, name, bases, attrs)


def need_activated(func) -> Callable:
    def wrapper(obj, *args, **kwargs):
        if not obj.activated:
            raise Exception('Scraper must be activated.')
        return func(obj, *args, **kwargs)

    return wrapper


def need_not_activated(func) -> Callable:
    def wrapper(obj, *args, **kwargs):
        if obj.activated:
            raise Exception('Scraper must be not activated.')
        return func(obj, *args, **kwargs)

    return wrapper


class Scraper(object, metaclass=ScraperMeta):
    # property
    _timeout: int = 10
    _proxy: Proxy = None
    _activated: bool = False

    # settings
    schemes: List[str] = []

    # ----------------------------------------------------------------------
    # abstract methods
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _activate(self):
        pass

    @abstractmethod
    def _clear(self):
        pass

    @abstractmethod
    def _quit(self):
        pass

    # ----------------------------------------------------------------------
    # scraper method

    @need_not_activated
    def scraper_activate(self):
        self._activate()

    @need_activated
    def scraper_clear(self):
        self._clear()

    def scraper_quit(self):
        # TODO : need try-except?
        try:
            if self.activated:
                self._quit()
                self._activated = False
        except Exception as e:
            raise Exception('some exception in scraper quit', e)

    # ----------------------------------------------------------------------
    # http methods

    @need_activated
    def _http(self, scheme: str, url: str, **kw) -> str:
        """

        :param scheme:
        :param url:
        :param kw:
        :return:
        """

        if scheme not in self.schemes:
            raise Exception("Scraper hasn't scheme named {}".format(scheme))

        func = getattr(self, '_' + scheme)
        return func(url, **kw)

    def get(self, url: str, **kw) -> str:
        return self._http('get', url, **kw)

    def post(self, url: str, **kw):
        return self._http('post', url, **kw)

    # ----------------------------------------------------------------------
    # property

    @property
    def proxy(self):
        return self._proxy

    @property
    def timeout(self):
        return self._timeout

    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, value):
        self._activated = bool(value)

    # ----------------------------------------------------------------------
    # abstract property

    @timeout.setter
    @abstractmethod
    def timeout(self, value):
        self._timeout = value

    @proxy.setter
    @abstractmethod
    def proxy(self, value: Proxy):

        pass

    # ----------------------------------------------------------------------
    # other methods
    def restart(self):
        self.scraper_quit()
        self.scraper_activate()

    def __del__(self):
        self.scraper_quit()


headers = {
    'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/json,text/plain,*/*,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Language': 'en-us',
    "Content-Type": "application/x-www-form-urlencoded",
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
    schemes = ['get', 'post']

    def __init__(self):
        super().__init__()

        self.timeout = 10
        self.headers = self.headers if self.headers else headers

    # ----------------------------------------------------------------------
    # scraper method

    def _activate(self):
        req = requests.Session()
        req.keep_alive = self.keep_alive

        # TODO: one single header
        req.headers = self.headers

        self.req = req

        self._activated = True

    def _clear(self):
        self.restart()

    def _quit(self):
        self.req.close()

    # ----------------------------------------------------------------------
    # requests property
    @property
    def proxy(self) -> dict:
        if self._proxy:
            return {
                "http": r"http://{0}".format(":".join((self._proxy.ip, self._proxy.port))),
                "https": r"http://{0}".format(":".join((self._proxy.ip, self._proxy.port))),
            }
        else:
            return {}

    @proxy.setter
    def proxy(self, value: Proxy):
        # TODO
        assert isinstance(value, Proxy)
        self._proxy = value

    @Scraper.timeout.setter
    def timeout(self, value):
        self._timeout = value

    # ----------------------------------------------------------------------
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
        if value:
            self.headers['Connection'] = 'keep-alive'
            self._keep_alive = True

        else:
            self.headers['Connection'] = 'close'
            self._keep_alive = False

    # ----------------------------------------------------------------------
    # http
    def _get(self, url, **kwargs):
        """
        http - GET
        :param url: str
        :param status: int - status_code's range.
        :return: content : str
        """
        params = kwargs.get('params', {})
        status = kwargs.get('status', 300)
        timeout = kwargs.get('timeout', self.timeout)

        response = self.req.get(url=url, timeout=timeout, headers=self.headers, proxies=self.proxy,
                                params=params, stream=False, verify=False)
        self.current = response

        if response.status_code / 100 > status / 100:
            raise Exception('RequestScraper http status failed. status: ' + str(response.status_code))

        return response.text

    def _post(self, url, **kwargs):

        params = kwargs.get('params', {})
        status = kwargs.get('status', 300)
        timeout = kwargs.get('timeout', self.timeout)
        data = kwargs.get('data', {})
        json = kwargs.get('json', {})

        response = self.req.post(url=url, data=data, json=json, timeout=timeout, headers=self.headers,
                                 proxies=self.proxy, params=params, stream=False, verify=False)

        self.current = response

        if response.status_code / 100 > status / 100:
            raise Exception('RequestScraper http status failed. status: ' + str(response.status_code))

        return response.text

        # self.req.post(url=url, json=json)

    # ----------------------------------------------------------------------
    # request other methods

    def get_requests(self) -> requests.Session:
        return self.req


class FireFoxScraper(Scraper):
    # firefox property
    _image: bool = False
    _headless: bool = True
    _js: bool = True

    firefox: Firefox = None
    options: FirefoxOptions = None

    schemes = ['get']

    def __init__(self, image=False, headless=True, js=True, exe_path=None, driver_path=None):
        super().__init__()
        self.options = FirefoxOptions()

        # firefox cache
        # 重要 disk.enable 磁盘缓存 默认为过期再删除
        self.options.set_preference('browser.sessionhistory.max_total_viewers', 1)
        self.options.set_preference('network.http.use-cache', 'false')
        self.options.set_preference("network.http.use-cache", False)
        self.options.set_preference("browser.cache.memory.enable", False)
        self.options.set_preference("browser.cache.disk.enable", False)
        self.options.set_preference("network.dns.disableIPv6", True)
        self.options.set_preference("Content.notify.interval", 750000)
        self.options.set_preference("content.notify.backoffcount", 3)

        # default no image, headless
        self.image = image
        self.headless = headless
        self.js = js
        self.exe_path = exe_path
        self.driver_path = driver_path

    def _activate(self):
        binary = None
        if self.exe_path:
            binary = FirefoxBinary(self.exe_path)

        if self.driver_path:
            self.firefox = Firefox(options=self.options, firefox_binary=binary, executable_path=self.driver_path)
        else:
            self.firefox = Firefox(options=self.options)

        self.firefox.set_script_timeout(self.timeout)
        self.firefox.set_page_load_timeout(self.timeout)

        # set config
        self.firefox.get("about:config")
        self.firefox.find_element_by_id("showWarningNextTime").click()
        self.firefox.find_element_by_id("warningButton").click()
        self.firefox.get("about:blank")

        # self.firefox.set

        self._activated = True

    # ----------------------------------------------------------------------
    # firefox property

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        """
        modify firefox options
        """
        if value:
            self._image = True
            self.options.set_preference('permissions.default.image', 0)
        else:
            self._image = False

            self.options.set_preference('permissions.default.image', 2)
            # self.options.set_preference('browser.migration.version', 9001)

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

    @property
    def js(self):
        return self._js

    @js.setter
    def js(self, value):
        if not value:
            self.options.set_preference("browser.download.folderList", 2)
            self.options.set_preference("javascript.enabled", False)

    # ----------------------------------------------------------------------
    # scraper property

    @Scraper.proxy.setter
    def proxy(self, proxy: Proxy):
        self._proxy = proxy

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
        if self.firefox:
            self.firefox.set_script_timeout(self.timeout)
            self.firefox.set_page_load_timeout(self.timeout)

    # ----------------------------------------------------------------------
    # scraper function

    def _clear(self):
        self.firefox.get("about:blank")
        self.firefox.delete_all_cookies()

    def _quit(self):
        try:
            self.firefox.service.assert_process_still_running()
        except Exception as e:
            pass
        finally:
            self.firefox.quit()

    # ----------------------------------------------------------------------
    # firefox function

    def get_driver(self) -> Firefox:
        return self.firefox

    def _get(self, url, **kwargs):

        self.firefox.get(url)

        return self.firefox.page_source

    def __del__(self):
        # TODO
        if self.activated:
            self.scraper_quit()


# class AppiumScraper(Scraper):
#
#     def __init__(self, desired, ):
#         super(AppiumScraper, self).__init__()
#
#         driver = webdriver.Remote('http://localhost:4723/wd/hub', desired)
#
#         pass
#
#     def _activate(self):
#         pass
#
#     def _clear(self):
#         pass
#
#     def _quit(self):
#         pass


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
