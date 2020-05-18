from abc import abstractmethod
from typing import List, Iterable

from . import log


class ComponentMeta(type):

    def __init__(cls, *args, **kwargs):
        # TODO: init in type
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
        attrs["_name"] = name

        if attrs.get("_active") is None:
            attrs["_active"] = False

        return type.__new__(mcs, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    _name: str
    _active: bool

    priority: int = 500

    @property
    def name(cls):
        return cls._name

    @property
    def active(cls):
        return cls._active

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass


class ComponentSuit(object):
    _components: List[Component] = None
    target_components: type(Component) = Component

    config: dict = None

    def __init__(self, components: List[type(Component)], config: dict = None):
        assert isinstance(components, Iterable)
        for component in components:
            # assert isinstance(processor, Processor), 'Processor must be init'
            assert issubclass(component, self.target_components), 'Suit need type {}.'.format(
                self.target_components.name)

        self.config = config if config else {}
        self._components = []

        # TODO: two for-loop
        for component in components:
            try:
                current = component(config)
                self._components.append(current)
            except Exception as e:
                log.exception(self.__class__.__name__, e)
                log.error('Component {} initial failed.'.format(component.name), self.__class__.__name__)
                # TODO: raise exception?

    @property
    def components(self):
        return self._components

    def suit_start(self):
        for component in self.components:
            try:
                component.on_start()
            except Exception as e:
                log.exception(self.__class__.__name__, e)
                log.error('component {} start failed.'.format(component.name), self.__class__.__name__)
                # TODO: interrupt exception.
                raise Exception('interrupt.')

    def suit_exit(self):
        for component in self.components:
            try:
                component.on_exit()
            except Exception as e:
                log.exception(self.__class__.__name__, e)
                log.error('component {} exit failed.'.format(component.name), self.__class__.__name__)
                # TODO: interrupt exception.
                # raise Exception('interrupt.')


def active(component_class: type(Component)):
    component_class._active = True
    return component_class
