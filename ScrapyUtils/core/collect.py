import time
import os
from types import ModuleType
from typing import List, Callable

from os import path
from queue import Queue
from importlib import import_module
from urllib import parse
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from ScrapyUtils.components import Component, Step, StepSuit, ActionStep, ParseStep, Processor, Pipeline, ProcessorSuit
from ScrapyUtils.libs import Scraper, RequestScraper, Proxy, MultiProducer, Producer
from ScrapyUtils.log import common
from ScrapyUtils.log import basic

from . import configure

# global:
# *******************************************************************************

# components
processors_class: List[type(Step)] = []
steps_class: List[type(Step)] = []

# callable
tasks_callable: Callable = None
scraper_callable: Callable = None

config: dict = None

# ----------------------------------------------------------------------

tasks: Queue = Queue()
scrapers: List[Scraper] = []
proxy: Producer = None

# suits
step_suits: List[StepSuit] = []
processor_suit: ProcessorSuit = None

models_pipeline: Pipeline = None

# others
log = basic


# *******************************************************************************


def initial_configure(settings_module: ModuleType):
    global tasks_callable, scraper_callable

    # globals()['SCHEME_PATH'] = path.dirname(settings_module.__file__)
    configure.FILE_FOLDER_PATH = path.join(path.dirname(settings_module.__file__), 'data')

    configure.SCHEME_PATH = path.dirname(settings_module.__file__)

    # initial download configure items
    configure.DOWNLOAD_FOLDER_PATH = path.join(path.dirname(settings_module.__file__), 'download')
    configure.DOWNLOAD_SUFFIX = 'html'

    for key in configure.registered_keys:
        if hasattr(settings_module, key):
            # globals()[key] = getattr(settings_module, key)
            setattr(configure, key, getattr(settings_module, key))

    # tasks
    tasks_callable = getattr(settings_module, 'generate_tasks')
    assert callable(tasks_callable), "profile's generate_tasks must be callable."

    # scraper
    scraper_callable = getattr(settings_module, 'generate_scraper')
    assert callable(scraper_callable), "profile's generate_scraper must be callable."


# def collect_scheme_preload(scheme: str):
#     global tasks_callable, scraper_callable, steps_class, processors_class, config
#
#     try:
#         module = import_module(scheme)
#         steps_class = module.steps_class
#         processors_class = module.processors_class
#
#         tasks_callable = module.tasks_callable
#         scraper_callable = module.scraper_callable
#
#         # ----------------------------------------------------------------------
#         # config : dict
#         config = module.config
#
#
#     except Exception as e:
#         # log.error()
#         log.exception(e, line=3)
#         return False
#
#     # ----------------------------------------------------------------------
#     # global setting
#     try:
#         global_settings = import_module('settings')
#         g_config, g_tasks_callable, g_scraper_callable = collect_settings(global_settings)
#
#         if g_config.get('global_config'):
#             log.info('enable global config.', 'System')
#
#             for key, value in g_config.items():
#                 if not key.startswith('scheme'):
#                     config[key] = value
#             # config = g_config
#
#         if g_config.get('global_task'):
#             log.info('enable global tasks.', 'System')
#             tasks_callable = g_tasks_callable
#
#         if g_config.get('global_scraper'):
#             log.info('enable global scraper.', 'System')
#             scraper_callable = g_scraper_callable
#
#     except ModuleNotFoundError as mnfe:
#         log.info('no global setting.', 'System')
#     except Exception as e:
#         log.warning('load global settings failed', 'System')
#         log.exception(e, line=3)
#
#     return True


def scheme_preload(scheme: str):
    # w = Watcher(start_content='scheme preloading')
    try:
        module = import_module(scheme)

        global steps_class, processors_class

        steps_class = module.steps_class
        processors_class = module.processors_class
    except Exception as e:
        log.exception(e)
        raise Exception('Failed in scheme preload.')
    # finally:
    #     w.exit_watch()


def collect_scheme_initial(command_kwargs: dict = None):
    global tasks_callable, scraper_callable, steps_class, processors_class, config
    global tasks, scrapers, proxy, config, step_suits, processor_suit, models_pipeline

    log.info('Scheme initialing...')

    # ----------------------------------------------------------------------
    # task queue : tasks_callable
    tasks = Queue()
    for task in tasks_callable():
        tasks.put(task)

    # ----------------------------------------------------------------------
    # processor suits : List[ProcessorSuit]
    processor_suit = ProcessorSuit(processors_class, command_kwargs)
    models_pipeline = Pipeline(processor_suit)

    # if kwargs.get('confirm'):
    #     input('Press any key to continue.')

    # ----------------------------------------------------------------------
    # scrapers* : list[Scraper]
    gen = _default_scraper(scraper_callable)
    scrapers = list_builder(gen, configure.THREAD, timeout=30)

    # ----------------------------------------------------------------------
    # step suits : List[StepSuit]
    step_suits = [StepSuit(scrapers[i], steps_class) for i in range(configure.THREAD)]

    # ----------------------------------------------------------------------
    # suit suit_start
    [x.suit_start() for x in step_suits]
    processor_suit.suit_start()

    # ----------------------------------------------------------------------
    # proxy : producer
    # proxy = build_proxy(config)


