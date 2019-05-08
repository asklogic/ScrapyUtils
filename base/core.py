from typing import *
from types import *
import threading
import queue
import time
import warnings

from base.log import act, status
from base.libs.setting import Setting
from base.components.base import Component, ComponentMeta
from base.libs.task import Task, TaskModel
from base.components.prepare import Prepare
from base.components.model import ModelMeta, Model, ModelManager
from base.components.scheme import Action, Parse, Scheme
from base.hub.pipeline import Pipeline
from base.components.proceesor import Processor
from base.common import ProxyProcessor, ProxyModel
from base.hub.hub import Hub
from base.libs.scraper import Scraper

import copy

ModelManager.add_model(TaskModel)


def load_files(target_name: str) -> List[ModuleType]:
    target_modules: List[ModuleType] = []

    try:
        __import__(target_name)
    except ModuleNotFoundError as mnfe:
        mnfe.msg = 'cannot found target named ' + target_name
        raise mnfe

    for file_names in ['action', 'parse', 'prepare', 'model', 'process']:
        try:
            module = __import__('.'.join([target_name, file_names]), fromlist=[target_name])
            target_modules.append(module)
        except ModuleNotFoundError as me:
            # TODO
            act.error("project must set a {}.py".format(file_names))
            act.critical("failed in load_files")
            raise me

    return target_modules


def load_components(target_name: str = None) -> Tuple[Prepare, List[Scheme], List[Model], List[Processor]]:
    # search modules in target dir
    target_modules = load_files(target_name)

    # load all components
    components: Set[Component] = set()

    for module in target_modules:
        attrs: List[str] = dir(module)
        for attr in attrs:
            current_attr = getattr(module, attr)

            # issubclass 类型问题
            # if (target_name and target_name in str(current_attr) and issubclass(current_attr, Component)):
            if (target_name and target_name in str(current_attr) and not attr.startswith('__')):
                components.add(current_attr)
    # classify components & pack ups
    prepares: List[Prepare] = [x for x in components if issubclass(x, Prepare) and x._active]
    schemes: List[Scheme] = [x for x in components if issubclass(x, Scheme) and x._active]
    models: List[Model] = [x for x in components if issubclass(x, Model) and x._active]
    processors: List[Processor] = [x for x in components if issubclass(x, Processor) and x._active]

    return prepares, schemes, models, processors


def build_setting(target: str) -> Setting:
    # 1. Setting object
    # default setting in Setting class property
    setting = Setting()

    # 2. load config.py

    try:
        config = __import__('config')
        setting.load_config(config)
    except ModuleNotFoundError as mnfe:
        warnings.warn('there is not config.py')

    # 3. load and check components
    components = load_components(target)
    setting.check_components(components)

    # 4. add default and check prepare
    setting.default()

    return setting


def build_schemes(scheme_list: List[type(Scheme)]) -> List[Scheme]:
    for scheme in scheme_list:
        assert issubclass(scheme, Scheme)

    schemes = [x() for x in scheme_list]
    # 同一个dict
    context = {}
    for scheme in schemes:
        scheme.context = context
    return schemes


def load_context(task: Task, schemes: List[Scheme]):
    if task.param and type(task.param) is dict:
        for key, item in task.param.items():
            schemes[0].context[key] = item


def build_thread_prepare(prepare: Prepare, thread: int) -> Tuple[List[Scraper], List[Task]]:
    tasks = prepare.get_tasks()
    scrapers: List[Scraper] = []
    for i in range(thread):
        thread_scraper: Scraper = prepare.get_scraper()
        scrapers.append(thread_scraper)
    return scrapers, tasks


def build_thread_schemes(schemes: List[Scheme], thread: int) -> List[List[Scheme]]:
    schemes = build_schemes(schemes)
    schemes_list: List[List[Scheme]] = []
    for i in range(thread):
        thread_schemes = []
        context = {}
        for scheme in schemes:
            current: schemes = copy.copy(scheme)
            current.context = context
            thread_schemes.append(current)
        schemes_list.append(thread_schemes)
    return schemes_list


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



