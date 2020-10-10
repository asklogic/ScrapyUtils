from abc import ABCMeta, abstractmethod, abstractproperty
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Any, Callable
from urllib3.exceptions import InsecureRequestWarning

from appium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait

import requests
import time
from .proxy import Proxy

# Request common setting
requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Firefox common setting

geckodriver_path = ''
firefox_path = ''


# TODO: fix it.
class ScraperMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs) -> Any:
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


# class Scraper(object, metaclass=ScraperMeta):
#     # property
#     _timeout: int = 10
#     _proxy: Proxy = None
#     _activated: bool = False
#
#     # settings
#     schemes: List[str] = []
#
#     # ----------------------------------------------------------------------
#     # abstract methods
#     @abstractmethod
#     def __init__(self):
#         pass
#
#     @abstractmethod
#     def _activate(self):
#         pass
#
#     @abstractmethod
#     def _clear(self):
#         pass
#
#     @abstractmethod
#     def _quit(self):
#         pass
#
#     # ----------------------------------------------------------------------
#     # scraper method
#
#     @need_not_activated
#     def scraper_activate(self):
#         self._activate()
#
#     @need_activated
#     def scraper_clear(self):
#         self._clear()
#
#     def scraper_quit(self):
#         try:
#             if self.activated:
#                 self._quit()
#                 self._activated = False
#         except Exception as e:
#             raise Exception('some exception in scraper quit', e)
#
#     # ----------------------------------------------------------------------
#     # http methods
#
#     @need_activated
#     def _http(self, scheme: str, url: str, **kw) -> str:
#         """
#
#         :param scheme:
#         :param url:
#         :param kw:
#         :return:
#         """
#
#         if scheme not in self.schemes:
#             raise Exception("Scraper hasn't scheme named {}".format(scheme))
#
#         func = getattr(self, '_' + scheme)
#         return func(url, **kw)
#
#     def get(self, url: str, **kw) -> str:
#         return self._http('get', url, **kw)
#
#     def post(self, url: str, **kw):
#         return self._http('post', url, **kw)
#
#     # ----------------------------------------------------------------------
#     # property
#
#     @property
#     def proxy(self):
#         return self._proxy
#
#     @property
#     def timeout(self):
#         return self._timeout
#
#     @property
#     def activated(self):
#         return self._activated
#
#     # ----------------------------------------------------------------------
#     # property setter
#
#     @activated.setter
#     def activated(self, value):
#         self._activated = bool(value)
#
#     # ----------------------------------------------------------------------
#     # abstract property setter
#
#     @timeout.setter
#     @abstractmethod
#     def timeout(self, value):
#         self._timeout = value
#
#     @proxy.setter
#     @abstractmethod
#     def proxy(self, value: Proxy):
#         pass
#
#     # ----------------------------------------------------------------------
#     # other methods
#     def restart(self):
#         self.scraper_quit()
#         self.scraper_activate()
#
#     def __del__(self):
#         self.scraper_quit()


class TimeoutMixin(object):
    _timeout: int = 10

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value


class ProxyMixin(object):
    _proxy: Proxy = None

    @property
    def proxy(self) -> Proxy:
        return self._proxy

    @proxy.setter
    def proxy(self, value: Proxy):
        self._proxy = value


class HttpMixin(object):
    # basic property
    timeout: int
    proxy: Proxy


class RequestProxyMixin(ProxyMixin):
    def request_proxy_dict(self):
        if self.proxy:
            return {
                "http": r"http://{0}".format(":".join((self.proxy.ip, self.proxy.port))),
                "https": r"http://{0}".format(":".join((self.proxy.ip, self.proxy.port))),
            }
        return None


class Scraper(RequestProxyMixin, TimeoutMixin, object):
    """The base class of Scraper. 

    Define the common method and the abstractmethods of a scraper. 

    Args:
        _activated (bool): The activated state. True == it activated.
    """
    _activated: bool = False

    @abstractmethod
    def __init__(self, **kwargs):
        if kwargs.get('activated'):
            self.scraper_activate()

    @abstractmethod
    def _activate(self) -> None:
        """Scraper activation. 
        """
        pass

    @abstractmethod
    def _clear(self) -> None:
        """Scraper clear it's sessions.
        """
        pass

    @abstractmethod
    def _quit(self) -> None:
        """Scraper quit.
        """
        pass

    @property
    def activated(self):
        return self._activated

    @need_not_activated
    def scraper_activate(self) -> None:
        # TODO: raise execption.
        self._activate()
        self._activated = True

    @need_activated
    def scraper_clear(self) -> None:
        self._clear()

    def scraper_quit(self) -> None:
        if self.activated:
            self._quit()
            self._activated = False

    @abstractmethod
    def get_instance(self) -> object:
        pass

    def restart(self) -> None:
        """Restart Scraper.
        """
        self.scraper_quit()
        self.scraper_activate()

    def __del__(self):
        self.scraper_quit()


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


