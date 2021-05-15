from dataclasses import dataclass, field, _process_class, asdict, astuple, Field, fields, _MISSING_TYPE
from typing import Any, Dict, Union, List

DEFAULT_VALUE = ''


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        origin_type = super().__new__(mcs, name, bases, attrs)

        default_mapper = {}
        if object not in bases:
            # Add __annotations__ dict in no-annotations class.
            if not hasattr(origin_type, '__annotations__'):
                setattr(origin_type, '__annotations__', {})

            # Auto type hinting
            for attr, value in attrs.items():
                if isinstance(value, Field):
                    if isinstance(value.default, _MISSING_TYPE) and isinstance(value.default_factory, _MISSING_TYPE):
                        default_mapper[attr] = DEFAULT_VALUE
                    # elif isinstance(value.default, _MISSING_TYPE):
                    #     default_mapper[attr] = value.default_factory()
                    # # elif isinstance(value.default_factory, _MISSING_TYPE):
                    # else:
                    #     default_mapper[attr] = value.default

                    if not origin_type.__annotations__.get(attr):
                        origin_type.__annotations__[attr] = Any

        # Hook here.
        dataclass_type = _process_class(origin_type, True, True, True, False, False, False)

        # Add default_mapper in class property.
        # dataclass_type.default_mapper = default_mapper

        # Extend will destory default __init__ with default
        # Add initial wrapper.
        current_init = dataclass_type.__init__

        def init_mapper(self, **kwargs):
            for k, v in default_mapper.items():
                kwargs.setdefault(k, v)
            # kwargs.update(default_mapper)
            # default_mapper.update(kwargs)
            current_init(self, **kwargs)

        dataclass_type.__init__ = init_mapper

        return dataclass_type


class Model(object, metaclass=ModelMeta):

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    @property
    def pure_data(self, to_tuple=False) -> Dict[str, Any]:
        if to_tuple:
            return astuple(self)
        else:
            return asdict(self)

    @classmethod
    def get_name(cls):
        return cls.__name__


class Proxy(Model):
    """
    The common Model.
    """
    ip: str = field()
    port: Union[int, str] = field()


class Task(Model):
    """
    The common Model.
    """
    url: str = field()
    count: int = field(default=0)
    param: Dict = field(default_factory=dict)


if __name__ == '__main__':
    p = Proxy(ip='1')
    print(p.pure_data)
    print(Task().pure_data)
