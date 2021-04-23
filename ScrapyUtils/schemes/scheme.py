# -*- coding: utf-8 -*-
"""Consumer module.


Todo:
    * For module TODOs

"""
from abc import abstractmethod
from typing import List, Callable, Any, Type, Union
from time import sleep

from concurrent.futures import ThreadPoolExecutor

from ScrapyUtils.log import getLogger

core_logger = getLogger('core')
scheme_state_logger = getLogger('scheme_state')
scheme_load_logger = getLogger('scheme_load')


class Scheme(object):

    @abstractmethod
    def deploy(self):
        pass

    @abstractmethod
    def verify(self) -> bool:
        return True

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def load_context(self):
        pass

    @abstractmethod
    def check_context(self):
        pass


from ScrapyUtils.libs import FireFoxScraper


class Scraper(Scheme):
    pass


class Element(Scheme):
    pass





def execute_function(executor: ThreadPoolExecutor, func: Callable, args: tuple) -> Union[bool, Any]:
    function_name = func.__name__

    future = executor.submit(func, *args)

    try:
        result = future.result()
    except Exception as e:
        scheme_state_logger.info('{0} failed.'.format(function_name.capitalize()), extra={'state': 'FAILED'})
        core_logger.exception('failed ', exc_info=e, extra={'state': 'FAILED'})
        return False

    else:
        scheme_state_logger.info('{0} done.'.format(function_name.capitalize()), extra={'state': 'SUCCESS'})
        return result


class Root(object):
    schemes: List[Type[Scheme]] = []

    context: dict = None

    def __init__(self):
        self.executor = ThreadPoolExecutor(1)
        pass



    def load(self, scheme: Type[Scheme]) -> bool:
        if scheme in self.schemes:
            return True

        scheme_load_logger.info('----- Loading: {}. -----'.format(scheme.__name__))

        if execute_function(self.executor, scheme.deploy, (scheme,)) is False:
            return False

        if not execute_function(self.executor, scheme.verify, (scheme,)):
            return False

        # scheme_load_logger.debug('--- Load <{}> success. ---'.format(scheme.__name__))
        self.schemes.append(scheme)
        sleep(0.618)
        return True

    def unload(self, scheme: Type[Scheme]):
        if scheme not in self.schemes:
            return True

        scheme_load_logger.info('--- Unloading <{}> scheme. ---'.format(scheme.__name__))

        # exit
        if execute_function(self.executor, scheme.exit, (scheme,)) is False:
            return False

        # scheme_load_logger.debug('--- UnLoad <{}> success. ---'.format(scheme.__name__))
        self.schemes.remove(scheme)
        sleep(0.314)
        return True


    def exit(self):
        # remove list item.
        while self.schemes:
            self.unload(self.schemes[0])


class Error(Scheme):

    def deploy(self):
        raise Exception()


if __name__ == '__main__':
    root = Root()


    root.load(Error)
