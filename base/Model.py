from abc import abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator, Any


class Field(object):
    xpath: str = ""

    def __init__(self, xpath: str = None):
        self.xpath = xpath

        pass


class Model(object):

    def __init__(self):
        self._data = {}
        self._mapper = {}
        for f in dir(self):
            filed = getattr(self, f)
            if isinstance(filed, Field):
                if filed.xpath:
                    self._mapper[f] = filed.xpath
                self._data[f] = None

    def __setattr__(self, key, value):
        super(Model, self).__setattr__(key, value)
        if key.startswith("_"):
            return
        elif key in self._data.keys():
            self._data[key] = value
        else:
            raise KeyError("Model {0} has no Field named {1}".format(self.__class__.__name__, key))

    def __delattr__(self, item):
        super(Model, self).__delattr__(item)
        self._data.pop(item)

    def __getattr__(self, item):
        super(Model, self).__getattr__(item)
        return self._data.get(item)

    def pure_data(self):
        return self._data

    @abstractmethod
    def feed_back(self):
        pass


class ModelManager(object):
    """
    models
    """

    def __init__(self, model_list: List[type(Model)]):
        self.models: Dict[str, List[Model]] = {}
        self.registered: Dict[str, List[type(Model)]] = {}
        for model in model_list:
            if not issubclass(model, Model):
                # TODO
                raise Exception()
            else:
                if hasattr(model, "name"):
                    self.models[model.name] = []
                    self.registered[model.name] = model
                    self.registered[model.__name__] = model
                else:
                    self.models[model.__name__] = []
                    self.registered[model.__name__] = model

    def model_list(self) -> List[str]:
        return list(self.models.keys())

    def get(self, name) -> List[Model]:
        if name in self.models:
            return self.models[name]
        else:
            raise KeyError("ModelManger dose not have model : {0}".format(name))

    def model(self, name) -> Model:
        current: type = self.registered.get(name)
        if current:
            return current()
        raise KeyError("ModelManger hasn't registered model named: " + name)

    def clear_data(self):
        for key in self.models.keys():
            self.models[key] = []


class ProxyModel(Model):
    container = "proxy"

    ip = Field()
    port = Field()


class FailedTaskModel(Model):
    # container = "proxy"
    url = Field()
    param = Field()


if __name__ == '__main__':
    pass
