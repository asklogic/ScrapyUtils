import json
import os
import time
from os import path as path
from typing import List, Dict, Generator, Any
from collections import deque

import csv
import redis
# import peewee
from urllib.parse import ParseResult, urlparse

from base.libs import Model, Field
from base.components.proceesor import Processor
from base.libs.scraper import Scraper
from base.libs.task import TaskModel
from base.components.scheme import Action, Parse
from base.libs.task import Task
from base.tool import xpathParse
from base.core import core

from base.log import common as log


class DownloadModel(Model):
    page_name = Field()
    page_content = Field()


class DefaultAction(Action):
    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get(url=task.url)


class FileProcessorMixin(Processor):
    file_folder: str = None
    file_name: str = None

    file_path: str = None

    file_suffix: str = '.data'

    def __init__(self, config: dict = None):
        super().__init__(config)

        # file's folder.
        # default : /<scheme>/data
        if not (hasattr(self, 'file_folder') and self.file_folder):
            self.file_folder = config.get('file_folder', self.config.get('file_folder'))

        # file's name.
        # default : timestamp
        if not (hasattr(self, 'file_name') and self.file_name):
            self.file_name = config.get('file_name', str(int(time.time())))

        # fixed path.
        if not (hasattr(self, 'file_path') and self.file_path):
            self.file_path = os.path.join(self.file_folder, self.file_name)

        # add suffix
        if not (self.file_suffix in self.file_path):
            self.file_path = self.file_path + self.file_suffix

        self.data = deque()

        log.info('folder: {}'.format(self.file_folder), self.name)
        log.info('file name: {}'.format(self.file_name), self.name)
        log.info('path: {}'.format(self.file_path), self.name)

    def on_start(self):
        temp_path = os.path.join(self.file_folder, 'touch')
        with open(temp_path, 'w') as f:
            pass
        os.remove(temp_path)

        # log.info('folder: {}'.format(self.file_folder), self.name)
        # log.info('file name: {}'.format(self.file_name), self.name)
        # log.info('path: {}'.format(self.file_path), self.name)

    def process_item(self, model: Model) -> Any:
        self.data.append(model.pure_data)


class JsonFileProcessor(FileProcessorMixin, Processor):
    file_suffix = '.json'

    def on_exit(self):
        with open(self.file_path, 'w') as f:
            json.dump(list(self.data), f)


class CSVFileProcessor(FileProcessorMixin, Processor):
    file_suffix = '.csv'

    def on_exit(self):
        with open(self.file_path, 'w', encoding='utf-8', newline='' "") as f:
            writer = csv.writer(f)

            writer.writerow(list(self.data[0].keys()))
            for i in self.data:
                writer.writerow(list(i.values()))


class XpathMappingParse(Parse):
    models: List[type(Model)] = []
    full: bool = False
    autoyield: bool = True

    def check(self) -> bool:
        for model in self.models:
            assert issubclass(model, Model)

        return True

    def parsing(self, content: str) -> Model or Generator[Model]:

        for model in self.models:
            if not model._mapper:
                continue

            parsed_mapper: Dict[str, List[str] or str] = {}
            parsed_result: List[Model] = []
            length = 1

            for key, value in model._mapper.items():
                # 常量get_name
                if value.startswith("const:"):
                    parsed_mapper[key] = value[6:]
                # 从Task中获取的context
                elif value.startswith("context:"):
                    parsed_mapper[key] = self.context[value[8:]]
                # 固定值
                elif value.startswith("fixed:"):
                    parsed_mapper[key] = xpathParse(content, value[6:])[0]
                # 动态值
                else:
                    parsed = xpathParse(content, value)
                    parsed_mapper[key] = parsed

                    if len(parsed) > length:
                        length = len(parsed)
                    # length = length if len(parsed) <= length else len(parsed)

            # 根据长度来生成model
            for index in range(length):
                data_model: type(Model) = data_model()
                for key, item in model._mapper.items():
                    try:
                        # 解析为列表
                        if type(parsed_mapper[key]) is list:
                            value = parsed_mapper[key][index]

                            if self.full and not bool(value):
                                value = "#"
                            setattr(data_model, key, value)
                        # 固定值
                        else:
                            if self.full and not parsed_mapper[key]:
                                setattr(data_model, key, "#")
                            else:
                                setattr(data_model, key, parsed_mapper[key])
                    except (KeyError, IndexError) as e:
                        # 不存在key 设置为-
                        setattr(data_model, key, '-')

                parsed_result.append(data_model)

            if self.autoyield:
                for parsed_model in parsed_result:
                    yield parsed_model
            else:
                self.context['mappers.' + model.get_name()] = parsed_result


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
            # xpathParse(content, '//input[@type="hidden" and [@name"{0}"]/@value')
            hidden_mapper: dict = {}

            # 对应

            for tag in tags:
                values_xpath = '//{0}[@{1}="{2}" and @name="{4}"]/@{3}'.format(self.target_tag, self.target_property,
                                                                               self.target_property_value,
                                                                               self.target_value, tag)
                value = xpathParse(content, values_xpath)
                if value:
                    hidden_mapper[tag] = value[0]
            # name 子集关系
            # for index in range(len(values)):
            #     tag = tags[index]
            #     value = values[index]
            #     hidden_mapper[tag] = value
            # hidden_mapper[tags[index]] = values[index]

            # 存在
            if self.context.get('hidden'):
                if False:
                    pass
                else:
                    for k, v in hidden_mapper.items():
                        self.context['hidden'][k] = v
            # 不存在
            else:
                self.context['hidden'] = hidden_mapper


