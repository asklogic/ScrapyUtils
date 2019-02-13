from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator, Any
from base.Model import Model, ModelManager, ProxyModel
import json
import redis
from base.lib import Config, ComponentMeta
import random
import os.path as path
import time
import os
from base.tool import jinglin

from scrapy_config import Project_Path
from base.log import act, status


class BaseProcess(object):
    pass


def target(model: type(Model)):
    def wrapper(func):
        def innerwrapper(*args, **kwargs):
            if not issubclass(model, Model):
                raise TypeError("target must be class")
            if isinstance(args[1], model):
                return func(*args, **kwargs)
            else:
                return True

        return innerwrapper

    return wrapper


class ProcessorMeta(ComponentMeta):

    def __new__(cls, name, bases, attrs: dict):
        if not attrs.get("target"):
            attrs["target"] = Model
        return super().__new__(cls, name, bases, attrs)


class Processor(object, metaclass=ProcessorMeta):
    target: type(Model)

    def __init__(self, settings: dict):
        self.count: int = 0
        self.next: Processor = None

    @abstractmethod
    def start_task(self, settings: dict):
        pass

    @abstractmethod
    def start_process(self, number: int, model: str = "Model"):
        pass

    @abstractmethod
    def end_process(self):
        pass

    @abstractmethod
    def end_task(self):
        pass

    @abstractmethod
    def process_item(self, model: Model) -> Any:
        pass


class Pipeline(object):
    head: Processor = None
    processor_list: List[Processor] = []

    def __init__(self, processor_list: List[type(Processor)] = (), settings: Dict[str, str] = {}):
        """
        构建process
        :param processor_list: processor对象列表
        :param settings: config对象中的pipeline键值 默认为空
        """
        self.head: Processor = None
        self.processor_list: List[Processor] = []
        process_count: List[int] = []

        for process in processor_list:
            current_process: Processor = process(settings)
            current_process.start_task(settings)
            self.add_process(current_process)

    def add_process(self, processor: Processor):
        """
        添加processor
        :param processor:
        :return:
        """
        self.processor_list.append(processor)

        current = self.head
        if self.head is None:
            self.head = processor
        else:
            while current.next is not None:
                current = current.next
            current.next = processor

    def process(self, model: Model) -> Tuple[Model, str]:
        """
        处理一个process
        :param model:
        :return:
        """
        index = 0

        current_process = self.head

        last = model

        # result = current_process.process_item(model)
        #
        # # TODO 判定逻辑
        # while current_process.next is not None:
        #     if isinstance(result, Model) :
        #         # 保存此processor返回的model 传至下一个
        #         current_process = current_process.next
        #         index += 1
        #         last = result
        #         result = current_process.process_item(result)
        #     elif bool(result) or result is None:
        #         # 跳过
        #         current_process = current_process.next
        #         index += 1
        #         result = current_process.process_item(last)
        #     elif result is False:
        #         break
        #     else:
        #         break

        result = last
        # fixme 遗留问题
        while current_process is not None:
            if isinstance(result, current_process.target):
                # 保存此processor返回的model 传至下一个

                result = current_process.process_item(last)
                if isinstance(result, Model):
                    last = result
                index += 1
                current_process = current_process.next
            elif not bool(result):
                # 返回False 直接退出

                break
            else:
                # 跳过

                index += 1
                current_process = current_process.next

        return (last, index)

    def feed_model(self, model_name: str, number: int) -> List[Model]:
        """
        feed Model 生成Model
        由ModelManager生成Model 再由processor进行处理(添加各属性
        :param number: 需要生成的model数量
        :param model_name: model 名称
        :return: 返回进过full过滤过的Model 保证Model值都被填满
        """
        list(map(lambda x: x.start_process(number, ModelManager.model_class(model_name)), self.processor_list))

        # TODO
        # FIXME ? wtf ?
        # model_list = []
        # for i in range(number):
        #     m = ModelManager.model(model_name)
        #     print("True id ", id(m.data))
        #
        #     model_list.append(m)
        # [print("List True id ", id(x.data)) for x in model_list]
        # model_list = [ModelManager.model(model_name) for i in range(number)]

        act.debug("[Pipeline] feed model start. Model: {0}  number: {1}".format(model_name, number))
        result_list: List[Model] = []

        for index in range(number):
            # 构建Model
            pure_model = ModelManager.model(model_name)

            # 处理Model
            result: Model = self.process(pure_model)[0]
            # 短路 None
            if result and result.full():
                result_list.append(result)

        list(map(lambda x: x.end_process(), self.processor_list))
        act.info("[Pipeline] feed model finish. Model: {0}  remained number: {1}".format(model_name, len(result_list)))
        return result_list

    def dump_model(self, data: List[Model]):
        """
        dump model 将得到的model交由processor处理保存
        :param data: model 列表
        :return:
        """
        number = len(data)

        list(map(lambda x: x.start_process(number), self.processor_list))
        # act.debug("[Pipeline] dump Model. Model: {0}  number: {1}".format(data[0]._name, len(data)))

        process_status = [0 for x in self.processor_list]
        for model in data:
            index: int = self.process(model)[1]
            process_status[index - 1] = process_status[index - 1] + 1

        for i in range(len(self.processor_list)):
            act.debug(
                "[Pipeline] " + " ".join([str(process_status[i]), "in", self.processor_list[i].__class__.__name__]))
        # act.info("[Pipeline] dump Model finish.")

        list(map(lambda x: x.end_process(), self.processor_list))

    def end_task(self):
        """
        关闭process
        :return:
        """
        list(map(lambda x: x.end_task(), self.processor_list))



