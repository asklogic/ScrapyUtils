# -*- coding: utf-8 -*-
"""Preload module to load components and other configuration from a python module.

启动爬虫流程的第零步：预加载 - Preload。

预加载模块，全部由工具函数组成，用于一个爬虫Python包的__init__.py中。

由于单独的爬虫项目是以一个符合项目规范的Python包的形式呈现，爬虫核心程序只需要import该Python包即可加载需要的爬虫项目。
因此将一个爬虫项目中的各项依赖包全部放置于__init__.py中，同时将一些需要预先执行的流程，诸如开启某个组件、加载项目配置等操作放置一并放入其中。

在执行爬虫项目时，因为基于Python特性，import此该爬虫项目时就会自动执行__init__.py中的流程，不需要在爬虫核心中执行额外步骤，
所以将这类函数归于预加载模块。

工具函数:

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
from os import path
from typing import List, Type, NoReturn
from types import ModuleType

from ScrapyUtils.components import Component, Action
from ScrapyUtils.components.processor import Processor

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
        # 短路判断
        # case 1: attr is type.
        # case 2: attr is subclass.
        # case 3: attr is not the type.
        if isinstance(attribute, type) and issubclass(attribute, component_type) and attribute is not component_type:
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
    """Collect Processor"""
    _collect_base(module, config_name='processor_classes', collect_type=Processor)


def initial_configure(settings_module: ModuleType) -> NoReturn:
    configure.SCHEME_PATH = path.dirname(settings_module.__file__)

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
