from abc import abstractmethod


class ComponentMeta(type):
    def __new__(mcs, name, bases, attrs: dict):
        attrs["_name"] = name

        if attrs.get("_active") is None:
            attrs["_active"] = True

        return type.__new__(mcs, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    _name: str

    @abstractmethod
    def check(self) -> bool:
        pass

    def get_name(self):
        return self._name

