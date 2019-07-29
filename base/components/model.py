from typing import Dict, Any


class Field(object):
    xpath: str = ""

    def __init__(self, xpath: str = None):
        self.xpath = xpath


class ModelMeta(type):
    def __new__(cls, name, bases, attrs: dict):

        # mapper
        if attrs.get('_mapper') and type(attrs.get('_mapper')) == dict:
            mapper = attrs.get('_mapper')
        else:
            mapper = {}
        data = {}

        # TODO 属性保留
        for k, v in list(attrs.items()):
            if isinstance(v, Field):
                if v.xpath:
                    mapper[k] = v.xpath
                data[k] = None
                attrs.pop(k)
                continue
            # if k not in ["full", "pure_data", "__setattr__", "__getattr__", "__delattr__"]:
            #     attrs.pop(k)
        # 清空Model其他属性 保留自带的属性
        # 使字段通过getattr来获取
        attrs["_data"] = data
        attrs["_name"] = name
        attrs["_mapper"] = mapper

        if attrs.get("_active") is None:
            attrs["_active"] = True

        return type.__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs: dict) -> None:
        super().__init__(self)


class Model(object, metaclass=ModelMeta):
    _active: bool
    _data: Dict[str, object] = {}
    _mapper: Dict[str, str]
    _name: str

    def __new__(cls) -> Any:
        return super().__new__(cls)

    def __init__(self) -> None:
        object.__setattr__(self, "_data", self.__class__._data.copy())

    def __setattr__(self, key, value):
        if key in self._data.keys():
            self._data[key] = value
        else:
            raise KeyError("Model {0} has no Field named {1}".format(self._name, key))

    def __getattr__(self, item):
        if item in self._data.keys():
            return self._data[item]
        else:
            raise KeyError("Model {0} has no Field named {1}".format(self._name, item))

    def __delattr__(self, item):
        self._data.pop(item)

    def full(self):
        for k, v in self._data.items():
            if v is None:
                return False
        return True

    def pure_data(self):
        return self._data

    @classmethod
    def get_name(cls):
        return cls._name


# ModelManager


class ManagerMeta(type):

    def __new__(cls, name, bases, attrs):
        attrs["registered"] = {}
        return type.__new__(cls, name, bases, attrs)


class ModelManager(object, metaclass=ManagerMeta):
    registered: Dict[str, type(Model)]

    def __new__(cls) -> Any:
        return super().__new__(cls)

    @classmethod
    def model(cls, model_name):
        # fixme 同一个对象
        current: type(Model) = cls.registered.get(model_name)

        if current:
            return current()
        raise KeyError("ModelManager hasn't registered model named: " + model_name)

    @classmethod
    def model_class(cls, model_name):
        # fixme 同一个对象
        current: type(Model) = cls.registered.get(model_name)
        if current:
            return current()
        raise KeyError("ModelManager hasn't registered model named: " + model_name)

    @classmethod
    def add_model(cls, model_class: type(Model), *args):
        cls.registered[model_class._name] = model_class
        for model in args:
            cls.registered[model._name] = model
