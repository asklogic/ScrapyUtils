from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Any
from base.Conserve import Conserve, allow
from base.Model import Model, ProxyModel
import scrapy_config
import os
import time
import json

from base.tool import jinglin

# temp
import threading

lock = threading.Lock()


class Container(object):
    """
        pass
    """
    data: list = []

    # @abstractmethod
    def __init__(self, conserve: Conserve = None, gather: int = 100, supply: int = 20):
        # max
        self.gather_limit = gather
        # min
        self.supply_limit = supply
        # data container
        self.data: List[Model] = []
        # conserve to gather data
        self.conserve: Conserve = conserve

    def end(self):
        self.gather(len(self.data))

    def pop(self) -> Model:
        if len(self.data) < self.supply_limit:
            self.supply(int(self.supply_limit * 2))
        return self.data.pop()

    def add(self, model: Model):
        if len(self.data) >= self.gather_limit:
            self.gather(self.gather_limit)
        self.data.insert(0, model)

    @abstractmethod
    def supply(self, number: int):
        pass

    def gather(self, number: int):
        if self.conserve:
            for i in range(number):
                self.conserve.model(self.data.pop())


class JsonContainer(Container):
    name = "test"

    def __init__(self, conserve: Conserve = None, gather: int = 100, supply: int = 20):
        super().__init__(conserve, gather, supply)

        # with open(os.path.join(scrapy_config.Project_Path, "assets", str(int(time.time())) + ".json")) as f:
        # with open(os.path.join(scrapy_config.Project_Path, "assets", self.name + ".json"), "w") as f:
        #     json.dump([],f)
        file_path = os.path.join(scrapy_config.Project_Path, "assets", self.name + ".json")
        if not os.path.isfile(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        origin = []
        with open(file_path) as f:
            origin = json.load(f)

        self.data.extend(origin)
        pass

    def gather(self, number: int):
        data = []

        with open(os.path.join(scrapy_config.Project_Path, "assets", self.name + ".json")) as f:
            data.extend(json.load(f))

        for i in range(number):
            data.append(self.data.pop())

        with open(os.path.join(scrapy_config.Project_Path, "assets", self.name + ".json"), "w") as f:
            json.dump(data, f)


class ProxyContainer(Container):
    def supply(self):
        proxies = jinglin(self.supply_limit)
        for proxyString in proxies:
            m = ProxyModel()
            ip = proxyString.split(":")[0]
            port = proxyString.split(":")[1]
            m.ip = ip
            m.port = port
            self.data.insert(0, m)


class ProxyTestConserve(Conserve):
    @allow(Model)
    def feed_function(self, model: Model):
        print(model.ip)


if __name__ == '__main__':
    # t = jinglin(1)
    # c = ProxyTestConserve()
    # pc = ProxyContainer(conserve=None, gather=15, supply=5)
    pc = JsonContainer(conserve=None, gather=10, supply=5)


    pass