def scheme_initial(command_kwargs={}):
    global step_suits, processor_suit

    w = Watcher(start_content='scheme initialing')

    time.sleep(1)

    # build suits
    step_suits = [StepSuit(steps=steps_class) for i in range(configure.THREAD)]
    processor_suit = ProcessorSuit(processors_class, command_kwargs)

    w.exit_watch()


def scheme_start():
    global scrapers, tasks, models_pipeline

    w = Watcher(start_content='scheme starting')

    # ----------------------------------------------------------------------
    # generate queue.
    tasks = Queue()
    for task in tasks_callable():
        tasks.put(task)

    # ----------------------------------------------------------------------
    # generate scrapers
    gen = _default_scraper(scraper_callable)
    scrapers = list_builder(gen, configure.THREAD, timeout=configure.SCRAPER_TIMEOUT)

    for index in range(configure.THREAD):
        step_suits[index]._scraper = scrapers[index]

    # ----------------------------------------------------------------------
    # start models pipeline.
    models_pipeline = Pipeline(processor_suit)

    # ----------------------------------------------------------------------
    # suit suit_start
    for step_suit in step_suits:
        step_suit.suit_start()
    # [step_suit.suit_start() for step_suit in step_suits]

    processor_suit.suit_start()

    w.exit_watch()


def scheme_exit():
    # ----------------------------------------------------------------------
    # suit - suit_quit

    w = Watcher(start_content='scheme exiting')

    processor_suit.suit_exit()

    for step_suit in step_suits:
        step_suit.suit_exit()

    models_pipeline.exit()

    w.exit_watch()

    # ----------------------------------------------------------------------
    # scrapers - scraper_quit
    # for scraper in scrapers:
    #     scraper.scraper_quit()


# abort
# def collect_scheme(scheme: str):
#     """
#     load scheme.
#     get attr in __init__ and init global variable.
#     """
#
#     global steps_class, processors_class, config, scrapers, tasks, models_pipeline, proxy
#
#     module = import_module(scheme)
#
#     steps_class = module.steps
#     processors_class = module.components
#
#     # config
#     config = module.config
#
#     # ----------------------------------------------------------------------
#     # scraper : scraper_callable
#     scrapers = _default_scraper(module.scraper_callable)
#
#     # ----------------------------------------------------------------------
#     # task queue : tasks_callable
#     tasks = Queue()
#     for task in module.tasks_callable():
#         tasks.put(task)
#
#     # ----------------------------------------------------------------------
#     # proxy : producer
#     # TODO: proxy
#     if config.get('proxy') and config.get('proxy_url'):
#         url = config.get('proxy_url')
#         thread = config.get('thread', 5)
#         query_dict = config.get('query_dict', {})
#
#         gen = proxy_generation(rebuild_url(url, query_dict))
#
#         proxy = get_proxy_producer(gen, thread)
#
#     # ----------------------------------------------------------------------
#     # init pipeline
#     models_pipeline = Pipeline(processors_class)


def _load_components(module: ModuleType, component: type(Component)):
    """
    Load the specified subclass from module
    :param module: the module
    :param component: the super class(type)
    :return: subclass list
    """
    components: List[Component] = []
    for attr in dir(module):
        attribute = getattr(module, attr)
        # 短路判断类
        if isinstance(attribute, type) and issubclass(attribute, component) and attribute is not component:
            components.append(attribute)
    return components


def collect_steps(*modules: ModuleType) -> List[Step]:
    """
    load scheme's steps
    """
    current_steps = list()
    for module in modules:
        current_steps.extend(_load_components(module, ActionStep))
        current_steps.extend(_load_components(module, ParseStep))

    # duplication steps
    current_steps = list(set(current_steps))

    # remove inactive steps
    current_steps = [x for x in current_steps if x.active]

    # sort by priority
    current_steps.sort(key=lambda x: x.priority, reverse=True)
    return current_steps


def collect_processors(module: ModuleType) -> List[Processor]:
    """
    load processors
    """
    current_processor = _load_components(module, Processor)

    # remove inactive processors
    current_processor = [x for x in current_processor if x.active]

    # sort by priority
    current_processor.sort(key=lambda x: x.priority, reverse=True)
    return current_processor