# class RequestScraper(Scraper):
#     # request property
#     _headers: dict = {}
#     _keep_alive: bool = True
#
#     req: requests.Session = None
#     current: requests.Response = None
#
#     # setting
#     schemes = ['get', 'post']
#
#     def __init__(self):
#         super().__init__()
#
#         self.timeout = 10
#         self.headers = self.headers if self.headers else default_headers
#
#     # ----------------------------------------------------------------------
#     # scraper method
#
#     def _activate(self):
#         req = requests.Session()
#         req.keep_alive = self.keep_alive
#
#         # TODO: one single header
#         req.headers = self.headers
#
#         self.req = req
#
#         self._activated = True
#
#     def _clear(self):
#         self.restart()
#
#     def _quit(self):
#         self.req.close()
#
#     # ----------------------------------------------------------------------
#     # requests property
#     @property
#     def proxy(self) -> dict:
#         if self._proxy:
#             return {
#                 "http": r"http://{0}".format(":".join((self._proxy.ip, self._proxy.port))),
#                 "https": r"http://{0}".format(":".join((self._proxy.ip, self._proxy.port))),
#             }
#         else:
#             return {}
#
#     @proxy.setter
#     def proxy(self, value: Proxy):
#         # TODO
#         assert isinstance(value, Proxy)
#         self._proxy = value
#
#     @Scraper.timeout.setter
#     def timeout(self, value):
#         self._timeout = value
#
#     # ----------------------------------------------------------------------
#     # requests property
#     @property
#     def headers(self) -> dict:
#         return self._headers
#
#     @headers.setter
#     def headers(self, value):
#         if type(value) is dict:
#             self._headers = value
#         else:
#             self._headers = default_headers
#
#     @property
#     def keep_alive(self):
#         return self._keep_alive
#
#     @keep_alive.setter
#     def keep_alive(self, value):
#         if value:
#             self.headers['Connection'] = 'keep-alive'
#             self._keep_alive = True
#
#         else:
#             self.headers['Connection'] = 'close'
#             self._keep_alive = False
#
#     # ----------------------------------------------------------------------
#     # http
#     def _get(self, url, **kwargs):
#         """
#         http - GET
#         :param url: str
#         :param status: int - status_code's range.
#         :return: content : str
#         """
#         params = kwargs.get('params', {})
#         status = kwargs.get('status', 300)
#         timeout = kwargs.get('timeout', self.timeout)
#
#         response = self.req.get(url=url, timeout=timeout, headers=self.headers, proxies=self.proxy,
#                                 params=params, stream=False, verify=False)
#         self.current = response
#
#         if response.status_code / 100 > status / 100:
#             raise Exception('RequestScraper http status failed. status: ' + str(response.status_code))
#
#         return response.text
#
#     def _post(self, url, **kwargs):
#
#         params = kwargs.get('params', {})
#         status = kwargs.get('status', 300)
#         timeout = kwargs.get('timeout', self.timeout)
#         data = kwargs.get('data', {})
#         json = kwargs.get('json', {})
#
#         response = self.req.post(url=url, data=data, json=json, timeout=timeout, headers=self.headers,
#                                  proxies=self.proxy, params=params, stream=False, verify=False)
#
#         self.current = response
#
#         if response.status_code / 100 > status / 100:
#             raise Exception('RequestScraper http status failed. status: ' + str(response.status_code))
#
#         return response.text
#
#         # self.req.post(url=url, json=json)
#
#     # ----------------------------------------------------------------------
#     # request other methods
#
#     def get_requests(self) -> requests.Session:
#         return self.req


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
        timeout_exec = kwargs.get('timeout_exec', True)

        if timeout_exec:
            self.firefox.get(url)
        else:
            try:
                self.firefox.get(url)
            except TimeoutException as te:
                return self.firefox.page_source

        return self.firefox.page_source

    def __del__(self):
        # TODO
        if self.activated:
            self.scraper_quit()


