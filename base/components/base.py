from abc import abstractmethod


class ComponentMeta(type):

    def __init__(cls, *args, **kwargs):
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


def active(component_class: type(Component)):
    component_class._active = True
    return component_class