# def collect_settings(module: ModuleType):
#     """
#     load setting.py as a dict.
#     """
#     current_config = {}
#
#     # command settings
#     current_config['keep_log'] = getattr(module, 'KEEP_LOG', True)
#
#     # implicit settings
#     current_config['scheme_path'] = path.dirname(module.__file__)
#
#     # common setting
#     current_config['thread'] = getattr(module, 'THREAD', 5)
#     current_config['timeout'] = getattr(module, 'TIMEOUT', 1.5)
#
#     # global setting
#     current_config['global_config'] = getattr(module, 'GLOBAL_CONFIG', False)
#     current_config['global_task'] = getattr(module, 'GLOBAL_TASK', False)
#     current_config['global_scraper'] = getattr(module, 'GLOBAL_SCRAPER', False)
#
#     # File setting
#     # TODO: global
#     current_config['file_folder'] = getattr(module, 'FILE_FOLDER', os.path.join(path.dirname(module.__file__), 'data'))
#     current_config['file_name'] = getattr(module, 'FILE_NAME', str(int(time.time())))
#
#     # download settings
#     # TODO: Abort download_folder? Set download path manually.
#     current_config['download_folder'] = getattr(module, 'DOWNLOAD_FOLDER',
#                                                 os.path.join(path.dirname(module.__file__), 'download'))
#     current_config['download_suffix'] = getattr(module, 'DOWNLOAD_SUFFIX', 'html')
#     current_config['download_path'] = getattr(module, 'DOWNLOAD_PATH', None)
#
#     # proxy
#     current_config['proxy'] = getattr(module, 'PROXY', False)
#     current_config['proxy_url'] = getattr(module, 'PROXY_URL', '')
#     current_config['query_dict'] = getattr(module, 'PROXY_DICT', {})
#
#     # task
#     tasks_callable = getattr(module, 'generate_tasks')
#     assert callable(tasks_callable), "profile's generate_tasks must be callable."
#
#     # scraper
#     scraper_callable = getattr(module, 'generate_scraper')
#     assert callable(scraper_callable), "profile's generate_scraper must be callable."
#
#     return current_config, tasks_callable, scraper_callable


# utils
# ----------------------------------------------------------------------


default_flag = True


def _default_scraper(scraper_callable) -> Callable:
    def inner():
        current_scraper = None
        global default_flag
        try:
            current_scraper = scraper_callable()
            assert isinstance(current_scraper, Scraper)
        except Exception as e:
            current_scraper = RequestScraper()
            if default_flag:
                # TODO: wtf is that?
                # log.exception('Scraper', e)
                # log.warning('able default RequestScraper.', 'system')
                log.warning('able default RequestScraper.')
                default_flag = False
        finally:
            if not current_scraper.activated:
                current_scraper.scraper_activate()

        return current_scraper

    return inner


# ----------------------------------------------------------------------
# TODO: proxy


def rebuild_url(url: str, query_dict: dict):
    # TODO: assert
    assert type(url) is str, 'type'
    assert type(query_dict) is dict, 'type'

    res = parse.urlparse(url)

    ori_query_dict = parse.parse_qs(res.query)

    ori_query_dict.update(query_dict)

    query_str = parse.urlencode(ori_query_dict, doseq=True)

    # res._replace(query=ori_query_dict)

    return res._replace(query=query_str).geturl()


def proxy_generation(url):
    """
    url from profile.
    """

    r = RequestScraper()
    r.scraper_activate()

    def proxy_generation():
        content = r.get(url)

        proxy_list = content.split('\r\n')

        for proxy_info in proxy_list:
            ip, port = proxy_info.split(':')
            proxy = Proxy(ip=ip, port=port)

            assert ip
            assert port

            yield proxy

    return proxy_generation


def get_proxy_producer(func, thread, delay=1.1):
    class ProxyProducer(MultiProducer):

        def producing(self, increment):
            log.info('get proxy', 'Proxy')
            return func()

    producer = ProxyProducer(queue=Queue(thread + 1), increment=thread + 1, delay=delay)
    return producer


def build_proxy(config: dict) -> Producer:
    if config.get('proxy') and config.get('proxy_url'):
        url = config.get('proxy_url')
        thread = config.get('thread', 5)
        query_dict = config.get('query_dict', {})

        gen = proxy_generation(rebuild_url(url, query_dict))

        proxy = get_proxy_producer(gen, thread)
        return proxy


def list_builder(invoker, number, timeout=10):
    res_list = []

    def inner():
        res = invoker()
        res_list.append(res)

    # executor = ThreadPoolExecutor(number)
    # futures = [executor.submit(inner) for x in range(number)]
    # method result will raise exception when timeout.
    # [x.result(timeout) for x in futures]
    # TODO: exit executor.
    # executor.shutdown(False)

    # log.info(f'Thread build ({number}). building... ')
    with ThreadPoolExecutor(number) as executor:
        futures = [executor.submit(inner) for x in range(number)]
        [x.result(timeout) for x in futures]

    # log.info('Thread build done.')

    return res_list


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
                 # output_instance=print,
                 daemon=True) -> None:
        super().__init__(daemon=daemon)

        self.exit_flag = True
        self.timeout = timeout
        self.start_content = start_content
        self.end_content = end_content
        self.delay = delay

        # self.output_instance = output_instance

        self.start()
        self.current_time = time.time()

    def exit_watch(self, spend=False):
        self.exit_flag = False
        spend_time = time.time() - self.current_time

        self.join()
        if spend:
            print('spend time:', spend_time)
