# -*- coding: utf-8 -*-
"""The Component module including base type of a Component.

组件基本模块，包含了组件基类、组件管理器和相关的工具函数。

组件基类:

    一个组件至少需要两个通用方法：on_start和on_exit，分别在启动和退出的时候调用，用于初始化&回收组件资源。

    以及三个通用属性，组件名字、组件激活状态和优先级，分别用于区分组件、判断组件是否应该启动以及启动时的优先级。

组件管理器:

    组件管理器是专门控制一系列组件的启动和停止的管理器，可以对同一批组件类进行统一的初始化和统一的启停。

工具函数 - 包含了两个工具函数：
    1. active装饰器 装饰于组件类使得组件状态为激活（active == True）。

    2. set_active组件激活函数 传入组件类使组件类状态为激活。


Todo:
    * 
"""

from abc import abstractmethod
from typing import List, Iterable, Type

from . import component_log


class ComponentMeta(type):
    """组件元类

    创建组件类时，添加默认的active为False，添加默认的name为类名。

    """
    def __new__(mcs, name, bases, attrs: dict):
        if attrs.get("_active") is None:
            attrs["active"] = False
        attrs["name"] = name
        return type.__new__(mcs, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    """组件基类，继承自object，被元类ComponentMeta修改。

    所有的组件类都继承自此类，其提供了组件类需要的通用方法，自组建再自行定义其自己的方法。

        
    Attributes:
        priority (int): Priority of a component. 
    """
    name: str
    active: bool

    priority: int = 500

    # @property
    # def name(self) -> str:
    #     """The name of a component(class name).
    #
    #     Returns:
    #         str: A str content.
    #     """
    #     return self.__class__.name

    # @property
    # def active(self) -> bool:
    #     """The state of a component.
    #
    #     The active attributes in base on class.
    #
    #     Returns:
    #         bool: True is active, Flase is deactive.
    #     """
    #     return self._active

    @abstractmethod
    def on_start(self):
        """The on_start method will invoke when component/suit start.
        """
        pass

    @abstractmethod
    def on_exit(self):
        """The on_exit method will invoke when component/suit start.
        """
        pass



class ComponentSuit(object):
    _components: List[Component] = None
    target_components: Type[Component] = Component

    def __init__(self, components: List[type(Component)]):
        # assert

        assert isinstance(components, Iterable)
        for component in components:
            assert issubclass(component, self.target_components), f'Suit need type {self.target_components.name}.'

        # initial components
        self._components = []

        for component in components:
            current = component()
            self.components.append(current)

    @property
    def components(self):
        return self._components

    def suit_start(self):
        for component in self.components:
            try:
                component.on_start()
            except Exception as e:
                component_log.exception(e)
                component_log.error('component {} start failed.'.format(component.name), self.__class__.__name__)

                self.components.remove(component)
                # TODO: interrupt exception.
                raise Exception('interrupt.')

    def suit_exit(self):
        for component in self.components:
            try:
                component.on_exit()
            except Exception as e:
                component_log.exception(e)
                component_log.error('component {} exit failed.'.format(component.name), self.__class__.__name__)
                # TODO: interrupt exception.
                # raise Exception('interrupt.')


def active(component_class: type(Component)):
    component_class._active = True
    return component_class


def set_active(component_class: type(Component)):
    component_class._active = True
