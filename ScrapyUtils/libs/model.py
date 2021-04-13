from typing import *
from abc import ABC, ABCMeta
import copy


class Field(object):
    """The attribute of Model class.

    add different Fields into Model to get custom Model.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__(self, default=None, convert=None) -> None:
        self._default = default
        self._convert = convert

    @property
    def default(self):
        """The default value of Field."""
        return self._default

    @property
    def convert(self):
        """The convert callable of Field."""
        return self._convert


class ModelMeta(type):

    def __new__(mcs, name, bases, attrs) -> Any:
        # attrs["_name"] = name
        _pure_data = {}
        _converts = {}
        _fields = []

        # remove all Field attribute
        # now model get attribute by __getattr__ that get from pure_data dict
        for key, value in tuple(attrs.items()):
            # if is Field instance.
            if isinstance(value, Field):
                # remove attribute
                attrs.pop(key)

                # append data field into _fileds
                _fields.append(key)

                if value.default and not value.convert:
                    _converts[key] = tuple(value.default)
                _converts[key] = value.convert

                if not value.default and value.convert:
                    _pure_data[key] = value._convert()
                _pure_data[key] = value.default

                if not value.default and not value.convert:
                    _pure_data[key] = ''
                    _converts[key] = None

        # add field info into model cls
        attrs['_fields'] = _fields
        attrs['_pure_data'] = _pure_data
        attrs['_converts'] = _converts

        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=ModelMeta):
    """The data model that to save data.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be d     ocumented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __new__(cls, **kwargs) -> Any:
        # Model must be extended
        if cls.__name__ == 'Model':
            raise Exception('Model must be extended')
        return super().__new__(cls)

    def __init__(self, **kwargs) -> None:
        # copy default value dict from Filed instance.
        self._pure_data = copy.deepcopy(self.__class__._pure_data)

        # set value by kwargs.
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __setattr__(self, name: str, value: Any) -> None:
        """
        in fields: save in pure_data
        not in field: save as attr
        """

        # TODO
        if name in self._fields:
            if self._converts[name]:
                self._pure_data[name] = self._converts[name](value)
            else:
                self._pure_data[name] = value
        else:
            super().__setattr__(name, value)

    def __getattr__(self, item):
        if item in self._fields:
            return self._pure_data[item]
        return super().__getattr__(item)

    @classmethod
    def get_name(cls):
        """

        Returns:

        """
        return cls.__name__

    @property
    def pure_data(self) -> Dict:
        """

        Returns: The key-value data as python dict.

        """

        return self._pure_data


class TaskModel(Model):
    url = Field(convert=str)
    param = Field()
    count = Field(default=0, convert=int)


Task = TaskModel

from collections import deque
def gen():
    d = deque()
    for i in range(1000*100):
        task = Task()
        task.url = 'asdasd'
        d.append(d)


if __name__ == '__main__':
    gen()
