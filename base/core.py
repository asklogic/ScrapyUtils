from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator, Any
import threading
import scrapy_config
import queue
import time

from base.log import act, status
from base.lib import Config, ComponentMeta
from base.task import Task
from base.Prepare import Prepare, DefaultRequestPrepare
from base.Model import Model, TaskModel, ProxyModel, ModelManager, ModelMeta
from base.scheme import Action, Parse
from base.Process import Processor, Pipeline
from base.common import Proxy_Processor
from base.hub import Hub
from base.Scraper import Scraper
from base.scheme import Scheme


def _load_module(target_root: str or None, file_name: str):
    """
    加载组件文件
    :param target_root:
    :param file_name:
    :return:
    """
    if target_root:
        file = ".".join([target_root, file_name])
    else:
        file = file_name
    target_file = __import__(file, fromlist=[target_root])
    return target_file


def _load_component(module, component: type) -> List[type]:
    """
    加载组件类
    :param module:
    :param component:
    :return:
    """
    # FIXME
    base = [Parse, Action, Processor, Prepare, Model]
    res = []
    flied = [getattr(module, x) for x in dir(module) if not x.startswith("_")]
    for f in flied:
        if (issubclass(type(f), ComponentMeta) or issubclass(type(f), ModelMeta)) and issubclass(f,
                                                                                                 component) and f not in base:
            # print(f)
            res.append(f)
    return res


# abort
def _load_target_component(components: List[type], target_list) -> List[type]:
    """
    选择具体的某几个组件 返回类对象
    :param components:
    :param target_list:
    :return:
    """
    res = []
    if type(target_list) is not list:
        target_list = [target_list]

    for target in target_list:
        for component in components:
            if component.__name__ is target:
                res.append(component)
                break

    # return [r[0] for r in [[c for c in components if t is c.__name__] for t in target_list ]]
    return res


def load_prepare(config: Config) -> Prepare:
    try:
        module = _load_module(config.job, "prepare")
    except ModuleNotFoundError as e:
        module = _load_module(None, "prepare")

    components = _load_component(module, Prepare)
    try:
        prepare = _load_target_component(components, config.prepare)
    except Exception as e:
        act.error("[Config] Job {} didn't have prepaer named: {}".format(config.job, config.prepare))
        raise Exception("config error")
    return prepare[0]


def load_processor(config: Config) -> List[type(Processor)]:
    module = _load_module(config.job, "process")

    components = _load_component(module, Processor)

    return _load_target_component(components, config.process)


def load_model(config: Config) -> List[type(Model)]:
    module = _load_module(config.job, "model")
    components: List[type(Model)] = _load_component(module, Model)

    ModelManager.add_model(ProxyModel)
    ModelManager.add_model(TaskModel)

    for model in components:
        ModelManager.add_model(model)

    if not config.models:
        return components
    else:
        return _load_target_component(components, config.models)


def load_scheme(config: Config) -> List[Action or Parse]:
    module_action = _load_module(config.job, "action")
    module_parse = _load_module(config.job, "parse")

    action_components = _load_component(module_action, Action)
    parse_components = _load_component(module_parse, Parse)

    schemes_class = _load_target_component(action_components + parse_components, config.schemes)

    schemes = [x() for x in schemes_class]

    context = {}
    for scheme in schemes:
        scheme.context = context

    return schemes


def build_prepare(prepare: Prepare) -> Tuple[type(Scraper), List[Task]]:
    scraper, task = prepare.do()
    if not task:
        act.warning("[Config] prepare must yield tasks")
        raise TypeError("[Config] build_prepare error")
    if not scraper:
        scraper = DefaultRequestPrepare.get_scraper()
    return (scraper, task)


def generate_task(prepare: Prepare) -> List[Task]:
    task = prepare.get_tasks()

    if not task:
        act.warning("[Config] prepare must yield tasks")
        raise TypeError("[Config] build_prepare error")
    return task


def generator_scraper(prepare: Prepare) -> Scraper:
    try:
        scraper = prepare.get_scraper()
    except Exception as e:
        scraper = DefaultRequestPrepare.get_scraper()
    return scraper


def initPrepare(target: str) -> type(Prepare):
    pm = _load_module(target, "prepare")
    prepare: List[Prepare] = _load_component(pm, Prepare)

    actives = [x for x in prepare if x._active]

    # 返回第一个
    currnet_prepare: Prepare = actives[0]
    return currnet_prepare


