# -*- coding: utf-8 -*-
"""Firefox scraper module.

FirefoxScraper bases on Selenium.webdriver.Firefox.

Todo:
    * log out.
    * Firefox proxy, timeout mixin.
    * unittest.
    * driver block function.
    * parameter driver/binary path
"""

import os
import platform
from typing import *

from ScrapyUtils.libs.scraper import Scraper, TimeoutMixin

from logging import getLogger

logger = getLogger('firefox')

try:
    from selenium.webdriver import Firefox, FirefoxOptions
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

except ImportError as e:
    # TODO: libs log
    pass

if 'Win' in platform.system():
    platform_suffix = '.exe'
else:
    platform_suffix = ''

firefox_path = ''.join(['firefox', os.sep, 'firefox', platform_suffix])
driver_path = ''.join(['firefox', os.sep, 'geckodriver', platform_suffix])


# setter function

def set_firefox_path(path: str):
    """Set the global varibale firefox_path.

    The firefox will attach the browser by this path.

    Default value is "project/firefox/firefox"

    Args:
        path (str): The path of browser.
    """
    global firefox_path
    firefox_path = path


def set_driver_path(path: str):
    """Set the gloabl variable driver_path.

    The dirver_path is the path of webdriver.

    Default value is "project/firefox/geckodriver"

    Args:
        path (str): The path of geckodriver
    """
    global driver_path
    driver_path = driver_path


# mixin

class FireFoxSettingMixin(object):
    """Firefox setting mixin.

    Firefox的设置，包含了浏览器通用设置，图片、无头和禁用js属性控制。
    attach之后不能修改浏览器属性，因为设置属性只修改了option的值，需要重启才能应用修改。

    Attributes:
        image (bool): Image state, Flase means no image.
        headless (bool): Headless state, Flase means headless.
        js (bool): Javascripts state, Flase means no js.

        driver_path (str): Current driver_path.
        binary (FirefoxBinary): Current bianry(browser).

        options (FirefoxOptions): Current options.

    """

    # firefox property
    _image: bool = False
    _headless: bool = True
    _js: bool = True

    options: FirefoxOptions = None

    driver_path: str = None
    binary: FirefoxBinary = None

    def __init__(self, headless: bool = True, image: bool = False, js: bool = True, **kwargs):
        assert os.path.isfile(driver_path), f'no driver file {driver_path}'
        assert os.path.isfile(firefox_path), f'no firefox file {firefox_path}'

        self.options = FirefoxOptions()
        self.binary = FirefoxBinary(firefox_path)
        self.driver_path = driver_path

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

        self.image = image
        self.headless = headless
        self.js = js

        super().__init__(**kwargs)

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
            # self.options.set_preference("browser.download.folderList", 0)
            self.options.set_preference("javascript.enabled", True)
        else:
            self._js = False
            self.options.set_preference("browser.download.folderList", 2)
            self.options.set_preference("javascript.enabled", False)


class FirefoxTimeoutMixin(TimeoutMixin):
    firefox: Firefox

    @TimeoutMixin.timeout.setter
    def timeout(self, value):
        if self.firefox:
            self.firefox.set_script_timeout(self.timeout)
            self.firefox.set_page_load_timeout(self.timeout)
        self._timeout = int(value)


class FirefoxHttpMixin(object):
    firefox: Firefox

    def get(self, url: str):
        self.firefox.get(url)
        return self.firefox.page_source


class FireFoxScraper(
    FireFoxSettingMixin,
    FirefoxHttpMixin,
    Scraper
):
    firefox: Firefox = None

    def _attach(self) -> NoReturn:
        self.firefox = Firefox(options=self.options, firefox_binary=self.binary, executable_path=self.driver_path)

        self.firefox.set_script_timeout(self.timeout)
        self.firefox.set_page_load_timeout(self.timeout)

        self.firefox.get("about:config")
        self.firefox.find_element_by_id("showWarningNextTime").click()
        self.firefox.find_element_by_id("warningButton").click()
        self.firefox.get("about:blank")

    def _detach(self) -> NoReturn:
        try:
            self.firefox.service.assert_process_still_running()
        except Exception as e:
            print(e)
        self.firefox.quit()

    def _clear(self) -> NoReturn:
        self.firefox.delete_all_cookies()
        self.firefox.get("about:blank")
        self.firefox.delete_all_cookies()

    def get_driver(self) -> Firefox:
        return self.firefox
