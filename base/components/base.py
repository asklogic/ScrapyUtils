

class ComponentMeta(type):
    def __new__(mcs, name, bases, attrs: dict):
        attrs["_name"] = name

        if not attrs.get("_active"):
            attrs["_active"] = False

        return type.__new__(mcs, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    pass