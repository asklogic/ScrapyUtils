import time
import os
import sys

from threading import Thread

# from ScrapyUtils.log import logger
# from ScrapyUtils.components.base import Component, ComponentMeta
# from ScrapyUtils.libs.task import Task, TaskModel
# from ScrapyUtils.libs import Model, Scraper, RequestScraper
# from ScrapyUtils.components.scheme import Action, Parse, Scheme
# from ScrapyUtils.components.proceesor import Processor
# # from ScrapyUtils.common import ProxyProcessor, ProxyModel
# from ScrapyUtils.libs.scraper import Scraper
# from ScrapyUtils.components import *
# from ScrapyUtils.components.step import Step, ActionStep, ParseStep

PROJECT_PATH = os.getcwd()

if getattr(sys, 'frozen', False):
    sys.path.append(os.path.dirname(sys.executable))
    os.chdir(os.path.dirname(sys.executable))


class Watcher(Thread):
    def run(self):
        char_list = ['-', '\\', '|', '/']
        count = 0

        while self.exit_flag:
            time.sleep(self.delay)

            print('\r' + self.start_content + ' ' + char_list[count % 4], end='', flush=True)

            count += 1
            if count * self.delay > self.timeout:
                break

        print(f'\r{self.start_content} - {self.end_content}')

    def __init__(self, timeout=20, start_content="Loading", end_content="Done!", delay=0.5,
                 daemon=True) -> None:
        super().__init__(daemon=daemon)

        self.exit_flag = True
        self.timeout = timeout
        self.start_content = start_content
        self.end_content = end_content
        self.delay = delay

        self.start()
        self.current_time = time.time()

    def exit_watch(self, spend=False):
        self.exit_flag = False
        spend_time = time.time() - self.current_time

        self.join()
        if spend:
            print('spend time:', spend_time)