origin_desired_caps = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "newCommandTimeout": "3000",
    'noReset': "True",
    # "appPackage": "com.youpin.comic",
    # "appActivity": "com.youpin.comic.welcomepage.WelcomeActivity",
}


class AppiumScraper(Scraper):
    """
    The Scraper of Appium's webdriver.

    It start a Appium.webdriver.Remote to get a Android webdriver. To set different app entry to controll different app.

    Args:
        port (intorstr): The avd's port(must in localhost).
        entry (Tuple[str, str]): The appPackge and The appActivity.

    Attributes:
        desired_caps (Dict[str, str]): The desired_caps parameter of the webdriver.Remote.
        driver (webdriver.Remote): The instance of webdriver.Remote.
        _no_reset (bool): TODO: no_reset 

    """

    desired_caps: Dict[str, str]

    # settings
    _no_reset: bool = True

    # instance
    driver: webdriver.Remote = None

    def __init__(self, port: int or str, entry: Tuple[str, str], **kwargs):
        self.desired_caps = origin_desired_caps.copy()

        devices = '127.0.0.1:' + str(port)

        self.desired_caps['deviceName'] = devices
        self.desired_caps['appPackage'] = entry[0]
        self.desired_caps['appActivity'] = entry[1]

        super(AppiumScraper, self).__init__(**kwargs)

    def _activate(self) -> None:
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.desired_caps)

    def _clear(self) -> None:
        self._quit()
        self._activate()

    def _quit(self) -> None:
        self.driver.quit()

    def get_instance(self) -> webdriver.Remote:
        """
        Get the instance of webdriver.Remote.

        Returns:
            webdriver.Remote: The instance of the webdriver.Remote.
        """
        return self.driver


class FirefoxHttpMixin(object):
    firefox: Firefox

    def get(self, url: str):
        return self.firefox.get(url)


class FirefoxTimeoutMixin(TimeoutMixin):
    firefox: Firefox

    @TimeoutMixin.timeout.setter
    def timeout(self, value):
        if self.firefox:
            self.firefox.set_script_timeout(self.timeout)
            self.firefox.set_page_load_timeout(self.timeout)
        self._timeout = int(value)


class FirefoxProxyMixin(ProxyMixin):
    firefox: Firefox

    @ProxyMixin.proxy.setter
    def proxy(self, proxy: Proxy):
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

        self._proxy = proxy


class FirefoxSettingMixin(object):
    options: FirefoxOptions = None

    _image: bool = False
    _headless: bool = True
    _js: bool = True

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if value:
            self._image = True
            self.options.set_preference('permissions.default.image', 0)
        else:
            self._image = False
            self.options.set_preference('permissions.default.image', 2)

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
        if value:
            self._js = True
            # self.options.set_preference("browser.download.folderList", 2)
            # self.options.set_preference("javascript.enabled", False)
        else:
            self._js = False
            self.options.set_preference("browser.download.folderList", 2)
            self.options.set_preference("javascript.enabled", False)


class FirefoxScraper(FirefoxSettingMixin, FirefoxProxyMixin, FirefoxTimeoutMixin, Scraper):
    """
    The Scraper of FirefoxWebdriver.

    Args:
        Scraper ([type]): [description]
    """
    options: FirefoxOptions = None

    # settings
    _image: bool = False
    _headless: bool = True
    _js: bool = True

    # instance
    firefox: Firefox = None

    def __init__(self, image: bool = False, headless: bool = True, js: bool = True, **kwargs):
        self.options = FirefoxOptions()

        # The firefox common setting.
        self.options.set_preference('browser.sessionhistory.max_total_viewers', 1)
        self.options.set_preference('network.http.use-cache', 'false')
        self.options.set_preference("network.http.use-cache", False)
        # critical: The disk cache.
        self.options.set_preference("browser.cache.memory.enable", False)
        self.options.set_preference("browser.cache.disk.enable", False)
        self.options.set_preference("network.dns.disableIPv6", True)
        self.options.set_preference("content.notify.interval", 750000)
        self.options.set_preference("content.notify.backoffcount", 3)

        # FirefoxScraper setting mixin
        self.image = image
        self.headless = headless
        self.js = js

        super(FirefoxScraper, self).__init__(**kwargs)

    def _activate(self) -> None:
        # configure: get_firefox_binary_path

        if None:
            binary = FirefoxBinary('firefox_binary_path')
        else:
            binary = None

        # configure: get_firefox_geckodriver_path
        driver_path = 'geckodriver'

        # TODO: webdriver timeout.

        self.firefox = Firefox(options=self.options, firefox_binary=binary, executable_path=driver_path)

        # set config
        self.firefox.get("about:config")
        self.firefox.find_element_by_id("showWarningNextTime").click()
        self.firefox.find_element_by_id("warningButton").click()
        self.firefox.get("about:blank")

    def _clear(self) -> None:
        self.firefox.get("about:blank")
        self.firefox.delete_all_cookies()

    def _quit(self) -> None:
        try:
            self.firefox.service.assert_process_still_running()
        except Exception as e:
            pass
        finally:
            self.firefox.quit()

    def get_instance(self) -> Firefox:
        return self.firefox


