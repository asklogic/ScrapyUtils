import json
import os
import time
from logging import getLogger
from typing import List, Dict, Generator, Any
from collections import deque

import csv
import openpyxl

from ScrapyUtils import configure
from ScrapyUtils.libs import Model, Field, Task, Scraper
from ScrapyUtils.components.process import Process
from ScrapyUtils.components import Action
from ScrapyUtils.tool import XpathParser

logger = getLogger('common')


class FileProcessMixin(Process):
    file_folder: str = None
    """str: 文件存放地址 == DataFolder"""
    file_name: str = None
    """str: 文件名字"""
    file_path: str = None
    """str: 文件绝对路径"""

    file_suffix: str = '.data'
    """str: 文件后缀名"""

    def __init__(self):
        # File's folder.
        # Default : /<project>/data
        # Keep blank str will save into the work folder.
        if not (hasattr(self, 'file_folder') and self.file_folder != None):
            self.file_folder = configure.DATA_FOLDER_PATH

        # File's name.
        # Default : timestamp
        if not (hasattr(self, 'file_name') and self.file_name):
            self.file_name = str(int(time.time()))

        # Fixed file path.
        # Default : /project/data
        if not (hasattr(self, 'file_path') and self.file_path):
            self.file_path = os.path.join(self.file_folder, self.file_name)

        # add suffix in the file path
        if not (self.file_suffix in self.file_path):
            self.file_path = self.file_path + self.file_suffix

        self.data = deque()

    def on_start(self):
        """尝试创建"""
        temp_path = os.path.join(self.file_folder, 'touch')
        with open(temp_path, 'w') as f:
            pass
        os.remove(temp_path)

        logger.info(f'{self.__class__.__name__} create file: {self.file_path}')

    def process_item(self, model: Model) -> Any:
        self.data.append(model.pure_data)


class JsonFileProcess(FileProcessMixin, Process):
    file_suffix = '.json'

    def on_exit(self):
        with open(self.file_path, 'w') as f:
            json.dump(list(self.data), f)
        logger.info(f'JSON file saved as: {self.file_path}')


class CSVFileProcess(FileProcessMixin, Process):
    file_suffix = '.csv'

    def on_exit(self):
        with open(self.file_path, 'w', encoding='utf-8', newline='' "") as f:
            writer = csv.writer(f)

            writer.writerow(list(self.data[0].keys()))
            for i in self.data:
                writer.writerow(list(i.values()))

        logger.info(f'CSV file saved as: {self.file_path}')


class ExeclFileProcess(FileProcessMixin, Process):
    file_suffix = '.xlsx'

    def on_start(self):
        super().on_start()

        wb = openpyxl.Workbook()
        ws = wb.active

        self.wb = wb
        self.ws = ws

        self.need_head = True

    def process_item(self, model: Model) -> Any:
        if self.need_head:
            self.need_head = False
            self.ws.append(list(model.pure_data.keys()))

        try:
            self.ws.append(list(model.pure_data.values()))
        except Exception as e:
            # TODO: add callback
            logger.error('insert row failed', 'Execl')

    def on_exit(self):
        self.wb.save(self.file_path)
        logger.info(f'Execl file saved as: {self.file_path}')


# TODO: 自动生成Parser -> 不如手动填
# class XpathMappingParse(Action):
#     """根据创建Model时绑定的Xpath来自动生成Parser"""
#     models: List[type(Model)] = []
#     full: bool = False
#     autoyield: bool = True
#
#     def check(self) -> bool:
#         for model in self.models:
#             assert issubclass(model, Model)
#
#         return True
#
#     def parsing(self, content: str) -> Model or Generator[Model]:
#         for model in self.models:
#             if not model._mapper:
#                 continue
#
#             parsed_mapper: Dict[str, List[str] or str] = {}
#             parsed_result: List[Model] = []
#             length = 1
#
#             for key, value in model._mapper.items():
#                 # 常量get_name
#                 if value.startswith("const:"):
#                     parsed_mapper[key] = value[6:]
#                 # 从Task中获取的context
#                 elif value.startswith("context:"):
#                     parsed_mapper[key] = self.context[value[8:]]
#                 # 固定值
#                 elif value.startswith("fixed:"):
#                     parsed_mapper[key] = XpathParser(content, value[6:])[0]
#                 # 动态值
#                 else:
#                     parsed = XpathParser(content, value)
#                     parsed_mapper[key] = parsed
#
#                     if len(parsed) > length:
#                         length = len(parsed)
#                     # length = length if len(parsed) <= length else len(parsed)
#
#             # 根据长度来生成model
#             for index in range(length):
#                 data_model: type(Model) = data_model()
#                 for key, item in model._mapper.items():
#                     try:
#                         # 解析为列表
#                         if type(parsed_mapper[key]) is list:
#                             value = parsed_mapper[key][index]
#
#                             if self.full and not bool(value):
#                                 value = "#"
#                             setattr(data_model, key, value)
#                         # 固定值
#                         else:
#                             if self.full and not parsed_mapper[key]:
#                                 setattr(data_model, key, "#")
#                             else:
#                                 setattr(data_model, key, parsed_mapper[key])
#                     except (KeyError, IndexError) as e:
#                         # 不存在key 设置为-
#                         setattr(data_model, key, '-')
#
#                 parsed_result.append(data_model)
#
#             if self.autoyield:
#                 for parsed_model in parsed_result:
#                     yield parsed_model
#             else:
#                 self.context['mappers.' + model.get_name()] = parsed_result


# TODO: 隐藏表单自动填充 -> 不如手动填
# class HiddenInputParse(Action):
#     target_tag: str = 'input'
#     target_property: str = 'type'
#     target_property_value: str = 'hidden'
#     target_value: str = 'value'
#
#     def parsing(self, content: str) -> Model or Generator[Model]:
#         if content:
#             values_xpath = '//{0}[@{1}="{2}"]/@{3}'.format(self.target_tag, self.target_property,
#                                                            self.target_property_value, self.target_value)
#             tags_xpath = '//{0}[@{1}="{2}"]/@name'.format(self.target_tag, self.target_property,
#                                                           self.target_property_value)
#
#             tags = XpathParser(content, tags_xpath)
#             values = XpathParser(content, values_xpath)
#             # XpathParser(content, '//input[@type="hidden" and [@name"{0}"]/@value')
#             hidden_mapper: dict = {}
#
#             # 对应
#
#             for tag in tags:
#                 values_xpath = '//{0}[@{1}="{2}" and @name="{4}"]/@{3}'.format(self.target_tag, self.target_property,
#                                                                                self.target_property_value,
#                                                                                self.target_value, tag)
#                 value = XpathParser(content, values_xpath)
#                 if value:
#                     hidden_mapper[tag] = value[0]
#             # name 子集关系
#             # for index in range(len(values)):
#             #     tag = tags[index]
#             #     value = values[index]
#             #     hidden_mapper[tag] = value
#             # hidden_mapper[tags[index]] = values[index]
#
#             # 存在
#             if self.context.get('hidden'):
#                 if False:
#                     pass
#                 else:
#                     for k, v in hidden_mapper.items():
#                         self.context['hidden'][k] = v
#             # 不存在
#             else:
#                 self.context['hidden'] = hidden_mapper
