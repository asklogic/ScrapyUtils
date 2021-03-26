# -*- coding: utf-8 -*-
"""Preload module to load python module in __init__ and preload function.

包含了Scheme包的各式加载函数，其主要存在于__init__.py中。
只需要import指定的包就可以自动加载各项设置、组件component和其他设置。

另外提供scheme_preload。

Todo:
    * 异常处理: Python加载异常（包含代码格式、缺少包）
"""
from importlib import import_module
from os import path
from typing import List, Type
from types import ModuleType

from ScrapyUtils.components import Component, Step, ActionStep, ParseStep, Processor

from ScrapyUtils import configure


def scheme_preload(scheme: str):
    try:
        module = import_module(scheme)

        global steps_class, processors_class

        steps_class = module.steps_class
        processors_class = module.processors_class
    except Exception as e:
        log.exception(e)
        raise Exception('Failed in scheme preload.')


def _load_components(module: ModuleType, component: type(Component)) -> List[Type[Component]]:
    components: List[Type[Component]] = list()
    for attr in dir(module):
        attribute = getattr(module, attr)
        # 短路判断
        if isinstance(attribute, type) and issubclass(attribute, component) and attribute is not component:
            components.append(attribute)
    return components


def collect_steps(*modules: ModuleType) -> List[Type[Step]]:
    """
    load scheme's steps
    """
    current_steps = list()
    for module in modules:
        current_steps.extend(_load_components(module, ActionStep))
        current_steps.extend(_load_components(module, ParseStep))

    # duplication steps
    current_steps = list(set(current_steps))

    # remove inactive steps
    current_steps = [x for x in current_steps if x.active]

    # sort by priority
    current_steps.sort(key=lambda x: x.priority, reverse=True)
    return current_steps


def collect_processors(module: ModuleType) -> List[Type[Processor]]:
    """
    load processors
    """
    current_processor = _load_components(module, Processor)

    # remove inactive processors
    current_processor = [x for x in current_processor if x.active]

    # sort by priority
    current_processor.sort(key=lambda x: x.priority, reverse=True)
    return current_processor


def initial_configure(settings_module: ModuleType):
    current_file_path = path.dirname(settings_module.__file__)

    configure.SCHEME_PATH = path.dirname(current_file_path)

    configure.DATA_FOLDER_PATH = path.join(configure.SCHEME_PATH, 'data')

    configure.DOWNLOAD_FOLDER_PATH = path.join(configure.SCHEME_PATH, 'download')

    for key in configure.registered_keys:
        if hasattr(settings_module, key):
            setattr(configure, key, getattr(settings_module, key))

    # tasks
    tasks_callable = getattr(settings_module, 'generate_tasks')
    assert callable(tasks_callable), "profile's generate_tasks must be callable."

    # scraper
    scraper_callable = getattr(settings_module, 'generate_scraper')
    assert callable(scraper_callable), "profile's generate_scraper must be callable."

    configure.tasks_callable = tasks_callable
    configure.scraper_callable = scraper_callable