def build_prepare(prepare: Prepare) -> Tuple[type(Scraper), List[Task]]:
    try:
        scraper = prepare.get_scraper()
        tasks = prepare.get_tasks()
    except Exception as e:
        act.exception(e)
        raise Exception('build_prepare failed')
    return scraper, tasks


def generate_task(prepare: Prepare) -> List[Task]:
    task = prepare.get_tasks()

    if not task:
        act.warning("[Config] prepare must yield tasks")
        raise TypeError("[Config] build_prepare error")
    return task


def build_hub(setting: Setting):
    models = setting.CurrentModels
    processors = setting.CurrentProcessorsList

    for model in models:
        assert issubclass(model, Model)
        ModelManager.add_model(model)

    ModelManager.add_model(ProxyModel)
    ModelManager.add_model(TaskModel)

    sys_hub = Hub([ProxyModel, TaskModel], setting=setting)

    if setting.ProxyAble:
        sys_hub.add_feed_pipeline('ProxyModel', Pipeline([ProxyProcessor], setting=setting))

    dump_hub = Hub(setting=setting)
    dump_hub.add_dump_pipeline('Model', Pipeline(processors, setting=setting))

    return sys_hub, dump_hub


def scrapy(scheme_list: List[Action or Parse], scraper: Scraper, task: Task, dump_hub: Hub, sys_hub: Hub):
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
            if isinstance(model, TaskModel):
                sys_hub.save(model)
            else:
                dump_hub.save(model)
    except Exception as e:
        import traceback
        import linecache

        # TODO refact
        error_info = []
        error_info.extend(('Scheme:' + scheme.get_name(),))
        error_info.extend(('Exception:' + e.__class__.__name__,))
        # error_info.extend(('msg: ' + ''.join(e.args),))

        current = e.__traceback__

        while current.tb_next is not None:
            current = current.tb_next
        code = current.tb_frame.f_code
        code_content = linecache.getline(code.co_filename, current.tb_lineno, current.tb_frame.f_globals).strip()
        error_info.extend(('\ncode: ' + code_content,))

        status.error(' | '.join(error_info))

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
    def __init__(self, sys_hub: Hub, dump_hub: Hub, schemes: List[Scheme], scraper: Scraper, setting: Setting):
        threading.Thread.__init__(self)

        self.sys: Hub = sys_hub
        self.dump: Hub = dump_hub
        self.schemes: List[Scheme] = schemes
        self.scraper: Scraper = scraper

        self.setting: Setting = setting

    def run(self):
        # load and init scraper

        # reset
        self.reset()

        # wait
        # barrier.wait()

        # python trigger.py thread ScjstBase
        # loop
        try:
            while True:
                self.sync(self.setting.Block)
                task: Task = self.sys.pop("TaskModel")

                load_context(task, self.schemes)

                res = scrapy(self.schemes, self.scraper, task, self.dump, self.sys)
                if res:
                    status.info("success. Task url:{} param {} count - {}".format(task.url, task.param, task.count))
                elif task.count < self.setting.FailedRetry:
                    # reset
                    self.reset()

                    # sleep
                    time.sleep(self.setting.FailedBlock)
                    # status.info("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))

                    # back to sys
                    task.count = task.count + 1
                    self.sys.save(task)
                else:
                    time.sleep(self.setting.FailedBlock)
                    status.info("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))

        except queue.Empty as qe:
            status.info("finish")

        self.scraper.quit()

    def sync(self, delay: int = 0):
        lock.acquire()
        if delay:
            time.sleep(delay)
        else:
            time.sleep(0.5)
        lock.release()

    def reset(self):
        self.scraper.clear_session()
        if self.setting.ProxyAble:
            proxy_model: ProxyModel = self.sys.pop("ProxyModel")
            self.scraper.set_proxy((proxy_model.ip, proxy_model.port))

        # fixme
        for scheme in self.schemes:
            scheme.context.clear()
