# -*- coding: utf-8 -*-
"""Preload module to load components and other configuration from a python module.

启动爬虫流程的第零步：预加载 - Preload。

预加载模块，随着自动生成工具自动生成在一个爬虫Python项目的__init__.py文件中，不需要额外的调用。

由于单独的爬虫项目是以一个符合项目规范的Python包的形式呈现，爬虫核心程序只需要引入该Python包即可加载需要的爬虫项目。
因此将一个爬虫项目中的各项依赖包全部放置于__init__.py中，同时将一些需要预先执行的流程，
诸如开启某个组件、加载项目配置等操作放置一并放入其中，由于框架组件全部由全局变量控制，因此不需要做额外的操作。

在执行爬虫项目时，因为基于Python特性，import此该爬虫项目时就会自动执行__init__.py中的流程，不需要在爬虫核心中执行额外步骤，
因此将这类函数归于预加载模块。

执行流程::

    0. import 引入
    1. 调用collect_steps和collect_processors，加载组件类
    2. 调用initial_configure，加载设置

可能出现的异常:

    1. Python文件格式异常导致无法引入

工具函数:

    1. collect_steps:
        基于_load_components函数，从多个module中加载Step组件类。

    2. collect_processors:
        基于_load_components函数，从多个module中加载Processor组件类。

    3. initial_configure:
        加载一个项目中的setting.py的各项设置。

Todo:
    * 异常处理: Python加载异常（包含代码格式、缺少包）
"""
from os import path
from typing import List, Type, NoReturn
from types import ModuleType

from ScrapyUtils.components import Component, Action, Process, ComponentMeta

from ScrapyUtils import configure

from logging import getLogger

logger = getLogger('preload')


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
        if type(attribute) == ComponentMeta and issubclass(attribute, component_type):
            components.append(attribute)
    return components


def _collect_base(*modules: ModuleType, config_name: str, collect_type: Type[Component]) -> NoReturn:
    """The common function for collect component.

    Load the target components from a module the save them in module configure.
    """
    target_components = []
    for module in modules:
        target_components.extend(_load_components(module, collect_type))

    # filter deactivated components
    activated_components = [x for x in target_components if x.active]

    setattr(configure, config_name, activated_components)


# The collect functions:
def collect_action(*modules: ModuleType) -> NoReturn:
    """Collect Action"""
    _collect_base(*modules, config_name='action_classes', collect_type=Action)


def collect_processors(module: ModuleType) -> NoReturn:
    """Collect Process"""
    _collect_base(module, config_name='process_classes', collect_type=Process)


def initial_configure(settings_module: ModuleType) -> NoReturn:
    configure.PROJECT_PATH = path.dirname(settings_module.__file__)

    configure.DATA_FOLDER_PATH = path.join(configure.PROJECT_PATH, 'data')

    configure.DOWNLOAD_FOLDER_PATH = path.join(configure.PROJECT_PATH, 'download')

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
