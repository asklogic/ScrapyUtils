# -*- coding: utf-8 -*-
"""Preload module to load components and other configuration from a python module.

包含了加载一个Scheme包的各式加载函数，其主要存在于一个项目的__init__.py文件中。

只需要import指定的包就可以自动加载各项设置、组件components和其他函数到全局变量中，以用于各类初始化函数中。


函数:

    1. _load_components::

        从一个Python module中加载指定类型的Components，返回指定类型的类对象列表。

    2. collect_steps::

        基于_load_components函数，从多个module中加载Step组件类。

    3. collect_processors::

        基于_load_components函数，从多个module中加载Processor组件

    4. initial_configure::

        加载一个项目中setting.py的各项属性。

Todo:
    * 异常处理: Python加载异常（包含代码格式、缺少包）
"""
from importlib import import_module
from os import path
from typing import List, Type, NoReturn
from types import ModuleType

from ScrapyUtils.components import Component, Step, ActionStep, ParseStep, Processor

from ScrapyUtils import configure

from logging import getLogger

logger = getLogger(__name__)


def _load_components(module: ModuleType, component_type: Type[Component] = Component) -> List[Type[Component]]:
    """Load Components from a python module.

    Args:
        module (ModuleType): The target python module.
        component_type (Type[Component], optional): The type of component that function will load. Defaults to Component.

    Returns:
        List[Type[Component]]: The list of component classes.
    """
    components: List[Type[Component]] = list()

    for attr in dir(module):
        attribute = getattr(module, attr)
        # 短路判断
        # case 1: attr is type.
        # case 2: attr is subclass.
        # case 3: attr is not the type.
        if isinstance(attribute, type) and issubclass(attribute, component_type) and attribute is not component_type:
            components.append(attribute)
    return components


def collect_steps(*modules: ModuleType) -> List[Type[Step]]:
    """Load Step classes from some python modules.

    Returns:
        List[Type[Step]]: The list of Step classes.
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
    """Load Processor classes from some python modules.

    Returns:
        List[Type[Processor]]: The list of Processor classes.
    """
    current_processor = _load_components(module, Processor)

    # remove inactive processors
    current_processor = [x for x in current_processor if x.active]

    # sort by priority
    current_processor.sort(key=lambda x: x.priority, reverse=True)
    return current_processor


def initial_configure(settings_module: ModuleType) -> NoReturn:
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
