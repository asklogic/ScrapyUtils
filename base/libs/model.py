from typing import *
from abc import ABC, ABCMeta



class Field(object):

    def __init__(self, default=None, convert=None) -> None:
        self._default = default

        # TODO convert lib （int/json/date...）

        if convert is None:
            self._convert = type(default)
        else:
            self._convert = convert

        super().__init__()

    @property
    def default(self):
        return self._default

    @property
    def convert(self):
        return self._convert

    @convert.setter
    def convert(self, value):
        self._convert = value


class ModelMeta(type):

    def __new__(mcs, name, bases, attrs) -> Any:
        attrs["_name"] = name
        _pure_data = {}
        _converts = {}
        _fields = []

        # remove all Field attribute
        # now model get attribute by __getattr__ that get from pure_data dict
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                attrs.pop(key)
                _fields.append(key)

                if value._convert is not type(None):
                    _pure_data[key] = value._convert(value.default)
                else:
                    _pure_data[key] = value.default
                _converts[key] = value._convert

        # add field info into model cls
        attrs['_fields'] = _fields
        attrs['_pure_data'] = _pure_data
        attrs['_converts'] = _converts

        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=ModelMeta):
    _name: str

    def __new__(cls) -> Any:
        if cls.__name__ is 'Model':
            raise Exception('Model must inheritance')
        return super().__new__(cls)

    def __init__(self) -> None:
        """
        pure_data must init
        converts and fields bind as cls
        """
        self.pure_data = self.__class__._pure_data.copy()

    def __setattr__(self, name: str, value: Any) -> None:
        """
        in fields: save in pure_data
        not in field: save as attr
        """
        if name in self._fields:
            if self._converts[name] is type(None):
                self.pure_data[name] = value
            else:
                self.pure_data[name] = self._converts[name](value)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, item):
        """
        same as __setattr__
        """
        if item in self._fields:
            return self.pure_data[item]
        raise KeyError("Model {0} has no Field named {1}".format(self.name(), item))

    @classmethod
    def name(cls):
        return cls._name

    @property
    def pure_data(self):
        return self._pure_data

    @pure_data.setter
    def pure_data(self, value):
        self._pure_data = value



if __name__ == '__main__':
    Model()
