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

组件管理器:

    组件管理器是专门控制一系列组件的启动和停止的管理器，可以对同一批组件类进行统一的初始化和统一的启停。

工具函数 - 包含了两个工具函数：

    1. active - 装饰器 装饰于组件类使得组件状态为激活（active == True）。

    2. set_active - 组件激活函数 传入组件类使组件类状态为激活。

"""

from abc import abstractmethod
from typing import List, Iterable, Type, Union, Optional, Sequence
from logging import getLogger

_logger = getLogger('component')


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
    def on_start(self):
        """The on_start method will invoke when component.suit start.
        """
        pass

    @abstractmethod
    def on_exit(self):
        """The on_exit method will invoke when component.suit start.
        """
        pass


class ComponentSuit(object):
    """The collection for series components.

    统一控制并且管理Component组件类的Suit类，可以统一对组件进行启停操作。

    """
    components: List[Component] = None
    """List[Component]: The component instances of this suit."""
    target_components: Type[Component] = Component
    """Type[Component]: The expect type of component"""

    def __init__(self, components: Sequence[Component] = None):
        """Append all the components when it initial."""
        self.components = []
        components = components if components else []

        for component in components:
            self.add_component(component)
        self.components.sort(key=lambda x: x.priority, reverse=True)

    def add_component(self, component: Component) -> Optional[Component]:
        """Add a component instance or class into suit.

        向suit中添加一个组件对象。

        返回对象本身代表成功添加，返回None代表传入了错误的类型导致没有成功添加。

        Args:
            component (Union[Type[Component], Component]): The component instance.

        Returns:
            Optional[Component]: If success, return the component instance.
        """
        if isinstance(component, self.target_components):
            self.components.append(component)
            self.components.sort(key=lambda x: x.priority, reverse=True)
            return component

    def suit_start(self) -> List[Component]:
        """Start all the components.

        Suit类统一调用其组件的on_start方法，如果某个子组件on_start方法报错则会移除该组件。

        Returns:
            List[Component]: 抛出错误的组件
        """
        error_components = []
        for index, component in enumerate(self.components):
            try:
                component.on_start()
            except Exception as e:
                _logger.error(f'Suit start component: {component.name} failed.')
                self.components.remove(component)
                error_components.append(component)

        return error_components

    def suit_exit(self) -> List[Component]:
        """Suit exit all the components.

        Suit类统一调用其组件的on_exit方法，如果某个子组件on_exit方法报错则会移除该组件。

        Returns:
            List[Component]: 抛出错误的组件
        """
        error_components = []
        for index, component in enumerate(self.components):
            try:
                component.on_exit()
            except Exception as e:
                _logger.error(f'Suit exit component: {component.name} failed.')
                self.components.remove(component)
                error_components.append(component)
        return error_components


def active(component_class: Type[Component]):
    """active装饰器，将装饰的类的active置为True。"""
    component_class.active = True
    return component_class


def set_active(component_class: Type[Component]):
    """单独的激活函数，将组件类手动开启。

    Args:
        component_class (Type[Component]): 将要被开启的组件。
    """
    component_class.active = True
