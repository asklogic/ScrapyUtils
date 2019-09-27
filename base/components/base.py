from abc import abstractmethod


class ComponentMeta(type):
    def __new__(mcs, name, bases, attrs: dict):
        attrs["_name"] = name

        if attrs.get("_active") is None:
            attrs["_active"] = False

        return type.__new__(mcs, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    _name: str

    # @abstractmethod
    # def check(self) -> bool:
    #     pass

    @classmethod
    def get_name(self):
        return self._name

class Active(object):
    pass

def active(component_class: type(Component)):
    component_class._active = True
    return component_class
