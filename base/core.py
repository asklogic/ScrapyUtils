from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import time

from base.Action import Action, DefaultAction
from base.Parse import Parse, DefaultXpathParse
from base.Scraper import Scraper
from base.Prepare import Prepare, DefaultRequestPrepare
from base.Model import Model, ModelManager
from base.Conserve import Conserve
from base.Container import Container, BaseContainer
from base.lib import Task, Config
from base.tool import get_proxy_model
from base.Process import Process, Pipeline

import scrapy_config
import threading

lock = threading.Lock()

from base.log import status, act


# FIXME
def load(job: str, module: str, current_type: type) -> List[type]:
    """
    从job中的module加载所有符合current_type的type 返回为type列表
    :param job: python package
    :param module: component name
    :param current_type: component type
    :return type_list: list of types(class)
    """
    if job:
        # 没有job则从默认根目录
        base_target = __import__(job + "." + module)
        target = getattr(base_target, module)
    else:
        base_target = __import__(module)
        target = base_target
    fields = dir(target)

    type_list = []
    for field in fields:
        t = getattr(target, field)
        if type(t) == type and issubclass(t, current_type) and not t == current_type:
            type_list.append(t)
    return type_list


def load_prepare(prepare_name: str, job: str = "") -> Prepare:
    prepares: List[type(Prepare)]
    try:
        prepares = load(job, "prepare", Prepare) + load("", "prepare", Prepare)
    except ModuleNotFoundError as mnfe:
        prepares = load("", "prepare", Prepare)

    prepares: List[Prepare]
    for prepare in prepares:
        # and 短路
        if prepare.__name__ == prepare_name or (hasattr(prepare, "name") and prepare.name == prepare_name):
            return prepare
    raise ModuleNotFoundError("not found prepare named: {0}".format(prepare_name))


def do_prepare(config: Config) -> Tuple[Scraper, List[Task]]:
    prepare = load_prepare(config.prepare, config.job)
    scraper, task = prepare.do()

    if not scraper:
        act.debug("prepare " + config.prepare + "didn't return a Scraper Instance. Use RequestScraper")
        scraper = DefaultRequestPrepare.get_scraper()
    if not task or type(task) == []:
        raise TypeError(config.prepare + " must yield a task list")
    act.info("prepare info")
    act.info("task length: " + str(len(task)))
    act.info("> scraper: " + str(scraper.__class__.__name__))
    return scraper, task


def load_models(config: Config) -> List[Model]:
    models_list: List[type(Model)] = load(config.job, "model", Model)

    if config.models:
        allow_model_list: List[Model] = []
        for allow in config.models:
            for model in models_list:
                if model.__name__ == allow:
                    allow_model_list.append(model)
                    break

        return allow_model_list + load_default_models()

    return models_list + load_default_models()


def load_default_models() -> List[type(Model)]:
    models_list: List[type(Model)] = load("base", "Model", Model)
    return models_list


def _register_containers(allow_models: List[str], job: str, conserve: Conserve = None) -> Dict[str, Container]:
    models = load_models(allow_model)

    containers: Dict[str, Container] = {}
    for model in models:
        # TODO temp
        if hasattr(model, "container"):
            if model.container == "json":
                # TODO 默认container设置
                containers[model.__name__] = JsonContainer(model.__name__)

            if model.container == "proxy":
                containers[model.__name__] = Container(supply_func=get_proxy_model, supply=scrapy_config.Thread * 2)

            if model.container == "base":
                containers[model.__name__] = BaseContainer()

        else:
            containers[model.__name__] = Container(conserve=conserve)
    return containers


def register_containers(config: Config, pipeline: Pipeline) -> Dict[str, Container]:
    models = load_models(config)

    # TODO 修改container
    containers: Dict[str, Container] = {}
    for model in models:
        if hasattr(model, "container"):
            if model.container == "proxy":
                containers[model.__name__] = Container(supply_func=get_proxy_model, supply=scrapy_config.Thread * 2)
        else:
            containers[model.__name__] = Container(pipeline=pipeline)
        containers[model.__name__].name = model.__name__

    act.info("> models :" + ", ".join(list(map(lambda x: x, containers.keys()))))
    return containers


def register_manager(config: Config) -> ModelManager:
    models = load_models(config)
    return ModelManager(models)


def load_scheme(allow_scheme: List[str], job: str) -> List[Action or Parse]:
    actions = load(job, "action", Action)
    parses = load(job, "parse", Parse)
    defaults = load_default()
    schemes = actions + parses + defaults

    register_list = []

    for allow in allow_scheme:
        for scheme in schemes:
            if scheme.__name__ == allow or (hasattr(scheme, "name") and scheme.name == allow):
                register_list.append(scheme)

    register_list = load_default_scheme(register_list, allow_scheme)

    act.info("> schemes: " + ", ".join(list(map(lambda x: x.__name__, register_list))))

    if len(register_list) >= len(allow_scheme):
        return register_list
    raise ModuleNotFoundError("some scheme cannot found! check scheme and allow_list")


def load_default():
    actions = load("base", "Action", Action)
    parses = load("base", "Parse", Parse)
    return actions + parses


def load_default_scheme(schemes: List[Action or Parse], allow_scheme: List[str]) -> List[Action or Parse]:
    scheme_type = list(map(lambda x: Action if issubclass(x, Action) else Parse, schemes))
    # 短路 如果没有
    if not scheme_type or scheme_type[0] is not Action:
        schemes.insert(0, DefaultAction)

    return schemes


