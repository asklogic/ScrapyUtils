from abc import abstractmethod
from typing import List, Iterable

from . import component_log

class ComponentMeta(type):

    def __init__(cls, *args, **kwargs):
        # TODO: init in type
        """
        Args:
            *args:
            **kwargs:
        """
        attr = args[2]
        cls._name = attr['_name']
        cls._active = attr['_active']

    @property
    def name(cls):
        return cls._name

    @property
    def active(cls):
        return cls._active

    def __new__(mcs, name, bases, attrs: dict):
        """
        Args:
            name:
            bases:
            attrs (dict):
        """
        attrs["_name"] = name

        if attrs.get("_active") is None:
            attrs["_active"] = False

        return type.__new__(mcs, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    _name: str
    _active: bool

    priority: int = 500

    @property
    def name(self):
        return self._name

    @property
    def active(self):
        return self._active

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass


class ComponentSuit(object):
    _components: List[type(Component)] = None
    target_components: type(Component) = Component

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
    """
    Args:
        component_class:
    """
    component_class._active = True
    return component_class


def set_active(component_class: type(Component)):
    """
    Args:
        component_class:
    """
    component_class._active = True