class DuplicateProcessor():
    pass


# class JsonFileProcessor(Processor):
#
#     def __init__(self, settings: dict):
#         super().__init__(settings)
#
#         # TODO
#         # 文件分卷
#         self.part: int = 0
#         # 单个文件元素限制
#         self.limit: int = 5000
#         # 文件名字
#         self.name: str = self.__class__.__name__
#         # 文件路径
#
#         # data
#         self.data: List[Model] = []
#         self.mark = str(int(time.time()))[-4:]
#
#         if settings.get("JsonFile"):
#             json_setting = settings.get("JsonFile")
#             if json_setting.get("mark"):
#                 self.mark = str(json_setting.get("mark"))
#
#         if settings.get("job"):
#             self.dir_path = path.join(Project_Path, settings.get("job"), "data")
#         else:
#             self.dir_path = path.join(Project_Path, "assets")
#
#         self.detect_save()
#         self.detect_exist_file()
#
#     def detect_exist_file(self):
#
#         while os.path.exists(path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(0), ".json"]))) \
#                 and \
#                 os.path.exists(
#                     path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(self.part + 1), ".json"]))):
#             self.part = self.part + 1
#
#         file_path = path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(self.part), ".json"]))
#         if os.path.exists(file_path):
#             with open(file_path) as f:
#                 data = json.load(f)
#             self.data.extend(data)
#             logger.info("<<JsonFile>> load exist data. exist file: " + file_path)
#
#     def detect_save(self):
#         temp_file = path.join(self.dir_path, self.name + "JsonFileTest.json")
#         logger.info("<<JsonFile>> Json File path: " + path.join(self.dir_path))
#         try:
#             if not os.path.exists(self.dir_path):
#                 os.mkdir(self.dir_path)
#
#             with open(temp_file, "w") as f:
#                 json.dump([], f)
#             os.remove(temp_file)
#         except Exception as e:
#             print(e.args)
#             raise TypeError('<<JsonFile>> cannot dump json file!')
#
#     def save_model(self, model: Model):
#         self.data.append(model.pure_data())
#         return True
#
#     def dump_to_file(self):
#         file_path = path.join(self.dir_path, "".join([self.name, self.mark, "-part" + str(self.part), ".json"]))
#         with open(file_path, "w") as f:
#             json.dump(self.data[:self.limit], f)
#             logger.info("<<JsonFile>> success dump file. " + file_path)
#         self.part += 1
#         self.data = self.data[self.limit:]
#
#     def end_process(self):
#         while len(self.data) >= self.limit:
#             self.dump_to_file()
#
#     def on_exit(self):
#         logger.info("<<JsonFile>> end task! last len:" + str(len(self.data)))
#         if self.data:
#             self.dump_to_file()
#
#     def process_item(self, model: Model) -> Model:
#         self.data.append(model.pure_data())
#         return model


# class DumpProcessor(Processor):
#
#     def on_start(self, settings: dict):
#         self.data = []
#
#     def start_process(self, number: int, model: str = "Model"):
#         self.data.clear()
#
#     def process_item(self, model: Model) -> Any:
#         self.data.append(model.pure_data())
#
#     def end_process(self):
#         print('data len', len(self.data))


