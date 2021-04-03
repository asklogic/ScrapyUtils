# -*- coding: utf-8 -*-
"""Consumer module.

生产者线程模块，提供了Producer类。

Producer样例：



Todo:
    * For module TODOs

"""
from abc import abstractmethod
from threading import Lock
from typing import List, NoReturn, Any, Union

from queue import Queue, Full
from time import sleep

from .base_thread import BaseThread

class Producer(BaseThread):
    pass
