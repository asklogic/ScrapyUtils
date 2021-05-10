# -*- coding: utf-8 -*-
"""The Component module including base type of a Component.

组件基本模块，包含了组件基类、组件管理器和相关的工具函数。

组件基类:

    一个组件至少需要两个通用方法：on_start和on_exit，分别在启动和退出的时候调用，用于初始化&回收组件资源。

    以及三个通用属性，组件名字、组件激活状态和优先级，分别用于区分组件、判断组件是否应该启动以及启动时的优先级。

Note:
    所有的组件都必须继承组件基类Component。

组件管理器:

    组件管理器是专门控制一系列组件的启动和停止的管理器，可以对同一批组件类进行统一的初始化和统一的启停。

工具函数 - 包含了两个工具函数：
    1. active装饰器 装饰于组件类使得组件状态为激活（active == True）。

    2. set_active组件激活函数 传入组件类使组件类状态为激活。


Todo:
    * 
"""

from abc import abstractmethod
from typing import List, Iterable, Type, Union, Optional, get_type_hints, get_args, get_origin

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


def method_checker(inner_check):
    annotations = get_type_hints(inner_check)

    # for key, value in annotations.items():
    #     get_args(value)
    #
    #     for item in get_args(value):
    #         get_args(item)
    #         get_origin(item)
    #     get_origin(value)
    #     pass
    def wrapper(*args, **kwargs):
        # Annotation number check.

        annotations_keys = annotations.keys()
        kwargs_keys = kwargs.keys()

        assert len(annotations_keys) + 1 == len(args) + len(kwargs_keys), 'Parameter need typing annotations.'

        parameters = {}

        # sorted key.
        for index, key in enumerate(annotations_keys):
            if key in kwargs_keys:
                parameters[key] = kwargs[key]
            else:
                parameters[key] = args[index + 1]

        _annotation_check(annotations, parameters)
        # _detect_type(annotations, parameters)

        return inner_check(*args, **kwargs)

    return wrapper


basic_type = [int, float, bool, str]

basic_collection = [list, tuple, set]


def _annotation_check(annotations: dict, parameters: dict):
    for key, value in annotations.items():
        _detect_type(value, parameters[key])
        pass


def _detect_type(target_type, actual_parameters):
    origin = get_origin(target_type)

    # basic
    if origin == None and target_type in basic_type:
        origin = target_type

        # assert
        assert isinstance(actual_parameters,
                          target_type), f'Except {target_type}, got {actual_parameters} at {type(actual_parameters)}.'
    elif origin in basic_collection:

        # assert

        assert isinstance(actual_parameters,
                          origin), f'Except {target_type}, got {actual_parameters} at {type(actual_parameters)}.'
        args = get_args(target_type)
        # args = target_type.__args__
        for param in actual_parameters:
            _detect_type(args[0], param)
    elif origin is dict:
        assert isinstance(actual_parameters,
                          origin), f'Except {target_type}, got {actual_parameters} at {type(actual_parameters)}.'

        args = get_args(target_type)

        for key, value in actual_parameters.items():
            assert isinstance(key, args[0])

            _detect_type(args[1], value)
    # case 3: custom type.
    elif origin is Union:
        args = get_args(target_type)

        assert type(actual_parameters) in args


    else:
        assert isinstance(actual_parameters,
                          target_type), f'Except {target_type}, got {actual_parameters} at {type(actual_parameters)}.'


# args = get_args(target_type)

# print(the_types)
# print(origin)

# if origin == list:
#     # _detect_type(get_args(origin_type)
#     for arg in the_types:
#         _detect_type(arg)
#
# elif origin == Union:
#     print('union', the_types)
#     pass


class Component(object, metaclass=ComponentMeta):
    """组件基类，继承自object，被元类ComponentMeta修改。

    所有的组件类都继承自此类，其提供了组件类需要的通用方法，自组建再自行定义其自己的方法。

    Note:
        不要动态修改Component已有的属性，此为组件类通用属性，需要通过工具函数来进行工作。

    Attributes:
        active (bool): Active state of a component. Default: False
        priority (int): Priority of a component. 
        name (str): Name of a component. Default: __class__.__name__

    """
    active: bool
    name: str
    priority: int = 500

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
    """The collection for series components.

    统一控制并且管理Component组件类的Suit类，可以统一对组件进行启停操作。

    Attributes:
        components (List[Component]): The list of components.

        Args:
            components (List[Union[Type[Component], Component]]): The components that will be added into suit.

    """
    components: List[Component] = None
    target_components: Type[Component] = Component

    def __init__(self, components: List[Union[Type[Component], Component]] = []):
        # initial components
        self.components = []

        for component in components:
            self.add_component(component)

    def add_component(self, component: Union[Type[Component], Component]) -> Optional[Component]:
        """Add a component instance or class into suit.

        向suit中添加一个组件实例或者组件类，如果是组件类将会无参数自动创建一个实例。

        返回True代表成功添加，返回False代表传入了错误的类型导致没有成功添加。

        Args:
            component (Union[Type[Component], Component]): The component instance/class.

        Returns:
            Optional[Component]: If success, return the component instance.
        """
        # case 1: A component instance.
        if isinstance(component, self.target_components):
            self.components.append(component)
            return component

        # case 2: A component class(type).
        elif isinstance(component, type) and issubclass(component, self.target_components):
            current = component()
            self.components.append(current)
            return current

        return None

    def suit_start(self):
        for index, component in enumerate(self.components):
            try:
                component.on_start()
            except Exception as e:
                component_log.error('Suit start component: {} failed.'.format(component.name), self.__class__.__name__)
                self.components.remove(component)

    def suit_exit(self):
        for index, component in enumerate(self.components):
            try:
                component.on_exit()
            except Exception as e:
                component_log.error('Suit exit component: {} failed.'.format(component.name), self.__class__.__name__)
                self.components.remove(component)


def active(component_class: type(Component)):
    component_class._active = True
    return component_class


def set_active(component_class: type(Component)):
    component_class._active = True
