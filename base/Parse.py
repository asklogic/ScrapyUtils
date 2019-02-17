from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
from base.Model import Model, ModelManager
from base.tool import xpathParse
from base.lib import ComponentMeta


class Parse(object, metaclass=ComponentMeta):
    def __init__(self):
        self.context: Dict = {}
        pass

    @abstractmethod
    def parsing(self, content: str) -> Model or Generator[Model]:
        pass


class DefaultXpathParse(Parse):
    name = "xpath"

    def parsing(cls, content: str, manager: ModelManager) -> Model or Generator[Model]:
        for registered in manager.model_list():
            current_model = manager.model(registered)

            if hasattr(current_model, '_mapper'):
                mapper: Dict[str, str] = current_model._mapper
                parsed_mapper: Dict[str, List[str]] = {}
                length = 0
                for filed in mapper.keys():
                    parsed = xpathParse(content, mapper.get(filed))
                    parsed_mapper[filed] = parsed

                    length = len(parsed)
                if hasattr(current_model, "xpath_length"):
                    length = current_model.xpath_length
                for index in range(length):
                    m = manager.model(registered)
                    for key in mapper.keys():
                        try:
                            setattr(m, key, parsed_mapper[key][index])
                        except IndexError as ie:
                            setattr(m, key, None)
                    yield m


class HiddenParse(Parse):

    @classmethod
    def parsing(cls, content: str) -> Model or Generator[Model]:
        pass
