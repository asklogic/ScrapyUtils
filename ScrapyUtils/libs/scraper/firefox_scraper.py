# -*- coding: utf-8 -*-
"""firefox_scraper module.

FirefoxScraper bases on Selenium.webdriver.Firefox.

Todo:
    * unittest.
    * binary or options.binary
"""

import os
import platform
from logging import getLogger
from typing import Set, Union, NoReturn

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# from ._base_scraper import Scraper
from ScrapyUtils.libs.scraper import Scraper

# default logger
logger = getLogger('scraper')
"""Common logger"""

global_webdriver_set: Set[Firefox] = set()
"""set: The set to store all the webdriver instances."""

# system switch
if 'Win' in platform.system():
    PLATFORM_SUFFIX = '.exe'
else:
    PLATFORM_SUFFIX = ''

FIREFOX_PATH = ''.join(['firefox', os.sep, 'firefox', PLATFORM_SUFFIX])
"""str: The firefox path"""
DRIVER_PATH = ''.join(['firefox', os.sep, 'geckodriver', PLATFORM_SUFFIX])
"""str: The geckodriver path"""


# setter function
def set_firefox_path(path: str) -> NoReturn:
    """Set the global variable firefox_path.

    The firefox will attach the browser with this path.

    Default value is "{work_path}/firefox/firefox"

    Args:
        path (str): The path of browser.
    """
    global FIREFOX_PATH
    FIREFOX_PATH = path


def set_driver_path(path: str) -> NoReturn:
    """Set the global variable driver_path.

    The driver_path is the path of webdriver.

    Default value is "{work_path}/firefox/geckodriver"

    Args:
        path (str): The path of geckodriver
    """
    global DRIVER_PATH
    DRIVER_PATH = path


def exit_all_firefox_webdriver() -> NoReturn:
    """Exit all firefox webdriver without scraper_detach.
    """
    for webdriver in global_webdriver_set:
        webdriver.quit()


class FireFoxBase:
    firefox: Firefox = None


class FireFoxOptionsBase:
    options: FirefoxOptions = None


class FirefoxHeadlessMixin(FireFoxOptionsBase):

    def set_headless(self, state: bool = False):
        if state:
            self.options.headless = True
        else:
            self.options.headless = False


class FirefoxJavascriptMixin(FireFoxOptionsBase):

    def set_js(self, state: bool = True):
        if state:
            self.options.set_preference("javascript.enabled", True)
        else:
            self.options.set_preference("javascript.enabled", False)


class FirefoxImageMixin(FireFoxOptionsBase):

    def set_image(self, state: bool = False):
        if state:
            self.options.set_preference('permissions.default.image', 3)
        else:
            self.options.set_preference('permissions.default.image', 2)


class FirefoxTimeoutMixin(FireFoxBase):
    timeout = 10

    def set_timeout(self, timeout: Union[int, float] = 10):
        self.timeout = timeout
        if self.firefox:
            self.firefox.set_script_timeout(timeout)
            self.firefox.set_page_load_timeout(timeout)


class FirefoxHttpMixin(FireFoxBase):

    def get(self, url: str):
        self.firefox.get(url)
        return self.firefox.page_source


class FirefoxBinaryBase(FireFoxBase, FireFoxOptionsBase):
    DRIVER_PATH: str = None

    def __init__(self):
        self.options = FirefoxOptions()

        if os.path.isfile(DRIVER_PATH):
            self.driver_path = DRIVER_PATH
        else:
            self.driver_path = None

    @property
    def binary(self) -> FirefoxBinary:
        if os.path.isfile(FIREFOX_PATH):
            return FirefoxBinary(FIREFOX_PATH)
        else:
            return FirefoxBinary()


class FireFoxScraper(
    FirefoxBinaryBase,
    FirefoxHeadlessMixin,
    FirefoxImageMixin,
    FirefoxJavascriptMixin,
    FirefoxTimeoutMixin,
    FirefoxHttpMixin,

    Scraper
):

    def __init__(self,
                 headless: bool = False,
                 js: bool = True,
                 image: bool = True,
                 timeout: Union[int, float] = 10,
                 attach: bool = False
                 ):
        # execute init method.
        FirefoxBinaryBase.__init__(self)

        self.set_js(js)
        self.set_headless(headless)
        self.set_image(image)
        self.set_timeout(timeout)

        Scraper.__init__(self, attach)

    def _attach(self) -> NoReturn:
        """Attach the Firefox instance.

        Create a firefox instance by options and binary.

        """
        self.firefox = Firefox(options=self.options,
                               firefox_binary=self.binary,
                               executable_path=self.driver_path)

        self.firefox.get("about:config")
        if el := self.firefox.find_elements(By.ID, 'showWarningNextTime'):
            el[0].click()
        if el := self.firefox.find_elements(By.ID, 'warningButton'):
            el[0].click()
        if el := self.firefox.find_elements(By.ID, 'about-config-show-only-modified'):
            el[0].click()
        self.firefox.get("about:blank")

        self.set_timeout(10)

        global_webdriver_set.add(self.firefox)

    def _detach(self) -> NoReturn:
        """Detach the firefox instance.

        Quit the firefox and remove the instance from global set.

        """
        try:
            self.firefox.service.assert_process_still_running()
            self.firefox.quit()
            if self.firefox in global_webdriver_set:
                global_webdriver_set.remove(self.firefox)
        except Exception as e:
            logger.error(e)

    def _clear(self) -> NoReturn:
        """Clear the cookie and cache.

        Restart it becasue no api.
        """
        self.firefox.delete_all_cookies()
        self.firefox.get("about:blank")
        self.firefox.delete_all_cookies()

    def get_driver(self) -> Firefox:
        return self.firefox
