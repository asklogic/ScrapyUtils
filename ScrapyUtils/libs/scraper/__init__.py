# -*- coding: utf-8 -*-
"""The scraper module for scrapy data.

爬取核心类，负责与网页或者其他数据来源交互，获得数据。

其中设定了爬取基本类Scraper，规定了所有爬取类的通用方法，具体的其他方法需要通过子类的Mixin导入。



样例:
    启动自带的Scraper或者自定义Scraper::

        scraper = RequestScraper()

    必须先attach之后再进行使用::

        scraper.scraper_attach()

    通用方法包括'重启'、'清理'和'返回爬取实例'，都需要子类自定义::

        scraper.scraper_clear()
        scraper.scraper_restart()
        scraper.get_driver()

    对于基于Selenium之类的Scraper，最好执行退出::

        scraper.scraper_detach()



Todo:
    * Appium Scraper
    * Chrome Scraper
"""

from abc import abstractmethod
from typing import *


def check_property(property_name: str, value: Any, assert_content='Scraper must be activated.'):
    """Check the property when the method be invoked.

    类属性检查装饰器，调用时通过属性名字检查属性, 属性的值不等于理想值将会抛出异常。

    If the property's value isn't equal to value raise Exception.
    """

    def need_activated(func) -> Callable:
        def check_property_inner(obj, *args, **kwargs):
            """check_property inner."""
            property_vale = getattr(obj, property_name)

            assert property_vale == value, assert_content

            return func(obj, *args, **kwargs)

        return check_property_inner

    return need_activated


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
