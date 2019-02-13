from abc import abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union

from base.log import act
from base.Model import ModelManager, TaskModel

ModelManager.add_model(TaskModel)


class Task(object):
    url: str
    param: str

    count: int

    def __new__(cls, *args, **kwargs) -> TaskModel:
        task = ModelManager.model("TaskModel")
        task.count = 0
        return task


class Config(object):

    def __init__(self, conf: Dict):
        job = conf.get("job")
        schemes = conf.get("allow")
        models = conf.get("models")
        prepare = conf.get("prepare")
        process = conf.get("process")

        current_model: List[str] = []
        current_process: List[str] = []
        current_model: List[str] = []
        current_model: List[str] = []

        if not job:
            raise KeyError("please set your target job")

        if not schemes:
            # TODO ? 添加名称还是?
            schemes = "default"

        if not prepare:
            prepare = "DefaultPrepare"

        # 如果只有一个就单独添加
        if not type(models) == list:
            current_model.append(models)
        else:
            current_model.extend(models)

        if not type(process) == list:
            current_process.append(process)
        else:
            current_process.extend(process)

        self.job = job
        self.schemes = schemes
        self.models = current_model
        self.prepare = prepare
        self.process = current_process

    job: str
    schemes: List[str]
    models: List[str]
    process: List[str]
    prepare: str


class ComponentMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        attrs["_name"] = name

        return type.__new__(cls, name, bases, attrs)
