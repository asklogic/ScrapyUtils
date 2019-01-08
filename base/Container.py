from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Any
from base.Conserve import Conserve, allow
from base.Model import Model, ProxyModel
import scrapy_config
import os
import time
import json
import queue

from base.tool import jinglin

# temp
import threading

lock = threading.Lock()


class BaseContainer(object):
    data: queue.Queue

    def __init__(self, timeout=0):
        self.data: queue.Queue[Model] = queue.Queue()
        self.timeout = timeout

    def pop(self) -> Model:
        data = None
        try:
            data = self.data.get(block=True, timeout=0)
        except Exception as e:
            return data
        return data

    def add(self, model: Model):
        self.data.put(model)

    def dump(self):
        pass


class Container(BaseContainer):

    def __init__(self, supply_func=None, conserve: Conserve = None, supply: int = 10, gather: int = 10, timeout=0):
        super().__init__(timeout)
        # max 超出会执行gather方法
        self.gather_limit = gather
        # min 小于会执行supply方法
        self.supply_limit = supply
        # data container
        self.data: queue.Queue[Any] = queue.Queue()
        # conserve to gather data
        self.conserve: Conserve = conserve
        # supply func
        self.supply_func = supply_func

    def pop(self) -> Any:
        lock.acquire()
        if self.supply_func and self.data.qsize() < self.supply_limit / 3:
            self.supply()
        lock.release()

        return super().pop()

    def supply(self):
        supply_data = self.supply_func(self.supply_limit)
        for item in supply_data:
            self.data.put(item)

    def add(self, model: Any):
        if self.conserve and self.data.qsize() >= self.gather_limit:
            self.gather()

        super().add(model)

    def gather(self):
        if self.conserve:
            for i in range(self.gather_limit):
                self.conserve.model(self.data.get())

    def dump(self):
        if self.conserve:
            for i in range(self.data.qsize()):
                self.conserve.model(self.data.get())


class JsonContainer(Container):

    def __init__(self, name, mapper, supply_func=None, supply: int = 10, gather: int = 10, count=30):
        super().__init__(supply_func, None, supply, gather)
        self.count = 0
        self.max_count = count

        self.file_path = os.path.join(scrapy_config.Project_Path, "assets", name + ".json")

        if not os.path.isfile(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

        origin = []
        with open(self.file_path) as f:
            origin = json.load(f)

        # TODO mapper 方法
        for item in origin:
            m = ProxyModel()
            m.ip = item.split(':')[0]
            m.port = item.split(':')[1]
            self.data.put(m)

    def pop(self) -> Any:
        self.count = self.count + 1

        if self.count > self.max_count:
            self.dump_file()
            self.count = 0
        return super().pop()

    def dump_file(self):
        data = []
        q = queue.Queue()
        for i in range(self.data.qsize()):
            item = self.data.get()
            data.append(item.ip + ":" + item.port)
        with open(self.file_path, "w") as f:
            json.dump(data, f)
        for i in range(q.qsize()):
            self.data.put(q.get())

    def dump(self):
        data = []
        for i in range(self.data.qsize()):
            data.append(self.data.get())
        with open(self.file_path, "w") as f:
            json.dump(data, f)


# class ModelContainer(BaseContainer):
#
#     def __init__(self, conserve: Conserve = None, gather: int = 10):
#         super().__init__()
#
#         self.conserve: Conserve = conserve
#         self.gather_limit = gather
#
#     def add(self, model: Model):
#         if self.gather_limit < self.data.qsize():
#             self.gather()
#         super().add(model)
#
#     def gather(self):
#         if self.conserve:
#             for i in range(self.gather_limit):
#                 self.conserve.model(self.data.get())


class SupplyContainer(BaseContainer):

    def __init__(self, supply_func: type, supply: int = 5):
        self.supply_limit = supply
        self.supply_func = supply_func

        super().__init__()

    def pop(self) -> Model:
        if self.data.qsize() < self.supply_limit / 2:
            self.supply()
        return super().pop()

    def supply(self):
        supply_data = self.supply_func(self.supply_limit)
        for item in supply_data:
            self.data.put(item)


class JsonSuContainer(SupplyContainer):

    def __init__(self, supply_func, name, supply: int = 5):
        super().__init__(supply_func, supply)

        file_path = os.path.join(scrapy_config.Project_Path, "assets", name + ".json")

        if not os.path.isfile(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        origin = []
        with open(file_path) as f:
            origin = json.load(f)

        for item in origin:
            self.data.put(origin)


# class Container(object):
#     """
#         pass
#     """
#     data: queue.Queue
#
#     @abstractmethod
#     def __init__(self, conserve: Conserve = None, gather: int = 100, supply: int = 20):
#         # max 超出会执行gather方法
#         self.gather_limit = gather
#         # min 小于会执行supply方法
#         self.supply_limit = supply
#         # data container
#         self.data: queue.Queue[Model] = queue.Queue()
#         # conserve to gather data
#         self.conserve: Conserve = conserve
#
#         self.timeout = 5
#
#     def pop(self) -> Model:
#         if self.data.qsize() < self.supply_limit:
#             self.supply(int(self.supply_limit * 2))
#         return self.data.get(timeout=self.timeout)
#
#     def add(self, model: Model):
#         if self.data.qsize() >= self.gather_limit:
#             self.gather(self.gather_limit)
#         self.data.put(model)
#
#     @abstractmethod
#     def supply(self, number: int):
#         pass
#
#     def gather(self, number: int):
#         """
#         默认gather方法 将model传给conserve
#         :param number:
#         :return:
#         """
#         if self.conserve:
#             for i in range(number):
#                 self.conserve.model(self.data.get(timeout=self.timeout))
#
#     def dump(self):
#         """
#         默认dump方法 会吧所有的model都执行gather方法
#         :return:
#         """
#
#         pass
#
#
# class JsonContainer(Container):
#
#     def __init__(self, name: str, job: str = None, conserve: Conserve = None, gather: int = 100, supply: int = 20):
#         super().__init__(conserve, gather, supply)
#         self.name = name
#
#         if job:
#             file_path = os.path.join(scrapy_config.Project_Path, job, name + ".json")
#         else:
#             file_path = os.path.join(scrapy_config.Project_Path, "assets", name + ".json")
#
#         if not os.path.isfile(file_path):
#             with open(file_path, "w") as f:
#                 json.dump([], f)
#
#         origin = []
#         with open(file_path) as f:
#             origin = json.load(f)
#
#         for item in origin:
#             self.data.put(origin)
#
#     def dump(self):
#         super().dump()
#
#
# class ProxyContainer(Container):
#
#     def supply(self):
#         proxies = jinglin(self.supply_limit)
#         for proxyString in proxies:
#             m = ProxyModel()
#             ip = proxyString.split(":")[0]
#             port = proxyString.split(":")[1]
#             m.ip = ip
#             m.port = port
#             self.data.insert(0, m)


class ProxyTestConserve(Conserve):
    @allow(Model)
    def feed_function(self, model: Model):
        print(model.port)


def test_supply(number: int) -> List[Model]:
    for i in range(10):
        m = ProxyModel()
        m.port = i
        yield m
        pass


if __name__ == '__main__':
    # t = jinglin(1)
    # c = ProxyTestConserve()
    # pc = ProxyContainer(conserve=None, gather=15, supply=5)
    # jsc = JsonSuContainer(jinglin, "test")
    # jsc.pop()
    # c = Container(test_supply, ProxyTestConserve())
    # m = ProxyModel()
    # m.port = 1
    # for i in range(20):
    #     c.add(m)

    js = JsonContainer('test')
    pass