# class DumpInPeeweeProcessor(Processor):
#     table: peewee.Model = None
#
#     def on_start(self, setting: Setting):
#         assert bool(self.table)
#
#     def process_item(self, model: Model) -> Any:
#         self.data.append(model.pure_data())
#         return model
#
#     def end_process(self):
#         if self.data:
#             self.table.insert(self.data).execute()
#         self.data.clear()


# class ProxyProcessor(Processor):
#     query_param: Dict = {}
#
#     query_parsed: ParseResult
#     query_number_key = ''
#
#     _headers = {
#         'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
#         "Content-Type": "application/x-www-form-urlencoded",
#         'Connection': 'close',
#         'Cache-Control': 'max-age=0',
#     }
#
#     def on_start(self, setting: Setting):
#         if not setting.ProxyFunc and setting.ProxyURL == '':
#             raise Exception("didn't set proxy info. check setting")
#
#         if setting.ProxyURL:
#             self.query_parsed = urlparse(setting.ProxyURL)
#
#             for item in parse_qsl(self.query_parsed.query):
#                 self.query_param[item[0]] = item[1]
#
#         if setting.ProxyNumberParam:
#             self.query_number_key = setting.ProxyNumberParam
#         else:
#             self.query_number_key = 'qty'
#
#         if setting.ProxyFunc:
#             self.proxy_get = setting.ProxyFunc
#
#     def proxy_get(self, number: int):
#
#         self.query_param[self.query_number_key] = number
#         result = list(tuple(self.query_parsed))
#         result[4] = urlencode(self.query_param)
#
#         url = urlunparse(tuple(result))
#
#         res = requests.get(url, headers=self._headers)
#
#         assert res.status_code >= 200 and res.status_code < 300
#
#         proxy_list = res.content.decode("utf-8").split("\r\n")
#
#         for proxy in proxy_list:
#             assert ':' in proxy
#
#         self.proxy_list = proxy_list
#
#     def start_process(self, number: int, model: str = "Model"):
#
#         self.proxy_get(number)
#
#         print('proxy success')
#
#     def process_item(self, model: Model) -> Any:
#         proxy = self.proxy_list.pop().split(":")
#         model.ip = proxy[0]
#         model.port = proxy[1]
#         return model


class DumpInPeeweeProcessor():
    pass


# class DuplicateProcessor(Processor):
#     # property
#     host: int = '127.0.0.1'
#     port: int = '6379'
#     db: int = 0
#     password: str = ''
#
#     redis_connect: redis.Redis = None
#
#     # Duplicate property
#     baseList: List[str] = []
#     modelKey: str = ''
#
#     def on_start(self, setting: Setting):
#         assert bool(self.modelKey)
#
#         duplication_setting = setting.Duplication
#
#         for key, value in duplication_setting.items():
#             setattr(self, key, value)
#
#         if self.baseList:
#             self._set_base(self.baseList)
#         else:
#             self._set_base(baseList=[setting.Target, self.modelKey])
#
#         self.connect()
#
#     def connect(self):
#         self.redis_connect = redis.Redis(host=self.host, port=self.port, db=self.db,
#                                          password=self.password, decode_responses=True,
#                                          socket_connect_timeout=3)
#         try:
#             self.redis_connect.keys('1')
#         except redis.ConnectionError as e:
#             print(e.args)
#             raise TypeError('redis connect failed')
#
#     def _set_base(self, baseList: List):
#         self.base = ":".join(baseList)
#
#     def _key(self, key: str) -> str:
#         return ":".join([self.base, key])
#
#     def process_item(self, model: Model) -> Any:
#         key = getattr(model, self.modelKey)
#         if key and self.check_identification(key):
#             return model
#         else:
#             return False
#
#     def exist_identification(self, key_name) -> bool:
#         """
#         存在key 返回True
#         不存在key 返回False
#         :param key_name:
#         :return:
#         """
#         return self.redis_connect.exists(self._key(key_name))
#
#     def save_identification(self, key_name):
#         """
#         保存
#         :param key_name:
#         :return:
#         """
#         self.redis_connect.set(self._key(key_name), 1)
#
#     def check_identification(self, key):
#         """
#         查询并且保存
#         存在 返回False
#         不存在 返回True
#         :param key:
#         :return:
#         """
#         if self.exist_identification(key):
#             return False
#         else:
#             self.save_identification(key)
#             return True


class ProxyModel(Model):
    ip = Field()
    port = Field()
