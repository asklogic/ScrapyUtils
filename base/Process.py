from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator, Any
from base.Model import Model
import json
import redis
from base.lib import Config
import random
import os.path as path
import time

from scrapy_config import Project_Path


class BaseProcess(object):
    pass


def target(model: type):
    def wrapper(func):
        def innerwrapper(*args, **kwargs):
            if not type(model) == type:
                raise TypeError("allow must be class")
            if isinstance(args[1], model):
                return func(*args, **kwargs)
            else:
                return True

        return innerwrapper

    return wrapper


# class _Process(BaseProcess):
#
#     def task_start(self):
#         pass
#
#     def task_end(self):
#         pass
#
#     @abstractmethod
#     def process_model(self, model: Model):
#         pass
# class RedisDuplicateGate(_Process):
#     db: redis.Redis
#
#     def __init__(self, origin_key: str):
#         r = redis.Redis()
#         self.r = r
#         self.origin_key = origin_key
#
#     def load_identification(self):
#         pass
#
#     def check_identification(self, filed):
#         key = ":".join([self.origin_key, filed])
#
#         res = self.db.get(key)
#         if res:
#             return True
#         else:
#             return False
#
#     def save_identification(self, filed: str):
#         key = ":".join([self.origin_key, filed])
#
#         self.db.set(key, 1)
#
#     def process_model(self, model: Model):
#         pass
# class TestProcess(_Process):
#
#     def process_model(self, model: Model) -> Model:
#         print(model.ip)
#         return model
# class OtherProcess(_Process):
#
#     def process_model(self, model: Model):
#         if random.random() > 0.5:
#
#             return model
#         else:
#             return None
# class _Pipeline(object):
#
#     def __init__(self):
#         self.process_list: List[_Process] = []
#
#     def add_process(self, process: _Process):
#         self.process_list.append(process)
#
#     def process_models(self, item: Model):
#         current_model = item
#         for current in self.process_list:
#             if isinstance(current_model, Model):
#                 print("is model instance")
#             elif bool(current_model):
#                 print("return true")
#             else:
#                 print("abort")
#
#             if current_model:
#                 current_model = current.process_model(current_model)
#
#     pass


class Process(object):
    def __init__(self):
        self.next: Process = None

    @abstractmethod
    def start_task(self, config: Config = None):
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

    def start_task(self, config: Config = None):
        list(map(lambda x: x.start_task(config), self.process_list))

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

    def process_all(self, data: List[Model], container_name=""):
        print("process all ", container_name)
        list(map(lambda x: x.start_process(), self.process_list))

        for model in data:
            self.process(model)

        list(map(lambda x: x.end_process(), self.process_list))

    def process(self, model: Model):

        current_process = self.head

        last = model
        result = current_process.process_item(model)

        while current_process.next is not None:

            if isinstance(result, Model):
                current_process = current_process.next
                last = result
                result = current_process.process_item(result)
            # TODO
            elif bool(result) or result is None:
                current_process = current_process.next
                result = current_process.process_item(last)
            elif result is False:
                break
            else:
                break


class JsonFileProcess(Process):
    part: int
    name: str
    data: List[Model]
    limit: int
    file_path: int
    time: str

    def start_task(self, config: Config = None):
        self.part = 0
        if not hasattr(self, "name"):
            self.name = self.__class__.__name__
        self.file_path = path.join(Project_Path, config.job, "data", self.name)
        self.limit = 10000
        self.data: List[Model] = []

        self.time = str(int(time.time()))[-4:]
        print("start json process!")
        print("file path: ", self.file_path)

    def dump_to_file(self):
        file = self.file_path + self.time + "-part" + str(self.part) + ".json"
        print(file)
        with open(file, "w") as f:
            json.dump(self.data[:self.limit], f)
            print("success dump file")
        self.part += 1
        self.data = self.data[self.limit:]

    def end_process(self):
        while len(self.data) >= self.limit:
            self.dump_to_file()

    def end_task(self):
        print("end task! last len:", len(self.data))
        if self.data:
            self.dump_to_file()

    def process_item(self, model: Model) -> Model:
        self.data.append(model.pure_data())
        return model


class DuplicateProcess(Process):

    def start_task(self, config: Config = None):
        self.db = redis.Redis(decode_responses=True)
        if not hasattr(self, "name"):
            self.name = self.__class__.__name__

        self.base = ":".join([config.job, self.name]) + ":"

        print("Duplication! ", self.base)

    def exist_identification(self, key):
        """
        存在key 返回True
        不存在key 返回False
        :param key:
        :return:
        """
        return self.db.exists(self.base + key)

    def save_identification(self, key):
        self.db.set(self.base + key, 1)

    def check_identification(self, key):
        """
        查询并且保存
        存在 返回False
        不存在 返回True
        :param key:
        :return:
        """
        if self.exist_identification(key):
            return False
        else:
            self.save_identification(key)
            return True


# class FirstProcess(Process):
#
#     def process_item(self, model: Model):
#         print(model.ip)
#         return model
#
#
# class SecondProcess(Process):
#     def process_item(self, model: Model):
#         print(model.port)
#         return model
#
#
# class OriginProcess(Process):
#     def process_item(self, model: Model):
#         if random.random() > 0.5:
#             return model


if __name__ == '__main__':
    from base.Model import ProxyModel

    pipeline = Pipeline()

    # pipeline.add_process(OriginProcess())
    # pipeline.add_process(FirstProcess())
    # pipeline.add_process(SecondProcess())

    modelList = []
    for i in range(2000):
        m = ProxyModel()
        m.ip = "1.2.2.3"
        m.port = "1234"
        modelList.append(m)
        pipeline.process(m)
