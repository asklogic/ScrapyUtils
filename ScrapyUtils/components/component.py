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
from typing import List, Iterable, Type, Union, get_type_hints, get_args, get_origin

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
        priority (int): Priority of a component. 
        name (str): Name of a component. Default: __class__.__name__
        active (bool): Active state of a component. Default: False

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
    """[summary]

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """
    _components: List[Component] = None
    target_components: Type[Component] = Component

    def __init__(self, components: List[Union[Type[Component], Component]]):

        self._components = []
        # initial components
        self.components = components

        # for component in components:
        #     current = component()
        #     self.components.append(current)

    @property
    def components(self):
        return self._components

    @components.setter
    def components(self, components: List[Union[Type[Component], Component]]):
        for component in components:
            # case 1: A component instance.
            if isinstance(component, Component):
                self._components.append(component)

            # case 2: A component class(type).

            elif isinstance(component, type) and issubclass(component, Component):
                current = component()
                self._components.append(current)

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
