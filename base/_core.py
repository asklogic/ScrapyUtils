from base.lib import Action, Model, Task, Parse, ModelManager, Conserve, Prepare, DefaultRequestPrepare, \
    DefaultAction
import scrapy_config
from base import log
import time
import queue
from base.scrapy_thread import threadTask
from typing import TypeVar, Generic, Tuple, List, Dict

# Log = log.getLog()
BreifLog = log.getbriefLog()


def task_run(conf: {}):
    job = conf["name"]
    allow_list = conf["allow"]
    prepare = conf["prepare"]
    conserve = conf["conserve"]

    BreifLog.info("single task run!")
    time.sleep(0.5)

    # load scheme
    scheme_list = load_scheme(job, allow=allow_list)
    BreifLog.info("schemes load:")
    BreifLog.info(str(scheme_list))

    # load model

    # model_list = load_model(job)
    model_list = _load(job, 'model', Model)

    # load modelManager
    manager = ModelManager(model_list)
    BreifLog.info("Load ModelManager .Register {0} models: ".format(len(manager.model_list())))
    BreifLog.info(str(manager.model_list()))

    # check scraper ? ready
    scraper, tasks = _do_prepare(prepare, job)
    BreifLog.info("Scraper load:")
    BreifLog.info(str(scraper))
    block(6, "scrapy", BreifLog)

    # check conserve - init TODO

    # scraper to scheme / model to parser
    # do scheme / task in schemes
    # scraper to scheme / model to parser
    # do scheme / task in schemes
    task = tasks[0]
    scrapy(scheme_list, manager, task, scraper)
    BreifLog.debug("Scrapy finish!")
    time.sleep(1)

    # models to conserve
    current_conserve = _load(job, "conserve", Conserve)[0]
    do_conserve(manager, current_conserve)
    BreifLog.debug("conserve finish!")
    BreifLog.info("single task end")

    scraper.safeQuit()

    # report
    # done


# abort
# def _load_scheme(job: str, allow_list: list = None):
#     action_list = []
#     parse_list = []
#     targetAction = __import__(job + ".action").action
#     targetParse = __import__(job + ".parse").parse
#
#     if not allow_list:
#         action_fields = dir(targetAction)
#         action_fields.remove("Action")
#
#         parse_fields = dir(targetParse)
#         parse_fields.remove("Parse")
#
#         allow_list = parse_fields + action_fields
#
#     # FIXME 判断加载
#     for field in allow_list:
#         if field.lower().find("action") > 0:
#             t = getattr(targetAction, field)
#             if type(t) == type and issubclass(t, Action):
#                 action_list.append(t)
#         elif field.lower().find("parse") > 0:
#             t = getattr(targetParse, field)
#             if type(t) == type and issubclass(t, Parse):
#                 parse_list.append(t)
#     return action_list + parse_list


def load_scheme(job, allow):
    actions = _load(job, "action", Action)
    parses = _load(job, "parse", Parse)
    scheme_list = actions + parses

    register_list = []
    for al in allow:
        for scheme in scheme_list:
            if scheme.__name__ == al:
                register_list.append(scheme)
    if len(register_list) == len(allow):
        return register_list
    raise ModuleNotFoundError("some scheme cannot found! check scheme and allow_list")


# FIXME 修改_load的参数规范
def _load(job, module, current_type) -> List[type]:
    """
    从job中的module加载所有符合current_type的type 返回为type列表
    :param job: python package
    :param module: component name
    :param current_type: component type
    :return type_list: list of types(class)
    """
    if job:
        baseTarget = __import__(job + "." + module)
        target = getattr(baseTarget, module)

    else:
        baseTarget = __import__(module)
        target = baseTarget
    fields = dir(target)

    type_list = []
    for field in fields:
        t = getattr(target, field)
        if type(t) == type and issubclass(t, current_type) and not t == current_type:
            type_list.append(t)
    return type_list


# def load_model(job: str):
#     model_list = []
#     target = __import__(job + ".model").model
#     fields = dir(target)
#     fields.remove("Model")
#
#     for field in fields:
#         t = getattr(target, field)
#         if type(t) == type and issubclass(t, Model):
#             model_list.append(t)
#     return model_list


