import json
import os
import time
from os import path as path
from typing import List, Dict, Generator, Any

import redis

from base.Model import ModelManager, TaskModel, Model, ProxyModel
from base.Process import Processor
from base.Scraper import Scraper
from base.log import act
from base.scheme import Action, Parse
from base.task import Task
from base.tool import xpathParse, jinglin, xpathParseList
from scrapy_config import Project_Path

ModelManager.add_model(TaskModel)


class DefaultAction(Action):
    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)


class DefaultXpathParse(Parse):
    mapper_model: Model = None
    auto_yield: bool = False

    def parsing(self, content: str) -> Model or Generator[Model]:

        # TODO mapper如何加载?
        if not self.mapper_model:
            return
        model: Model = ModelManager.model(self.mapper_model._name)
        mapper: Dict[str, str] = model._mapper
        parsed_mapper: Dict[str, List[str]] = {}
        parsed_result: List[Model] = []
        length: int = 0

        for key, value in mapper.items():
            parsed = xpathParse(content, value)

            parsed_mapper[key] = parsed
            # if len(parsed) and parsed[0] is not 'None':
            #     length = len(parsed)
            length = length if len(parsed) <= length else len(parsed)

        for index in range(length):
            model: Model = ModelManager.model(self.mapper_model._name)
            for key in mapper:
                try:
                    setattr(model, key, parsed_mapper[key][index])
                except:
                    setattr(model, key, None)
            parsed_result.append(model)

        if self.auto_yield:
            for model in parsed_result:
                yield model
        else:
            self.context['mappers'] = parsed_result


class HiddenInputParse(Parse):
    target_tag: str = 'input'
    target_property: str = 'type'
    target_property_value: str = 'hidden'
    target_value: str = 'value'

    def parsing(self, content: str) -> Model or Generator[Model]:
        if content:
            values_xpath = '//{0}[@{1}="{2}"]/@{3}'.format(self.target_tag, self.target_property,
                                                           self.target_property_value, self.target_value)
            tags_xpath = '//{0}[@{1}="{2}"]/@name'.format(self.target_tag, self.target_property,
                                                          self.target_property_value)

            tags = xpathParse(content, tags_xpath)
            values = xpathParse(content, values_xpath)

            hidden_mapper: dict = {}

            # name 子集关系
            for index in range(len(values)):
                tag = tags[index]
                value = values[index]
                hidden_mapper[tag] = value
                # hidden_mapper[tags[index]] = values[index]

            # 存在
            if self.context.get('hidden'):
                for k, v in hidden_mapper.items():
                    self.context['hidden'][k] = v
            # 不存在
            else:
                self.context['hidden'] = hidden_mapper


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
    # property
    host: int
    port: int
    db_index: int

    # Duplicate property
    baseList: List[str]
    modelKey: str

    def __init__(self, settings: dict):
        super().__init__(settings)

        if not settings.get("duplication"):
            # TODO
            # 地址
            self.host: str = "127.0.0.1"
            self.port: int = 6379
            # 数据库索引
            self.db_index: int = 0

        if not self.modelKey:
            raise KeyError("Duplication must set model key")

        if self.baseList:
            self.set_base(self.baseList)
        else:
            if settings.get("target"):
                self.set_base([settings.get("target"), self.modelKey])
            else:
                self.set_base(["default", self.modelKey])

        # redis数据库
        self.db: redis.Redis = None

        # 链接
        self.connect()

    def connect(self):
        """
        重新连接
        :return:
        """
        # if not self.db:
        self.db = redis.Redis(host=self.host, port=self.port, db=self.db_index, decode_responses=True)
        try:
            self.db.keys("1")
        except redis.ConnectionError as e:
            print(e.args)
            raise TypeError('redis connect failed')

    def set_base(self, baseList: List):
        self.base = ":".join(baseList)

    def key(self, key: str) -> str:
        return ":".join([self.base, key])

    def process_item(self, model: Model) -> Any:
        key = getattr(model, self.modelKey)
        if self.check_identification(key):
            return model
        else:
            return False

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


class DumpProcessor(Processor):

    def start_task(self, settings: dict):
        self.data = []

    def start_process(self, number: int, model: str = "Model"):
        self.data.clear()

    def process_item(self, model: Model) -> Any:
        self.data.append(model.pure_data())

    def end_process(self):
        print('data len', len(self.data))


class Proxy_Processor(Processor):
    target = ProxyModel

    def start_process(self, number: int, model: str = "Model"):
        self.proxy_data: [] = jinglin(number)

    def process_item(self, model: ProxyModel) -> Any:
        proxy = self.proxy_data.pop().split(":")
        model.ip = proxy[0]
        model.port = proxy[1]
        return model
