# -*- coding: utf-8 -*-
"""The Component module including base type of a Component.

组件基本模块，包含了组件基类、组件管理器和相关的工具函数。

组件基类:

    一个组件至少需要两个通用方法：on_start和on_exit，分别在启动和退出的时候调用，用于初始化和回收组件资源。

    以及三个通用属性:

        1. 组件名字: 自动生成, 用于区分组件
        2. 组件激活状态: 默认为 False, 需要通过装饰器来开启.
        3. 优先级: 一般为0-1000的整数, 通过大小来控制启动组件启动的顺序。

Note:
    所有的组件都必须继承组件基类Component。


工具函数 - 包含了两个工具函数：

    1. active - 装饰器 装饰于组件类使得组件状态为激活（active == True）。

    2. set_active - 组件激活函数 传入组件类使组件类状态为激活。

"""

from abc import abstractmethod
from logging import getLogger
from typing import NoReturn, Type


class ComponentMeta(type):
    """Metaclass of Component to append some common properties.

    Property:

        1. 创建组件类时，添加active为False
        2. 添加name为类名
    """

    def __new__(mcs, name, bases, attrs: dict):
        if attrs.get("_active") is None:
            attrs["active"] = False
        attrs["name"] = name
        return type.__new__(mcs, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    """The base component

    所有的组件类都继承自此类，其提供了组件类需要的通用方法，各组件再自行定义其自己的方法。

    Note:
        不要动态修改Component已有的属性，此为组件类通用属性，需要通过工具函数来进行工作。

    """
    active: bool
    """bool: Active state of a component."""
    name: str
    """str: Component's name."""
    priority: int = 500
    """int: Priority of a component."""

    @abstractmethod
    def on_start(self) -> NoReturn:
        """The on_start method will invoke when component.suit start.
        """
        pass

    @abstractmethod
    def on_exit(self) -> NoReturn:
        """The on_exit method will invoke when component.suit start.
        """
        pass


def active(component_class: Type[Component]):
    """装饰器，将装饰的类的active置为True。"""
    component_class.active = True
    return component_class


def set_active(component_class: Type[Component]):
    """将装饰的组件类手动开启。

    Args:
        component_class (Type[Component]): 将要被开启的组件。
    """
    component_class.active = True


from .process import Process
from .action import Action

logger = getLogger('component')