# def _do_prepare(job: str, prepare_name=None):
#     '''
#
#     :param job: 是哪一个job
#     :return: scraper 对象
#     '''
#
#     if not job or not prepare_name:
#         # FIXME
#         print("load defualt prepare")
#         # TODO
#         return DefaultRequestPrepare.do()
#
#     try:
#         target = __import__(job + ".prepare").prepare
#     except ModuleNotFoundError as e:
#         # FIXME
#         if str(e).find(".") < 0:
#             print("no job named: {0}".format(job))
#         else:
#             print("job: {0} has no prepare.py".format(job))
#         return DefaultRequestPrepare.do()
#
#     if prepare_name in dir(target):
#         prepare = getattr(target, prepare_name)
#         return prepare.do()
#     raise AttributeError("Module {0} doesn't have Prepare {1}".format(target, prepare_name))


def _do_prepare(prepare_name, job=""):
    """
    abort
    :param prepare_name:
    :param job:
    :return:
    """
    scraper = None
    tasks = None
    try:
        prepares = _load(job, "prepare", Prepare)
    except ModuleNotFoundError as mnfe:
        prepares = _load("", "prepare", Prepare)

    for prepare in prepares:
        if prepare.__name__ == prepare_name:
            scraper, tasks = prepare.do()
            if not scraper:
                scraper = DefaultRequestPrepare.do()[0]
            return scraper, tasks
    raise AttributeError("{0} doesn't have Prepare class: {1}".format(job if job else __name__, prepare_name))


def do_prepare(name: str = "defulat", job: str = ""):
    prepare = load_prepare(name, job)
    scraper, task = prepare.do()

    if not scraper:
        scraper = DefaultRequestPrepare.do()[0]



def load_prepare(prepare_name: str, job: str = "") -> Prepare:
    try:
        prepares = _load(job, "prepare", Prepare)
    except ModuleNotFoundError as mnfe:
        prepares = _load("", "prepare", Prepare)

    prepares: List[Prepare]
    for prepare in prepares:
        # and 短路
        if prepare.__name__ == prepare_name or (hasattr(prepare, "name") and prepare.name == prepare_name):
            return prepare
    raise ModuleNotFoundError("not found prepare named: {0}".format(prepare_name))


def thread_task_run(conf: {}):
    job = conf["name"]
    allow_list = conf["allow"]
    prepare = conf["prepare"]
    conserve = conf["conserve"]

    BreifLog.info("thread task run!")
    time.sleep(2)

    prepare = load_prepare(prepare, job)

    q = queue.Queue()
    for task in prepare.get_tasks():
        q.put(task)

    for i in range(5):
        t = threadTask(queue)
        t.start()

    # load prepare
    # load threading
    # load scraper
    # load conserve

    # get task
    # task in scheme
    # models to conserve
    # loop
    # jump for empty / report
    # wait signal / cmd
    # done

    pass


def scrapy(schemes, manager, task, scraper):
    content = ""
    scheme_type = list(map(lambda x: Action if issubclass(x, Action) else Parse, schemes))
    if scheme_type[0] is not Action:
        content = do_action(DefaultAction, task, scraper, manager)
    for scheme in schemes:
        if issubclass(scheme, Action):
            content = do_action(scheme, task, scraper, manager)
        elif issubclass(scheme, Parse):
            do_parser(scheme, content, manager)

    if Parse not in scheme_type:
        # TODO
        pass


def do_action(scheme: type, task: Task, scraper, manager):
    currentAction: Action = scheme()
    currentAction.manager = manager

    content = currentAction.scraping(task=task, scraper=scraper)
    return content


def do_parser(scheme: type, content, manager: ModelManager):
    currentParse: Parse = scheme()

    currentModel = currentParse.parsing(content, manager)
    # TODO check
    for model in currentModel:
        name = model.__class__.__name__
        manager.get(name).append(model)


def do_conserve(manager: ModelManager, conserve):
    conserve = conserve()
    for models in manager.models.values():
        for m in models:
            conserve.model(m)


# TODO
def load_conifg(conf: {}):
    pass


# todo
def report():
    pass


def block(times: int, msg: "", log=None):
    for t in range(times):
        t = times - t
        if log:
            log.debug("{0} second to {1}".format(str(t), msg))
        else:
            print("{0} second to {1}".format(str(t), msg))
        time.sleep(1)


def l():
    pass


if __name__ == '__main__':
    task_run(scrapy_config.scjst_base)