class RequestHttpMixin(HttpMixin):
    current: requests.Response = None

    req: requests.Session

    def get(self, url: str, params: Dict = None, timeout: int = None, status_limit: int = 300):
        timeout = timeout if timeout else self.timeout
        # proxy = {
        #     "http": r"http://{0}".format(":".join((self.proxy.ip, self.proxy.port))),
        #     "https": r"http://{0}".format(":".join((self.proxy.ip, self.proxy.port))),
        # }

        # response = self.req.get(url=url, timeout=timeout, headers=self.headers, proxies=proxy,
        #                         params=params, stream=False, verify=False)

        response = self.req.get(url=url, timeout=timeout, proxies=self.request_proxy_dict(), params=params, stream=False, verify=False)
        self.current = response

        if response.status_code / 100 > status_limit / 100:
            raise Exception('RequestScraper http status Exception. status code: ' + str(response.status_code))

        return response.text

    def post(self, url: str, params: Dict = None, data: Dict = None, json=None, timeout: int = None,
             status_limit: int = 300):
        timeout = timeout if timeout else self.timeout
        proxy = {
            "http": r"http://{0}".format(":".join((self.proxy.ip, self.proxy.port))),
            "https": r"http://{0}".format(":".join((self.proxy.ip, self.proxy.port))),
        }

        response = self.req.post(url=url, data=data, json=json, timeout=timeout, proxies=proxy, params=params,
                                 stream=False, verify=False)
        self.current = response

        if response.status_code / 100 > status_limit / 100:
            raise Exception('RequestScraper http status Exception. status code: ' + str(response.status_code))

        return response.text


# class RequestTimeoutMixin(object):
#     pass
#
#
# class RequestProxyMixin(ProxyMixin):
#     pass


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


class RequestScraper(RequestSettingMixin, RequestHttpMixin, Scraper):
    # setting
    _headers: Dict[str, str] = None
    _keep_alive: bool = True

    # http
    current: requests.Response = None

    # instance
    req: requests.Session = None

    def __init__(self, headers: dict = None, **kwargs):
        self.timeout = 10
        self.headers = headers if headers else default_headers.copy()

        super(RequestScraper, self).__init__(**kwargs)

    def _activate(self) -> None:
        req = requests.Session()
        req.keep_alive = self.keep_alive

        req.headers = self.headers
        self.req = req

    def _clear(self) -> None:
        self.restart()

    def _quit(self) -> None:
        self.req.close()

    def get_instance(self) -> requests.Session:
        return self.req


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

def get_headless_firefox():
    f = FirefoxScraper(headless=False, activated=True)
    return f


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


def wait_block(mark_class, wait_time, context, driver):
    """
    Args:
        mark_class:
        wait_time:
        context:
        driver:
    """
    if not context.get('mark'):
        WebDriverWait(driver, wait_time).until(lambda d: d.find_element_by_class_name(mark_class))
        context['mark'] = True

    else:
        WebDriverWait(driver, wait_time).until(
            lambda d: d.find_element_by_class_name(mark_class).get_attribute('themark') != 'themark')

    js = 'document.getElementsByClassName("{}")[0].setAttribute("themark","themark")'.format(mark_class)
    driver.execute_script(js)
