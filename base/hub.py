from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator

from multiprocessing.dummy import Process, Queue
import time

from base.Model import Model
from base.Process import Pipeline
from base.log import act, status


class Resource(object):

    def __init__(self, model_class: type(Model), timeout: int, limit: int, feed, pipeline: Pipeline = None):
        self._storage: Queue = Queue()
        self.trigger: bool = True
        self.model: type(Model) = model_class
        self.pipeline: Pipeline = pipeline

        self.limit = limit
        self.thread: Process = None
        self.timeout: int = timeout

        self.feed = feed

    def start(self):
        if self.feed:
            self.thread = Process(target=resource_feed, args=(self,))
        else:
            self.thread = Process(target=resource_dump, args=(self,))

        self.thread.daemon = True

        self.thread.start()

    def set_timeout(self, timeout: int):
        self.timeout = timeout

    def stop(self):
        # 阻塞资源线程
        if self.pipeline:
            self.trigger = False
            self.thread.join(timeout=10)
        else:
            return [self.pop() for i in range(self.size())]

        if self.feed:
            remain = [self.pop() for i in range(self.size())]
            self.pipeline.end_task()
            return remain
        else:
            remain = [self.pop() for i in range(self.size())]

            if dump_processing(remain, self.pipeline):
                self.pipeline.end_task()
                act.info("[Resource] remain dump success")
                return True
            else:
                self.pipeline.end_task()
                act.warning("[Resource] remain dump failed")
                return remain

    def size(self) -> int:
        return self._storage.qsize()

    def add(self, model):
        self._storage.put(model)

    def pop(self):
        return self._storage.get(timeout=5)


def resource_feed(resource: Resource):
    while resource.trigger and resource.pipeline:
        if resource.size() < int(resource.limit / 2):
            try:
                model_list = resource.pipeline.feed_model(resource.model._name, resource.limit)
                if not model_list:
                    raise Exception("process nothing!")
                for model in model_list:
                    resource.add(model)
            except Exception as e:
                act.error("[Resource - Pipeline] feed error - " + str(e))
                act.exception(e)
                time.sleep(1.2)
        time.sleep(0.5)


def resource_dump(resource: Resource):
    to_dump_models = []
    remain = []

    while resource.trigger:
        if resource.size() >= resource.limit:
            try:
                to_dump_models = [resource.pop() for x in range(resource.limit)]
                resource.pipeline.dump_model(to_dump_models)

            except Exception as e:
                act.error("[Resource - Pipeline] dump error - " + str(e))
                act.exception(e)
                [resource.add(x) for x in to_dump_models]
                time.sleep(1.2)
        time.sleep(0.5)

    act.info("[Resource - Pipeline] Dump Thread Finish")


def dump_processing(to_dump_models: List[Model], pipeline: Pipeline):
    try:
        pipeline.dump_model(to_dump_models)
    except Exception as e:
        act.error("[Resource - Pipeline] dump error - " + str(e))
        act.exception(e)
        time.sleep(1)
        return False
    return True


class Hub(object):
    """
    hub
    暂时存储Model 并且可以pop / save Model
    """

    def __init__(self, models: List[type(Model)], pipeline: Pipeline, timeout: int = 10, limit: int = 50,
                 feed: bool = False):

        self.model_list: List[str] = [x._name for x in models]
        # self._models: List[type(Model)] = models
        self.resource_list: List[Resource] = []
        for model in models:
            resource = Resource(model, timeout, limit, feed, pipeline)

            self.resource_list.append(resource)
            # self.producer = threading.Thread(target=pipeline_process, args=(self.res,), daemon=True)

    def activate(self):
        """
        使Resource子线程运行
        :return:
        """
        for resource in self.resource_list:
            if resource.pipeline:
                resource.start()
            else:
                # TODO 没有设置Pipeline1
                pass

    def set_timeout(self, model_name: str, timeout: int):
        if not model_name in self.model_list:
            raise KeyError("Model name {} didn't register in hub".format(model_name))
        resource = self.resource_list[self.model_list.index(model_name)]
        resource.set_timeout(timeout)

    def pop(self, model_name: str):
        if not model_name in self.model_list:
            raise KeyError("Model name {} didn't register in hub".format(model_name))
        resource = self.resource_list[self.model_list.index(model_name)]
        return resource.pop()

    def save(self, model: Model):
        if not model._name in self.model_list:
            raise KeyError("Model name {} didn't register in hub".format(model._name))
        resource = self.resource_list[self.model_list.index(model._name)]
        resource.add(model)

    def remove_pipeline(self, model_name: str):
        if not model_name in self.model_list:
            raise KeyError("Model name {} didn't register in hub".format(model_name))
        resource = self.resource_list[self.model_list.index(model_name)]
        resource.pipeline = None
        resource.timeout = 10

    def replace_pipeline(self, model_name: str, pipeline: Pipeline, limit: 50):
        if not model_name in self.model_list:
            raise KeyError("Model name {} didn't register in hub".format(model_name))
        resource = self.resource_list[self.model_list.index(model_name)]
        resource.pipeline = pipeline
        resource.limit = limit


    # def __del__(self):
    #     self.stop()

    def stop(self):
        act.info("[Hub] Exiting Hub. Stop Resource thread")
        for resource in self.resource_list:
            resource.stop()

        act.info("[Hub] Exited")
