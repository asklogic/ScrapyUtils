# -*- coding: utf-8 -*-
"""base scraper module.

FirefoxScraper bases on Selenium.webdriver.Firefox.

Todo:
    * unittest.
    * binary or options.binary
"""
from abc import abstractmethod
from typing import NoReturn, Any


class Scraper(object):
    """
    The base class of Scraper.

    Define the common methods and the abstract methods of a scraper.

    只定义了爬取类通用方法的Scraper基类，子类必须实现全部的抽象方法。

    Args:
        attach (bool): Common parameter. Scraper will attach when it initial.

    """
    _attached: bool = False

    def __init__(self, attach: bool = False):
        if attach:
            self.scraper_attach()

    @property
    def attached(self) -> bool:
        """
        The state of scraper's driver.

        Returns:
            bool: State of attached.

        """
        return self._attached

    def scraper_attach(self) -> bool:
        """
        Attach the driver.

        Try to invoke _attach and set the attached to True.

        Returns:
            bool: Property attached.
        """
        if not self.attached:
            try:

                self._attach()
            except Exception as e:
                print(e)
            else:
                self._attached = True

        return self.attached

    def scraper_detach(self) -> bool:
        """
        Detach the driver.

        Try to invoke the _detach and set attach to Fasle

        Returns:
            bool: Property attached.
        """
        if self.attached:
            try:
                self._detach()
            except Exception as e:
                print(e)
            else:
                self._attached = False

        return self.attached

    def scraper_clear(self) -> bool:
        """
        clear the driver.

        Try to invoke the _clear and set attach to Fasle

        Returns:
            bool: Property attached.
        """
        try:
            self._clear()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def scraper_restart(self) -> NoReturn:
        """Restart the driver.
        """
        self.scraper_detach()
        self.scraper_attach()

    # abstract methods

    @abstractmethod
    def _attach(self) -> NoReturn:
        """
        Create the driver.
        """

    @abstractmethod
    def _detach(self) -> NoReturn:
        """
        Destroy the driver.
        """

    @abstractmethod
    def _clear(self) -> NoReturn:
        """
        Clear the driver's session.
        """

    @abstractmethod
    def get_driver(self) -> Any:
        """
        Get the instance of driver.
        """


class TimeoutMixin(object):
    """Common Mixin: Timeout

    提供了基本的timeout属性，默认值为10。

    通过 @TimeoutMixin.timeout.setter 来重写setter。
    Attributes:
        timeout (int): Default timeout value(int).

    """

    _timeout: int = 10

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """Default timeout setter

        Args:
            value (int): Value of Timeout.
        """
        self._timeout = value