from typing import *
from types import *


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

    # component
    Target: str = None
    Prepare: str = None
    SchemeList: List[str or ClassVar] = None
    Model: List[str] = None
    Processor: List[str] = None

    # hubs

    Timeout = 5
    DumpLimit = 1500
    FeedLimit = 50

    HubFailedBlock = 2
    HubFailedRetry = 4

    # Proxy
    ProxyAble: bool = None
    ProxyFunc: Callable = None
    # Processor
    Duplication: dict = None


class Setting(BaseSetting):
    Thread = 5
    Block = 0.5
    FailedBlock = Block * 2

    Target = ''
    Prepare = ''
    SchemeList = []
    Model = []
    Processor = []

    # Proxy
    ProxyAble: bool = None
    ProxyFunc: Callable = lambda x: x

    # Processor
    Duplication: dict = {}

    def load_prepare(self, prepare):
        for x in [x for x in dir(BaseSetting) if not x.startswith('__')]:
            if getattr(prepare, x) is not None:
                setattr(self, x, getattr(prepare, x))

    def load_config(self, module: ModuleType):
        for x in [x for x in dir(BaseSetting) if not x.startswith('__')]:
            if hasattr(module, x):
                setattr(self, x, getattr(module, x))