def scrapy(scheme_list: List[Action or Parse], manager: ModelManager, task: Task, scraper: Scraper) -> bool:
    content = ""
    scheme_type = list(map(lambda x: Action if issubclass(x, Action) else Parse, scheme_list))

    try:
        for scheme in scheme_list:
            if issubclass(scheme, Action):
                content = do_action(scheme, task, scraper, manager)
            elif issubclass(scheme, Parse):
                do_parse(scheme, content, manager)
    except Exception as e:
        print(e.args)
        print("scheme {0} except error".format(str(scheme)))
        return False

    return True


def do_action(action: type(Action), task: Task, scraper: Scraper, manager: ModelManager) -> str:
    current_action: Action = action()
    current_action.delay()
    content = current_action.scraping(task=task, scraper=scraper, manager=manager)
    return content


def do_parse(parse: Parse, content: str, manager: ModelManager):
    current_parse = parse()
    # current_models = current_parse.parsing(content=content, manager=manager)

    current_models = current_parse.parsing(content=content, manager=manager)
    # TODO
    if not current_models:
        # log.debug("parse didn't yield a Model")
        return
    for model in current_models:
        name = model.name if hasattr(model, "name") else model.__class__.__name__
        manager.get(name).append(model)


# abort
def load_conserve(conserve_name: str = "default", job: str = "") -> type(Conserve):
    conserves = List[type(Conserve)]
    try:
        conserves = load(job, "conserve", Conserve) + load("", "conserve", Conserve)
    except ModuleNotFoundError as mnfe:
        conserves = load("", "conserve", Conserve)

    conserves: List[Conserve]

    for conserve in conserves:
        if conserve.__name__ == conserve_name or (hasattr(conserve, "name") and conserve.name == conserve_name):
            return conserve
    raise ModuleNotFoundError("not found conserve named: {0}".format(conserve_name))


def load_process(config: Config) -> List[type(Process)]:
    processes = load(config.job, "process", Process)

    registered_processes: List[type(Process)] = []
    for process_name in config.process:
        for process in processes:
            # FIXME
            if process.__name__ == process_name or (hasattr(process, "name") and process.name == process_name):
                registered_processes.append(process)

    act.info("> processes: " + ", ".join(list(map(lambda x: x.__name__, registered_processes))))
    return registered_processes


# abort
# def build_process(processes: List[type(Process)], config: Config) -> Pipeline:
#     pipeline = Pipeline()
#     for process_class in processes:
#         process = process_class()
#         pipeline.add_process(process)
#     pipeline.start_task(config)
#     return pipeline


def finish(containers: Dict[str, Container], pipeline: Pipeline):
    for container in containers:
        containers[container].dump()

    from base.Container import pool
    pool.wait()

    pipeline.end_task()


# abort
def build_conserve(conserve: type(Conserve)):
    # TODO temp: 使用类方法代替
    current_conserve = conserve()
    current_conserve.start_conserve()
    return current_conserve


# abort
def do_conserve(manager: ModelManager, conserve: Conserve) -> bool:
    for models in manager.models.values():
        for m in models:
            try:
                conserve.model(m)
            except Exception() as e:
                print(e.args)
                print("error")
                return False
    return True


# abort
# def load_conf(conf: Dict) -> Config:
#     config = Config()
#
#     job = conf.get("job")
#     schemes = conf.get("allow")
#     models = conf.get("models")
#     prepare = conf.get("prepare")
#     conserve = conf.get("conserve")
#
#     if not (job and schemes):
#         raise KeyError("set your job and schemes")
#     if not models:
#         models = []
#     if not prepare:
#         prepare = "default"
#     if not conserve:
#         conserve = "default"
#
#     config.job = job
#     config.schemes = schemes
#     config.models = models
#     config.prepare = prepare
#     config.conserve = conserve
#     return config


def thread_check(task: Task, scheme_state=True, conserve_state=True) -> Task or None:
    if task.count >= 5:
        # print("failed! task end! task: url:{0} param:{1}".format(task.url, task.param))
        log.info("failed! task end! task: url:{0} param:{1}".format(task.url, task.param))
        return

    if not scheme_state:
        task.count = task.count + 1
        # print("scheme error retry: {0}".format(task.count))
        log.info("scheme error retry: {0}".format(task.count))
        return task
    elif not conserve_state:
        task.count = task.count + 1
        # print("conserve error retry: {0}".format(task.count))
        log.info("conserve error retry: {0}".format(task.count))
        return task
    else:
        # print("success! task: url:{0} param:{1}".format(task.url, task.param))
        log.info("success! task: url:{0} param:{1}".format(task.url, task.param))


def thread_reset(scraper: Scraper, manager: ModelManager):
    scraper.clear_session()
    manager.clear_data()
    scraper.switch_proxy()


def thread_conserve(manager: ModelManager, containers: Dict[str, Container]):
    # FIXME manager register不符合
    # lock.acquire()
    # try:
    #     for model in manager.models.keys():
    #         container = containers.get(model)
    #         model_data = manager.get(model)
    #         for model_data_item in model_data:
    #             container.add(model_data_item)
    # except Exception as e:
    #     return False
    # finally:
    #     lock.acquire()

    for model in manager.models.keys():
        container = containers.get(model)
        model_data = manager.get(model)
        for model_data_item in model_data:
            container.add(model_data_item)
    return True


if __name__ == '__main__':
    from base.Prepare import Prepare
    from base.Action import Action

    # load_scheme(["newAction"], 'hope')
