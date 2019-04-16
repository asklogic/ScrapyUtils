from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator

from multiprocessing.dummy import Process, Queue
import time
import warnings

from base.Model import Model, ModelManager
from base.Process import Pipeline, Processor
from base.log import act, status
from base.lib import Setting


class Resource(object):
    _storage: Queue

    timeout: int = 5
    dump_limit: int = 500
    feed_limit: int = 500
    model: type(Model) = Model

    dump_pipeline: Pipeline = None
    feed_pipeline: Pipeline = None

    # sub thread
    dump_thread: Process = None
    feed_thread: Process = None

    process_failed: int = 2
    failed_retry: int = 3

    name: str

    trigger: bool

    def __init__(self, model_class: type(Model) = Model, timeout: int = 5,
                 dump_limit: int = 500, feed_limit: int = 100,
                 feed_pipeline: Pipeline = None, dump_pipeline: Pipeline = None,
                 process_failed: int = 2, failed_retry: int = 3, name: str = None):
        # init property
        self._storage: Queue = Queue()
        self.trigger: bool = True

        # param
        self.model: type(Model) = model_class
        self.timeout: int = timeout
        self.dump_limit = dump_limit
        self.feed_limit = feed_limit

        if int(feed_limit * 1.5) > dump_limit and self.feed_pipeline and self.dump_pipeline:
            warnings.warn('feed limit is bigger than dump limit. Double dump limit')
            self.dump_limit = dump_limit * 2

        # fixme
        # TODO  空processor pipeline会无限导入?

        self.feed_pipeline: Pipeline = feed_pipeline
        self.dump_pipeline: Pipeline = dump_pipeline

        self.process_failed = process_failed
        self.thread: Process = None

        if not name:
            name = model_class._name
        self.name = name

        # other
        ModelManager.add_model(model_class=model_class)

    def start(self):

        self.dump_thread = Process(target=resource_dump, args=(self,))
        self.feed_thread = Process(target=resource_feed, args=(self,))

        self.dump_thread.daemon = True
        self.feed_thread.daemon = True

        self.dump_thread.start()
        self.feed_thread.start()

    def set_timeout(self, timeout: int):
        self.timeout = timeout

    def stop(self, dump_all=False) -> List[Model] or None:
        # block resource process
        self.trigger = False
        if self.feed_thread:
            self.feed_thread.join(timeout=10)

        if self.dump_thread:
            self.dump_thread.join(timeout=10)

        # remain model to dump
        if dump_all and self.dump_pipeline:
            remain = [self.pop() for i in range(self.size())]
            result = dump_processing(remain, self.dump_pipeline)

            if self.dump_pipeline:
                self.dump_pipeline.end_task()
            if self.dump_pipeline:
                self.dump_pipeline.end_task()

            if result:
                return []
            else:
                return remain

        else:
            if self.dump_pipeline:
                self.dump_pipeline.end_task()
            if self.dump_pipeline:
                self.dump_pipeline.end_task()

            remain = [self.pop() for i in range(self.size())]
            return remain

    def size(self) -> int:
        return self._storage.qsize()

    def add(self, model, force=True):
        if isinstance(model, self.model):
            self._storage.put(model)
        elif force:
            warnings.warn("model should'n add in this Resource")
            self._storage.put(model)
        else:
            warnings.warn("model can not add in this Resource")

    def pop(self):
        return self._storage.get(timeout=self.timeout)


def resource_feed(resource: Resource):
    retry = resource.failed_retry

    while resource.trigger and resource.feed_pipeline and retry > 0:
        if resource.size() < int(resource.feed_limit / 2):
            try:
                model_list = resource.feed_pipeline.feed_model(resource.model._name, resource.feed_limit)
                if not model_list:
                    raise Exception("process nothing!")
                for model in model_list:
                    resource.add(model)

            except Exception as e:
                act.error("[Resource {0} feed error ] retry: {1}".format(resource.name, retry))
                act.exception(e)

                retry -= 1
                time.sleep(resource.process_failed)
        time.sleep(0.33)


def resource_dump(resource: Resource):
    to_dump_models = []

    retry = resource.failed_retry
    while resource.trigger and resource.dump_pipeline and retry > 0:
        if resource.size() >= resource.dump_limit:
            try:
                to_dump_models = [resource.pop() for x in range(resource.dump_limit)]
                resource.dump_pipeline.dump_model(to_dump_models)

            except Exception as e:
                act.error("[Resource {0}] dump error ({1}) ] - {2}".format(resource.name, retry, str(e)))
                act.exception(e)

                retry -= 1
                [resource.add(x) for x in to_dump_models]
                time.sleep(resource.process_failed)
        time.sleep(0.33)
    if resource.dump_pipeline:
        act.info("[Resource {0}] Dump Thread Finish".format(resource.name))


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
    model_list: List[str] = []
    resource_list: List[Resource] = []

    activated = False

    def __init__(self, models: List[type(Model)] = (Model,), dump_processors=(), feed_processors=(), setting=Setting()):

        pass
        self.model_list: List[str] = [x._name for x in models]

        self.activated = False
        self.resource_list: List[Resource] = []

        for processor in dump_processors:
            pass

        for processor in feed_processors:
            pass

        # activated 先后
        # TODO setting 默认参数问题
        for model in models:
            resource = Resource(model, timeout=setting.Timeout,
                                dump_limit=setting.DumpLimit, feed_limit=setting.FeedLimit,
                                process_failed=setting.PipelineFailedBlock, failed_retry=setting.PipelineFailedRetry)
            self.resource_list.append(resource)

    def activate(self):
        """
        使Resource子线程运行
        :return:
        """
        if self.activated:
            warnings.warn('hub has already activated')
        for resource in self.resource_list:
            resource.start()

    def set_timeout(self, model_name: str, timeout: int):
        if not model_name in self.model_list:
            raise KeyError("Model name {} didn't register in hub".format(model_name))
        resource = self.resource_list[self.model_list.index(model_name)]
        resource.set_timeout(timeout)

    def get_number(self, model_name: str) -> int:
        resource = self._resource(model_name)
        return resource.size()

    def _resource(self, model_name) -> Resource:

        if len(self.model_list) is 1 and self.model_list[0] is 'Model':
            resource = self.resource_list[0]
        elif model_name not in self.model_list:
            raise KeyError("Model name {} didn't register in hub".format(model_name))
        else:
            resource = self.resource_list[self.model_list.index(model_name)]

        return resource

    def pop(self, model_name: str) -> Model:
        resource = self._resource(model_name)
        return resource.pop()

    def save(self, model: Model):
        resource = self._resource(model_name=model._name)
        resource.add(model)

    def add_dump_pipeline(self, model_name: str, pipeline: Pipeline):

        if self.activated:
            warnings.warn('hub has already activated')
            return
        resource = self._resource(model_name)
        resource.dump_pipeline = pipeline

    def add_feed_pipeline(self, model_name: str, pipeline: Pipeline):
        if self.activated:
            warnings.warn('hub has already activated')
            return

        resource = self._resource(model_name)
        resource.feed_pipeline = pipeline

    def remove_pipeline(self, model_name: str):
        if self.activated:
            warnings.warn('hub has already activated')
            return

        resource = self._resource(model_name)

        resource.feed_pipeline = None
        resource.dump_pipeline = None

    # def __del__(self):
    #     self.stop()

    def stop(self, dump_all=False):
        act.info("[Hub] Exiting Hub. Stop Resource thread")
        for resource in self.resource_list:
            resource.stop(dump_all)

        act.info("[Hub] Exited")
