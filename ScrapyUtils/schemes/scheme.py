# -*- coding: utf-8 -*-
"""Scheme module.

在Python项目中的模拟一个service的Scheme类，负责一个服务的管理。

提供了如下几个方法:
    1. start - 开启

    2. verify - 校验，类似于status

    3. stop - 退出

每一个方法的返回值代表了该方法的运行情况:
    1. True & None - 返回True或者返回空代表正确运行

    2. False - 返回False代表逻辑错误。

    3. Error - 运行报错

case 1 该步骤正常启动，logger返回状态 [SUCCESS].

case 2 该步骤错误，logger返回状态 [FAILED].

case 3 该步骤错误，logger返回状态 [ERROR].



Todo:
    * For module TODOs

"""
from abc import abstractmethod
from typing import List, Callable, Any, Type, Union, Optional
from types import FunctionType, MethodType
from time import sleep

from concurrent.futures import ThreadPoolExecutor

from ScrapyUtils.log import getLogger

import ScrapyUtils.schemes

base_logger = getLogger('base')
scheme_state_logger = getLogger('scheme_state')
scheme_load_logger = getLogger('scheme_load')


class SchemeDecoratorMixin(object):

    @classmethod
    def register_start(cls, func: FunctionType):

        assert isinstance(func, FunctionType)
        if func.__code__.co_argcount == 0:

            def register_wrapper(cls):
                func()

            cls.start = MethodType(register_wrapper, cls)
        else:
            cls.start = MethodType(func, cls)

    @classmethod
    def register_verify(cls, func: FunctionType):
        assert isinstance(func, FunctionType)
        if func.__code__.co_argcount == 0:
            def register_wrapper(cls):
                func()

            cls.verify = MethodType(register_wrapper, cls)
        else:
            cls.verify = MethodType(func, cls)

    @classmethod
    def register_stop(cls, func: FunctionType):
        assert isinstance(func, FunctionType)
        if func.__code__.co_argcount == 0:
            def register_wrapper(cls):
                return func()

            cls.verify = MethodType(register_wrapper, cls)
        else:
            cls.verify = MethodType(func, cls)


class Scheme(SchemeDecoratorMixin):

    @classmethod
    @abstractmethod
    def start(cls):
        pass

    @classmethod
    @abstractmethod
    def verify(cls) -> bool:
        return True

    @classmethod
    @abstractmethod
    def stop(cls):
        pass

    @classmethod
    @abstractmethod
    def load_context(cls):
        pass

    @classmethod
    @abstractmethod
    def check_context(cls):
        pass


def execute_function(executor: ThreadPoolExecutor, func: Callable, target_method='scheme') -> Optional[bool]:
    function_name = func.__name__

    future = executor.submit(func)

    try:
        result = future.result()

    # case 3
    except Exception as e:
        scheme_state_logger.info(
            '{0} error.'.format(function_name.capitalize()),
            extra={'state': 'ERROR', 'method': target_method}
        )
        base_logger.exception('Error message ', exc_info=e, extra={'state': 'FAILED'})
        return False

    else:
        # case 1
        if result is True or result is None:
            scheme_state_logger.info(
                "The function '{0}' done.".format(function_name.capitalize()),
                extra={'state': 'SUCCESS', 'method': target_method}
            )
            return True

        # case 2
        else:
            scheme_state_logger.info(
                "The function '{0}' done.".format(function_name.capitalize()),
                extra={'state': 'SUCCESS', 'method': target_method}
            )
            return False


class Root(object):
    schemes: List[Type[Scheme]] = []

    context: dict = None

    def __init__(self):
        self.executor = ThreadPoolExecutor(1)
        pass

    def load(self, scheme: Type[Scheme]) -> bool:
        if scheme in self.schemes:
            return True

        base_logger.info('----- Loading: <{}>. -----'.format(scheme.__name__))

        if not execute_function(self.executor, scheme.start, target_method='start'):
            return False

        if not execute_function(self.executor, scheme.verify, target_method='verify'):
            return False

        self.schemes.append(scheme)
        sleep(0.618)
        return True

    def unload(self, scheme: Type[Scheme]):
        if scheme not in self.schemes:
            return True

        scheme_load_logger.info('--- Unloading <{}> scheme. ---'.format(scheme.__name__))

        # exit
        if not execute_function(self.executor, scheme.stop, target_method='stop'):
            return False

        # scheme_load_logger.debug('--- UnLoad <{}> success. ---'.format(scheme.__name__))
        self.schemes.remove(scheme)
        sleep(0.314)
        return True

    def exit(self):
        # remove list item.
        while self.schemes:
            if not self.unload(self.schemes[0]):
                break

        if not self.schemes:
            base_logger.info('--- Exit <{}> success. ---'.format(self.__class__.__name__))
            return True
        base_logger.info('--- Exit <{}> failed. ---'.format(self.__class__.__name__))
        return False


class Demo(Scheme):
    pass


@Demo.register_start
def inner(cls):
    print('inner ', cls)
    pass


@Demo.register_verify
def verify():
    print('verify')
    return False


if __name__ == '__main__':
    root = Root()

    root.load(Demo)

    root.exit()
