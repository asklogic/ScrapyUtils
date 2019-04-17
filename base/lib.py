from typing import *
from types import *

import warnings


# from base.scheme import Scheme

class Config(object):

    def __init__(self, config_file, config_name: str):
        target_config: dict = getattr(config_file, config_name)

        job = target_config.get("job")
        schemes = target_config.get("schemes")
        models = target_config.get("models")
        prepare = target_config.get("prepare")
        process = target_config.get("process")
        project = target_config.get("project")

        current_model: List[str] = []
        current_process: List[str] = []
        current_project: Dict[str, str] = {}

        # job
        if not job:
            job = config_name

        if (not schemes) and (type(schemes) is not list):
            raise KeyError("Config must set your target scheme list")

        if not prepare:
            prepare = "DefaultPrepare"

        # 如果只有一个就单独添加
        if not models:
            raise KeyError("Config must set your target models list")
        elif not type(models) == list:
            current_model.append(models)
        else:
            current_model = models

        if not process:
            raise KeyError("Config must set your target process list")
        elif not type(process) == list:
            current_process.append(process)
        else:
            current_process.extend(process)

        if not project:
            for project_setting in ("Thread", "Block", "Proxy_Able", "Project_Path"):
                setting = getattr(config_file, project_setting)
                current_project[project_setting] = setting
        else:
            for project_setting in ("Thread", "Block", "Proxy_Able", "Project_Path"):
                current_project[project_setting] = project[project_setting]

        self.job = job
        self.prepare = prepare
        self.schemes = schemes
        self.models = current_model
        self.process = current_process
        self.project = current_project

    job: str
    schemes: List[str]
    models: List[str]
    process: List[str]
    prepare: str
    project: Dict[str, str]


class ComponentMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        attrs["_name"] = name

        if not attrs.get("_active"):
            attrs["_active"] = False

        return type.__new__(cls, name, bases, attrs)


class Component(object, metaclass=ComponentMeta):
    pass


class BaseSetting(object):
    # common
    Thread: int = None
    Block: int = None
    FailedBlock: int = None
    FailedRetry: int = None

    # component
    Target: str = None
    Prepare: str = None
    SchemeList: List[str or ClassVar] = None
    Model: List[str or ClassVar] = None
    ProcessorList: List[str or ClassVar] = None

    # hubs

    Timeout = None
    DumpLimit = None
    FeedLimit = None

    PipelineFailedBlock = None
    PipelineFailedRetry = None

    # Proxy
    ProxyAble: bool = None
    ProxyFunc: Callable = None

    ProxyURL: str = None
    ProxyNumberParam: tuple = None

    # ProcessorList
    Duplication: dict = None


class Setting(BaseSetting):
    Thread = 5
    Block = 0.5
    FailedBlock = Block * 2
    FailedRetry: int = 3

    Target = ''
    Prepare = ''
    SchemeList = []
    Model = []
    ProcessorList = []

    # Proxy
    ProxyAble: bool = False
    ProxyFunc: Callable = None

    ProxyURL: str = ''
    ProxyNumberParam = ''

    # ProcessorList
    Duplication: dict = {
        'host': '127.0.0.1',
        'port': '6379',
        'password': '',
    }

    # load

    CurrentPrepare = None
    CurrentSchemeList = []
    CurrentModels = []
    CurrentProcessorsList = []

    def __init__(self):



        # common
        self.Thread = 5
        self.Block = 0.5
        self.FailedBlock = self.Block * 2
        self.FailedRetry: int = 3

        # components
        self.Target = ''
        self.Prepare = ''
        self.SchemeList = []
        self.Model = []
        self.ProcessorList = []

        # hub
        self.Timeout = 5
        self.DumpLimit = 1500
        self.FeedLimit = self.Thread * 2

        self.PipelineFailedBlock = 3
        self.PipelineFailedRetry = 4

        # proxy
        self.ProxyAble = False
        self.ProxyFunc: Callable = None

        self.ProxyURL: str = ''
        self.ProxyNumberParam = {}

        self.Duplication = {
            'host': '127.0.0.1',
            'port': '6379',
            'password': '',
        }

        self.CurrentPrepare = None
        self.CurrentSchemeList = []
        self.CurrentModels = []
        self.CurrentProcessorsList = []

    def load_prepare(self):
        for x in [x for x in dir(BaseSetting) if not x.startswith('__')]:
            attr = getattr(self.CurrentPrepare, x)
            if attr is not None:
                setattr(self, x, getattr(self.CurrentPrepare, x))

    def load_config(self, module: ModuleType):
        for x in [x for x in dir(BaseSetting) if not x.startswith('__')]:
            if hasattr(module, x):
                setattr(self, x, getattr(module, x))

    def check_components(self, components):
        from base.Prepare import Prepare
        from base.scheme import Scheme
        from base.Model import Model
        from base.Process import Processor

        prepares, schemes, models, processors = components

        for prepare in prepares:
            if self.Prepare == prepare._name:
                self.CurrentPrepare = Prepare

        if not self.CurrentPrepare and len(prepares) is not 0:
            self.CurrentPrepare = prepares[0]
        if not self.CurrentPrepare:
            raise ModuleNotFoundError("there isn't have activated prepare class in Prepare.py")

        self.load_prepare()

        # TODO refact
        for current_scheme in self.SchemeList:
            if type(current_scheme) is str:
                res = [x for x in schemes if x._name == current_scheme]
                if len(res) is 0:
                    raise KeyError('cannot found Scheme named ' + current_scheme)
                else:
                    self.CurrentSchemeList.append(res[0])
            elif issubclass(current_scheme, Scheme):
                self.CurrentSchemeList.append(current_scheme)
            else:
                raise TypeError('elements of SchemeList only support str or Scheme Type')

        for current_model in self.Model:
            if issubclass(current_model, Model):
                self.CurrentModels.append(current_model)
            elif type(current_model) is str:

                res = [x for x in models if x._name == current_model]
                if len(res) is 0:
                    raise KeyError('cannot found Model named ' + current_model)
                else:
                    self.CurrentModels.append(res[0])
            else:
                raise TypeError('elements of Model only support str or Model Type')

        for current_processor in self.ProcessorList:
            if issubclass(current_processor, Processor):
                self.CurrentProcessorsList.append(current_processor)
            elif type(current_processor) is str:

                res = [x for x in processors if x._name == current_processor]
                if len(res) is 0:
                    raise KeyError('cannot found Processor named ' + current_processor)
                else:
                    self.CurrentProcessorsList.append(res[0])
            else:
                raise TypeError('elements of ProcessorsList only support str or Processor Type')

    def check(self, components):
        prepares, schemes, models, processors = components
        # TODO
        from base.Prepare import Prepare
        from base.scheme import Scheme, Action, Parse
        from base.Model import Model
        from base.Process import Processor

        if not self.CurrentSchemeList:
            actions = [x for x in schemes if issubclass(x, Action)]
            parses = [x for x in schemes if issubclass(x, Parse)]

            [self.CurrentSchemeList.append(x) for x in actions]
            [self.CurrentSchemeList.append(x) for x in parses]

        if not [x for x in self.CurrentSchemeList if issubclass(x, Action)]:
            raise warnings.warn('cannot found any action class')

        if not self.CurrentProcessorsList:
            self.CurrentProcessorsList = processors

        if not self.CurrentModels:
            self.CurrentModels = models