class JsonFileProcessor(Processor):

    def __init__(self, settings: dict):
        super().__init__(settings)

        # TODO
        # 文件分卷
        self.part: int = 0
        # 单个文件元素限制
        self.limit: int = 5000
        # 文件名字
        self.name: str = self.__class__.__name__
        # 文件路径

        # data
        self.data: List[Model] = []
        self.mark = str(int(time.time()))[-4:]

        if settings.get("JsonFile"):
            json_setting = settings.get("JsonFile")
            if json_setting.get("mark"):
                self.mark = str(json_setting.get("mark"))

        if settings.get("job"):
            self.dir_path = path.join(Project_Path, settings.get("job"), "data")
        else:
            self.dir_path = path.join(Project_Path, "assets")

        self.detect_save()
        self.detect_exist_file()

    def detect_exist_file(self):

        while os.path.exists(path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(0), ".json"]))) \
                and \
                os.path.exists(
                    path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(self.part + 1), ".json"]))):
            self.part = self.part + 1

        file_path = path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(self.part), ".json"]))
        if os.path.exists(file_path):
            with open(file_path) as f:
                data = json.load(f)
            self.data.extend(data)
            act.info("<<JsonFile>> load exist data. exist file: " + file_path)

    def detect_save(self):
        temp_file = path.join(self.dir_path, self.name + "JsonFileTest.json")
        act.info("<<JsonFile>> Json File path: " + path.join(self.dir_path))
        try:
            if not os.path.exists(self.dir_path):
                os.mkdir(self.dir_path)

            with open(temp_file, "w") as f:
                json.dump([], f)
            os.remove(temp_file)
        except Exception as e:
            print(e.args)
            raise TypeError('<<JsonFile>> cannot dump json file!')

    def save_model(self, model: Model):
        self.data.append(model.pure_data())
        return True

    def dump_to_file(self):
        file_path = path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(self.part), ".json"]))
        with open(file_path, "w") as f:
            json.dump(self.data[:self.limit], f)
            act.info("<<JsonFile>> success dump file. " + file_path)
        self.part += 1
        self.data = self.data[self.limit:]

    def end_process(self):
        while len(self.data) >= self.limit:
            self.dump_to_file()

    def end_task(self):
        act.info("<<JsonFile>> end task! last len:" + str(len(self.data)))
        if self.data:
            self.dump_to_file()

    def process_item(self, model: Model) -> Model:
        self.data.append(model.pure_data())
        return model


class DuplicateProcessor(Processor):

    def __init__(self, settings: dict):
        super().__init__(settings)

        if not settings.get("duplication"):
            # TODO
            # 地址
            self.host: str = "127.0.0.1"
            self.port: int = 6379
            # 数据库索引
            self.db_index: int = 0

        name = self.__class__.__name__
        if settings.get("job"):
            job = settings.get("job")
            self.set_base(job, self.target._name, name)
        else:
            self.set_base(self.target._name, name)

        # redis数据库
        self.db: redis.Redis = None

        # 链接
        self.connect()

    def connect(self):
        if not self.db:
            self.db = redis.Redis(host=self.host, port=self.port, db=self.db_index, decode_responses=True)

        try:
            self.db.keys("1")
        except redis.ConnectionError as e:
            print(e.args)
            raise TypeError('redis connect failed')

    def set_base(self, *args):
        self.base = ":".join(args)

    def key(self, key: str) -> str:
        return ":".join([self.base, key])

    def exist_identification(self, key_name) -> bool:
        """
        存在key 返回True
        不存在key 返回False
        :param key_name:
        :return:
        """
        return self.db.exists(self.key(key_name))

    def save_identification(self, key_name):
        """
        保存
        :param key_name:
        :return:
        """
        self.db.set(self.key(key_name), 1)

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


class Proxy_Processor(Processor):
    target = ProxyModel

    def start_process(self, number: int, model: str = "Model"):
        self.proxy_data: [] = jinglin(number)

    def process_item(self, model: ProxyModel) -> Any:
        proxy = self.proxy_data.pop().split(":")
        model.ip = proxy[0]
        model.port = proxy[1]
        return model