def initModel(target: str) -> List[type(Model)]:
    mm = _load_module(target, "model")
    model: List[Model] = _load_component(mm, Model)

    actives: List[Model] = [x for x in model if x._active]

    # 注册
    [ModelManager.add_model(x) for x in actives]

    # 注册默认Model
    ModelManager.add_model(ProxyModel)
    ModelManager.add_model(TaskModel)

    return actives


def initProcessor(target: str) -> List[type(Processor)]:
    pm = _load_module(target, "process")
    processor = _load_component(pm, Processor)

    actives: List[Processor] = [x for x in processor if x._active]

    return actives


def build_Hub(models: List[type(Model)], processor: List[type(Processor)]):
    sys_hub = Hub([ProxyModel, TaskModel], Pipeline([]), feed=True, timeout=10)
    sys_hub.remove_pipeline("ProxyModel")
    sys_hub.remove_pipeline("TaskModel")

    dump_hub = Hub(models, Pipeline(processor), feed=False, timeout=10, limit=3000)

    return sys_hub, dump_hub


def temp_appendProxy(sys_hub: Hub, number):
    # TODO
    sys_hub.replace_pipeline("ProxyModel", Pipeline([Proxy_Processor]), number * 2)


def scrapy(scheme_list: List[Action or Parse], scraper: Scraper, task: Task, hub: Hub):
    content = ""
    gather_models: List[Model] = []
    try:
        for scheme in scheme_list:
            if isinstance(scheme, Action):
                res = do_action(scheme, task, scraper)
                if res:
                    content = res
            elif isinstance(scheme, Parse):
                gather_models.extend(do_parse(scheme, content))

        for model in gather_models:
            hub.save(model)
    except Exception as e:
        status.error("".join(["[Scrapy] scrapy error ", str(e)]))
        # status.exception(e)
        return False
    return True


def do_action(scheme: Action, task, scraper):
    scheme.delay()
    content = scheme.scraping(task=task, scraper=scraper)
    # print("content: ", content)
    return content


def do_parse(scheme: Parse, content):
    current_models = scheme.parsing(content=content)
    if not current_models:
        return []
    else:
        return list(current_models)


barrier = None
lock = threading.Lock()


class ScrapyThread(threading.Thread):
    def __init__(self, sys_hub: Hub, dump_hub: Hub, prepare: Prepare):
        threading.Thread.__init__(self)

        self.sys: Hub = sys_hub
        self.dump: Hub = dump_hub
        self.prepare: Prepare = prepare
        self.schemes: List[type(Scheme)] = prepare.schemeList

        self.proxy: bool = False

        self.proxy = self.prepare.ProxyAble

    def run(self):
        # load and init scraper
        # scraper, task = build_prepare(load_prepare(self.config))
        scraper = self.prepare.get_scraper()
        task = self.prepare.get_tasks()
        # FIXME 同一个类问题
        # print(id(scraper))
        # return

        # load  scheme
        # schemes: List[Action or Parse] = load_scheme(self.config)
        schemes = [x() for x in self.schemes]

        # reset
        self.reset(scraper)
        for scheme in schemes:
            scheme.context.clear()

        # wait
        barrier.wait()

        # python trigger.py thread ScjstBase

        # loop
        try:
            while True:
                self.sync(self.prepare.Block)
                task = self.sys.pop("TaskModel")

                res = scrapy(schemes, scraper, task, self.dump)
                if res:
                    status.info("success. Task url:{} param {} count - {}".format(task.url, task.param, task.count))
                elif task.count < 5:
                    # reset
                    self.reset(scraper)
                    for scheme in schemes:
                        scheme.context.clear()

                    status.info("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))

                    # back to sys
                    task.count = task.count + 1
                    self.sys.save(task)
                else:
                    status.info("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))

        except queue.Empty as qe:
            status.info("finish")

        scraper.quit()

    def sync(self, delay: int = 0):
        lock.acquire()
        if delay:
            time.sleep(delay)
        else:
            time.sleep(0.5)
        lock.release()

    def reset(self, scraper: Scraper):
        scraper.clear_session()
        if self.proxy:
            proxyInfo: ProxyModel = self.sys.pop("ProxyModel")

            scraper.set_proxy((proxyInfo.ip, proxyInfo.port))

