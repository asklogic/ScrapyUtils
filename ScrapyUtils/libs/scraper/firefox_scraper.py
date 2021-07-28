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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from ScrapyUtils.libs.scraper import Scraper

# default logger
logger = getLogger('firefox')

# system switch
if 'Win' in platform.system():
    platform_suffix = '.exe'
else:
    platform_suffix = ''

firefox_path = ''.join(['firefox', os.sep, 'firefox', platform_suffix])
"""str: The firefox path"""
driver_path = ''.join(['firefox', os.sep, 'geckodriver', platform_suffix])
"""str: The geckodriver path"""

global_webdriver_set: Set[Firefox] = set()


# setter function
def set_firefox_path(path: str) -> NoReturn:
    """Set the global variable firefox_path.

    The firefox will attach the browser with this path.

    Default value is "{project}/firefox/firefox"

    Args:
        path (str): The path of browser.
    """
    global firefox_path
    firefox_path = path


def set_driver_path(path: str) -> NoReturn:
    """Set the global variable driver_path.

    The driver_path is the path of webdriver.

    Default value is "{project}/firefox/geckodriver"

    Args:
        path (str): The path of geckodriver
    """
    global driver_path
    driver_path = path


def exit_all_firefox_webdriver() -> NoReturn:
    """Exit all firefox webdriver without scraper_detach.
    """
    for webdriver in global_webdriver_set:
        webdriver.quit()


class FireFoxBase(object):
    firefox: Firefox = None


class FireFoxOptionsBase(object):
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
    binary: FirefoxBinary = None
    driver_path: str = None

    def __init__(self):
        assert os.path.isfile(driver_path), f'Path: {driver_path} no geckodriver file.'
        assert os.path.isfile(firefox_path), f'Path: {firefox_path} no firefox file.'

        self.options = FirefoxOptions()
        self.binary = FirefoxBinary(firefox_path)
        self.driver_path = driver_path


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
                 image: bool = False,
                 attach: bool = False
                 ):
        # execute init method.
        FirefoxBinaryBase.__init__(self)

        self.set_js(js)
        self.set_headless(headless)
        self.set_image(image)

        Scraper.__init__(self, attach)

    def _attach(self) -> NoReturn:
        """Attach the Firefox instance.

        Create a firefox instance by options and binary.

        """
        self.firefox = Firefox(options=self.options,
                               firefox_binary=self.binary,
                               executable_path=self.driver_path)

        self.firefox.get("about:config")
        self.firefox.find_element_by_id("showWarningNextTime").click()
        self.firefox.find_element_by_id("warningButton").click()
        self.firefox.get("about:blank")

        self.set_timeout(10)

        global_webdriver_set.add(self.firefox)

    def _detach(self) -> NoReturn:
        """Detach the firefox instacne.

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
