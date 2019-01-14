from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator, Any
from base.Model import Model

import redis


class BaseProcess(object):
    pass


class _Process(BaseProcess):

    def task_start(self):
        pass

    def task_end(self):
        pass

    @abstractmethod
    def process_model(self, model: Model):
        pass


class RedisDuplicateGate(_Process):
    db: redis.Redis

    def __init__(self, origin_key: str):
        r = redis.Redis()
        self.r = r
        self.origin_key = origin_key

    def load_identification(self):
        pass

    def check_identification(self, filed):
        key = ":".join([self.origin_key, filed])

        res = self.db.get(key)
        if res:
            return True
        else:
            return False

    def save_identification(self, filed: str):
        key = ":".join([self.origin_key, filed])

        self.db.set(key, 1)

    def process_model(self, model: Model):
        pass


class TestProcess(_Process):

    def process_model(self, model: Model) -> Model:
        print(model.ip)
        return model


import random


class OtherProcess(_Process):

    def process_model(self, model: Model):
        if random.random() > 0.5:

            return model
        else:
            return None


class _Pipeline(object):

    def __init__(self):
        self.process_list: List[_Process] = []

    def add_process(self, process: _Process):
        self.process_list.append(process)

    def process_models(self, item: Model):
        current_model = item
        for current in self.process_list:
            if isinstance(current_model, Model):
                print("is model instance")
            elif bool(current_model):
                print("return true")
            else:
                print("abort")

            if current_model:
                current_model = current.process_model(current_model)

    pass


class Process(object):
    def __init__(self):
        self.next: Process = None

    @abstractmethod
    def start_task(self):
        pass

    @abstractmethod
    def end_task(self):
        pass

    @abstractmethod
    def start_process(self):
        pass

    @abstractmethod
    def end_process(self):
        pass

    @abstractmethod
    def process_item(self, model: Model) -> Any:
        pass


class Pipeline(object):
    head: Process = None
    process_list: List[Process] = []

    def __init__(self):
        self.head: Process = None

    def start_task(self):
        list(map(lambda x: x.start_task(), self.process_list))

    def end_task(self):
        list(map(lambda x: x.end_task(), self.process_list))

    def add_process(self, process: Process):
        self.process_list.append(process)

        current = self.head
        if self.head is None:
            self.head = process
        else:
            while current.next is not None:
                current = current.next
            current.next = process

    def process_all(self, data: List[Model], container_name = ""):
        print("process all ", container_name)
        list(map(lambda x: x.start_process(), self.process_list))

        for model in data:
            self.process(model)

        list(map(lambda x: x.end_process(), self.process_list))

    def process(self, model: Model):

        current = self.head

        result = current.process_item(model)

        while current.next is not None and result:

            if isinstance(result, object):
                # print("return model")
                current = current.next
                result = current.process_item(model)

            elif bool(result):
                # print("return true")
                break
            else:
                # print("return false")
                break


class FirstProcess(Process):

    def process_item(self, model: Model):
        print(model.ip)
        return model


class SecondProcess(Process):
    def process_item(self, model: Model):
        print(model.port)
        return model


class OriginProcess(Process):
    def process_item(self, model: Model):
        if random.random() > 0.5:
            return model


if __name__ == '__main__':
    from base.Model import ProxyModel

    pipeline = Pipeline()

    pipeline.add_process(OriginProcess())
    pipeline.add_process(FirstProcess())
    pipeline.add_process(SecondProcess())

    modelList = []
    for i in range(2000):
        m = ProxyModel()
        m.ip = "1.2.2.3"
        m.port = "1234"
        modelList.append(m)
        pipeline.process(m)
