from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator

from base.Model import Model

import threading
lock = threading.Lock()


class BaseConserve(object):
    pass


class Conserve(object):

    @abstractmethod
    def start_conserve(self):
        pass

    @abstractmethod
    def end_conserve(self):
        pass

    @abstractmethod
    def feed_function(self, model: Model):
        pass

    def model(self, model: Model):
        """
        将model分别给赋给conserve所有feed开头的方法
        :param model: model实例
        :return:
        """
        for func in dir(self):
            if func.startswith("feed"):
                f = getattr(self, func)
                f(model)


def allow(model: type):
    def wrapper(func):
        def innerwrapper(*args, **kwargs):
            if not type(model) == type:
                raise TypeError("allow must be class")
            if isinstance(args[1], model):
                return func(*args, **kwargs)
            else:
                pass

        return innerwrapper

    return wrapper
