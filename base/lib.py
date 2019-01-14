from abc import abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union


# temp


class Task(object):
    url: str
    param: str

    count: int

    def __init__(self, url=None, param=None):
        self.url = url
        self.param = param
        self.count = 0


class Config(object):

    def __init__(self, conf: Dict):
        job = conf.get("job")
        schemes = conf.get("allow")
        models = conf.get("models")
        prepare = conf.get("prepare")
        conserve = conf.get("conserve")
        process = conf.get("process")

        if not (job and schemes):
            raise KeyError("set your job and schemes")

        if not type(schemes) == list:
            raise TypeError('allow must be a list')
        if not type(models) == list:
            raise TypeError('models must be a list')
        if not models:
            models = []
        if not prepare:
            prepare = "default"
        if not conserve:
            conserve = "default"

        self.job = job
        self.schemes = schemes
        self.models = models
        self.prepare = prepare
        self.conserve = conserve
        self.process = process

    job: str
    schemes: List[str]
    models: List[str]
    prepare: str
    conserve: str

### model
#
# class BaseModel(object):
#     pass
#
#
# class Model(object):
#     # data = {}
#
#     # def __init__(self):
#     #     if not self.name:
#     #         self.name = self.__name__
#
#     def __setitem__(self, key, value):
#         pass
#
#     def __getitem__(self, item):
#         pass
#
#     def __delitem__(self, key):
#         pass
#
#
# class ModelManager(object):
#     models: {}
#
#     def __init__(self, model_list: []):
#         self.models = {}
#         for model in model_list:
#             if not issubclass(model, Model):
#                 # TODO
#                 raise Exception()
#             else:
#                 if hasattr(model, "name"):
#                     self.models[model.name] = []
#                 else:
#                     self.models[model.__name__] = []
#
#     def model_list(self):
#         return list(self.models.keys())
#
#     def get(self, key):
#         if key in self.models:
#             return self.models[key]
#         else:
#             raise KeyError("ModelManger dose not have model : {0}".format(key))
#
#     def __setitem__(self, key, value):
#         if key in self.models:
#             self.models[key].append(value)
#         else:
#             raise KeyError("ModelManger dose not have model : {0}".format(key))
#
#     def __getitem__(self, item):
#         if item in self.models:
#             return self.models[item]
#         else:
#             raise KeyError("ModelManger dose not have model : {0}".format(item))
#
#     def __delitem__(self, key):
#         if key in self.models:
#             self.models.pop(key)
#         else:
#             raise KeyError("ModelManger dose not have model : {0}".format(key))

#
# class currentModel(Model):
#     name = "1"
#     age = 2
#
#
# class BaseScheme(object):
#     pass


# class Action(BaseScheme):
#     scraper: baseScraper
#     manager: ModelManager
#
#     def __init__(self):
#         self.scraper = None
#
#     def check(self):
#         if self.scraper:
#             return True
#         else:
#             return False
#
#     @abstractmethod
#     def scraping(self, task: Task, scraper: baseScraper):
#         pass
#
#
# class DefaultAction(Action):
#     def scraping(self, task: Task, scraper: baseScraper):
#         return scraper.getPage(url=task.url)


# class Parse(BaseScheme):
#     @abstractmethod
#     def parsing(self, content: str, manager: ModelManager):
#         pass
#
#
# class Conserve(object):
#
#     # FIXME
#     def __init__(self):
#         print("conserve init! run start")
#         self.start()
#
#     def __del__(self):
#         print("conserve end! run finish")
#         self.finish()
#
#     @abstractmethod
#     def start(self):
#         pass
#
#     @abstractmethod
#     def finish(self):
#         pass
#
#     def model(self, model: Model):
#         for func in dir(self):
#             if func.startswith("feed"):
#                 f = getattr(self, func)
#                 f(model)


# class BasePrepare(object):
#     pass
#
#
# class Prepare(BasePrepare):
#
#     def __int__(self):
#         self.start_prepare()
#
#     def __del__(self):
#         self.end_prepare()
#
#     def start_prepare(self):
#         pass
#
#     def end_prepare(self):
#         pass
#
#     @classmethod
#     @abstractmethod
#     def scraper_prepared(cls) -> type:
#         pass
#
#     @classmethod
#     @abstractmethod
#     def task_prepared(cls) -> type or list:
#         """
#         可以返回单个task 也可以返回一个Generic
#         :return:
#         """
#         pass
#
#     @classmethod
#     def do(cls) -> Tuple[baseScraper, Union[List, type]]:
#         scraper = cls.scraper_prepared()
#         tasks = cls.task_prepared()
#
#         # FIXME
#         if not tasks:
#             return scraper, tasks
#         try:
#             tasks = list(cls.task_prepared())
#         except TypeError as te:
#             raise TypeError("function task_prepared must return a iterable")
#         return scraper, tasks
#
#     @classmethod
#     def get_scraper(cls):
#         scraper = cls.scraper_prepared()
#         # TODO
#         return scraper
#
#     @classmethod
#     def get_tasks(cls):
#         tasks = cls.task_prepared()
#         try:
#             tasks = list(cls.task_prepared())
#         except TypeError as te:
#             raise TypeError("function task_prepared must return a iterable")
#         return tasks
#
#
# class DefaultRequestPrepare(Prepare):
#
#     @classmethod
#     def scraper_prepared(cls):
#         req = requestScraper()
#         return req
#
#
# def allow(model: type):
#     def wrapper(func):
#         def innerwrapper(*args, **kwargs):
#             if not type(model) == type:
#                 raise TypeError("allow must be class")
#
#             if isinstance(args[1], model):
#                 # TODO
#                 # print("model {0} to conserve")
#                 return func(*args, **kwargs)
#             else:
#
#                 # TODO
#                 # print("nope")
#                 pass
#
#         return innerwrapper
#
#     return wrapper
#
#
# if __name__ == '__main__':
#     DefaultRequestPrepare().do()