# def load_files(target_name: str) -> List[ModuleType]:
#     target_modules: List[ModuleType] = []
#
#     try:
#         __import__(target_name)
#     except ModuleNotFoundError as mnfe:
#         mnfe.msg = 'cannot found target named ' + target_name
#         raise mnfe
#
#     for file_names in ['action', 'parse', 'prepare', 'model', 'process']:
#         try:
#             module = __import__('.'.join([target_name, file_names]), fromlist=[target_name])
#             target_modules.append(module)
#         except ModuleNotFoundError as me:
#             # TODO
#             logger.error("project must set a {}.py".format(file_names))
#             logger.critical("failed in load_files")
#             raise me
#
#     return target_modules
#
#
# def load_components(target_name: str = None) -> Tuple[List[Scheme], List[Model], List[Processor]]:
#     # search modules in target dir
#     target_modules = load_files(target_name)
#
#     # load all components
#     components: Set[Component] = set()
#
#     for module in target_modules:
#         attrs: List[str] = dir(module)
#         for attr in attrs:
#             current_attr = getattr(module, attr)
#
#             # issubclass 类型问题
#             # if (target_name and target_name in str(current_attr) and issubclass(current_attr, Component)):
#             if (target_name and target_name in str(current_attr) and not attr.startswith('__')):
#                 components.add(current_attr)
#     # classify components & pack ups
#     prepares: List[Prepare] = [x for x in components if issubclass(x, Prepare) and x._active]
#     schemes: List[Scheme] = [x for x in components if issubclass(x, Scheme) and x._active]
#     models: List[Model] = [x for x in components if issubclass(x, Model) and x._active]
#     processors: List[Processor] = [x for x in components if issubclass(x, Processor) and x._active]
#
#     return prepares, schemes, models, processors
#
#
# def build_schemes(scheme_list: List[type(Scheme)]) -> List[Scheme]:
#     for scheme in scheme_list:
#         assert issubclass(scheme, Scheme)
#
#     schemes = [x() for x in scheme_list]
#     # 同一个dict
#     context = {}
#     for scheme in schemes:
#         scheme.context = context
#     return schemes
#
#
# def load_context(task: Task, schemes: List[Scheme]):
#     if task.param and type(task.param) is dict:
#         for key, item in task.param.items():
#             schemes[0].context[key] = item
#
#
# def build_thread_schemes(schemes: List[Scheme], thread: int) -> List[List[Scheme]]:
#     schemes = build_schemes(schemes)
#     schemes_list: List[List[Scheme]] = []
#     for i in range(thread):
#         thread_schemes = []
#         context = {}
#         for scheme in schemes:
#             current: schemes = copy.copy(scheme)
#             current.context = context
#             thread_schemes.append(current)
#         schemes_list.append(thread_schemes)
#     return schemes_list
#
#
# def _load_module(target_root: str or None, file_name: str):
#     """
#     加载组件文件
#     :param target_root:
#     :param file_name:
#     :return:
#     """
#     if target_root:
#         file = ".".join([target_root, file_name])
#     else:
#         file = file_name
#     target_file = __import__(file, fromlist=[target_root])
#     return target_file
#
#
# def _load_component(module, component: type) -> List[type]:
#     """
#     加载组件类
#     :param module:
#     :param component:
#     :return:
#     """
#     # FIXME
#     base = [Parse, Action, Processor, Prepare, Model]
#     res = []
#     flied = [getattr(module, x) for x in dir(module) if not x.startswith("_")]
#     for f in flied:
#         if (issubclass(type(f), ComponentMeta) or issubclass(type(f), ModelMeta)) and issubclass(f,
#                                                                                                  component) and f not in base:
#             # print(f)
#             res.append(f)
#     return res
#
#
# def do_action(scheme: Action, task, scraper):
#     scheme.delay()
#     content = scheme.scraping(task=task, scraper=scraper)
#     # print("content: ", content)
#     return content
#
#
# def do_parse(scheme: Parse, content):
#     current_models = scheme.parsing(content=content)
#     if not current_models:
#         return []
#     else:
#         return list(current_models)
#
#
# def components_detail(components: List[Component], head: str = 'components'):
#     head = 'Activated {}:  {}\n'.format(head, len(components))
#     content = '\n'.join(['\t{}) {}'.format(components.index(x), x.get_name()) for x in components])
#     return head + content
#
#
# def collect(scheme_path: str, file_name: str, component: Type) -> List[Component]:
#     module = _load_file(scheme_path, file_name)
#     components = _load_components(module, component)
#
#     return components
#
#
# def _load_file(scheme_path: str, file_name: str) -> ModuleType:
#     assert os.path.exists(scheme_path), scheme_path
#     assert os.path.isdir(scheme_path), scheme_path
#     file_path = os.path.join(scheme_path, file_name)
#
#     assert os.path.exists(file_path), file_path
#     assert os.path.isfile(file_path), file_path
#
#     scheme = os.path.basename(scheme_path)
#
#     # TODO: imp
#     module = importlib.import_module(scheme + '.' + file_name.split('.')[0])
#     return module
#
#
# def _load_components(module: ModuleType, component: Type):
#     components: List[Component] = []
#     for attr in dir(module):
#         attribute = getattr(module, attr)
#         # 短路判断类
#         if isinstance(attribute, type) and issubclass(attribute, component) and attribute is not component:
#             components.append(attribute)
#     return components
#
#
# def collect_steps(scheme_path) -> List[Step]:
#     actions = collect(scheme_path, 'action.py', ActionStep)
#     parses = collect(scheme_path, 'parse.py', ParseStep)
#
#     # remove deactive
#     steps = [x for x in actions + parses if x.active]
#
#     # sort
#     steps.sort(key=lambda x: x.priority, reverse=True)
#     return steps
#
#
# def collect_processors(scheme_path) -> List[Processor]:
#     origin_processors = collect(scheme_path, 'processor.py', Processor)
#     # remove active
#     processors = [x for x in origin_processors if x.active]
#
#     # sort
#     processors.sort(key=lambda x: x.priority, reverse=True)
#     return processors
#
#
# def _load_profile(scheme_path, profile_name: str = 'profile.py'):
#     assert os.path.exists(scheme_path)
#     assert os.path.isdir(scheme_path)
#
#     profile: str = os.path.join(scheme_path, profile_name)
#
#     scheme = os.path.basename(scheme_path)
#
#     # TODO: imp
#     module = importlib.import_module(scheme + '.' + profile_name.split('.')[0])
#     return module
#
#
# def _invoke_scraper():
#     pass
#
#
# def collect_profile(scheme_path, profile_name: str = 'profile.py'):
#     module = _load_profile(scheme_path, profile_name)
#     config = {}
#
#     # common setting(
#     config['thread'] = getattr(module, 'THREAD', 5)
#     config['timeout'] = getattr(module, 'TIMEOUT', 1.5)
#
#     # Task
#     task = getattr(module, 'generate_tasks')
#
#     task_queue = Queue()
#     for t in list(task()):
#         task_queue.put(t)
#     config['task_queue'] = task_queue
#
#     # TODO: step setting
#     # TODO: processor setting
#
#     # scraper
#     scraper_callable = getattr(module, 'generate_scraper')
#
#     scrapers: List[Scraper] = []
#
#     # TODO: refact thread.
#     for i in range(config['thread']):
#         try:
#             scraper = scraper_callable()
#             assert isinstance(scraper, Scraper)
#             scrapers.append(scraper)
#         except Exception as e:
#             scraper = RequestScraper()
#             scraper.scraper_activate()
#             scrapers.append(scraper)
#
#     config['scrapers'] = scrapers
#
#     return config
