from abc import abstractmethod
from typing import *


# FirefoxScraper, AppiumScraper, wait_block = None, None, None


def check_property(property: str, value):
    def need_activated(func) -> Callable:
        def wrapper(obj, *args, **kwargs):
            property_vale = getattr(obj, property)

            if property_vale != value:
                raise Exception('Scraper must be activated.')

            return func(obj, *args, **kwargs)

        return wrapper

    return need_activated


class Scraper(object):
    """
    The base class of Scraper.

    Define the common methods and the abstract methods of a scraper.

    Args:
        _attached (bool): The activated state.

    """
    _attached: bool = False

    def __init__(self, attach: bool = False):
        if attach:
            self.scraper_attach()

    @property
    def attached(self) -> bool:
        return self._attached

    def scraper_attach(self) -> bool:
        """
        Attach the driver.

        Try to invoke _attach and set the attached to True.

        Returns:
            bool: attached.
        """

        self._attached = True

        return self.attached

    def scraper_detach(self) -> bool:
        """
        Detach the driver.

        Try to invoke the _detach and set attach to Fasle 

        Returns:
            bool: attached.
        """
        self._attached = False

        return self.attached

    def scraper_restart(self) -> NoReturn:
        """Restart the driver.
        """
        self.scraper_detach()
        self.scraper_attach()

    # abstract methods

    @abstractmethod
    def _attach(self):
        """
        Create the driver.
        """

    @abstractmethod
    def _detach(self):
        """
        Destroy the driver.
        """

    @abstractmethod
    def _clear(self):
        """
        Clear the driver's session.
        """

    @abstractmethod
    def get_driver(self):
        """
        Get the instance of driver.
        """
