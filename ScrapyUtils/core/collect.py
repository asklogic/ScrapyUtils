import time
import os
from types import ModuleType
from typing import List, Callable

from os import path
from queue import Queue
from importlib import import_module
from urllib import parse
from concurrent.futures import ThreadPoolExecutor

from ScrapyUtils.components import Component, Step, StepSuit, ActionStep, ParseStep, Processor, Pipeline, ProcessorSuit
from ScrapyUtils.libs import Scraper, RequestScraper, Proxy, MultiProducer, Producer
from ScrapyUtils.log import common
from ScrapyUtils.log import basic

# global:
# *******************************************************************************

# components
processors_class: List[type(Step)] = None
steps_class: List[type(Step)] = None

# callable
tasks_callable: Callable = None
scraper_callable: Callable = None

config: dict = None

# ----------------------------------------------------------------------

tasks: Queue = Queue()
scrapers: List[Scraper] = None
proxy: Producer = None

# suits
step_suits: List[StepSuit] = None
processor_suit: ProcessorSuit = None

models_pipeline: Pipeline = None

# others
log = basic


# *******************************************************************************

def collect_scheme_preload(scheme: str):
    global tasks_callable, scraper_callable, steps_class, processors_class, config

    try:
        module = import_module(scheme)
        steps_class = module.steps_class
        processors_class = module.processors_class

        tasks_callable = module.tasks_callable
        scraper_callable = module.scraper_callable

        # ----------------------------------------------------------------------
        # config : dict
        config = module.config


    except Exception as e:
        log.exception('collect', e)
        # TODO: interrupt
        raise Exception('interrupt.')

    # ----------------------------------------------------------------------
    # global setting
    try:
        global_settings = import_module('settings')
        g_config, g_tasks_callable, g_scraper_callable = collect_settings(global_settings)

        if g_config.get('global_config'):
            log.info('enable global config.', 'System')

            for key, value in g_config.items():
                if not key.startswith('scheme'):
                    config[key] = value
            # config = g_config

        if g_config.get('global_task'):
            log.info('enable global tasks.', 'System')
            tasks_callable = g_tasks_callable

        if g_config.get('global_scraper'):
            log.info('enable global scraper.', 'System')
            scraper_callable = g_scraper_callable

    except ModuleNotFoundError as mnfe:
        log.info('no global setting.', 'System')
    except Exception as e:
        log.warning('load global settings failed', 'System')
        log.exception('System', e)


def collect_scheme_initial(**kwargs):
    global tasks_callable, scraper_callable, steps_class, processors_class, config

    global tasks, scrapers, proxy, config, step_suits, processor_suit, models_pipeline

    thread_num = config.get('thread')

    # ----------------------------------------------------------------------
    # task queue : tasks_callable
    tasks = Queue()
    for task in tasks_callable():
        tasks.put(task)

    # ----------------------------------------------------------------------
    # processor suits : List[ProcessorSuit]
    processor_suit = ProcessorSuit(processors_class, config)
    models_pipeline = Pipeline(processor_suit)

    # if kwargs.get('confirm'):
    #     input('Press any key to continue.')

    # ----------------------------------------------------------------------
    # scrapers* : list[Scraper]
    gen = _default_scraper(scraper_callable)
    scrapers = list_builder(gen, thread_num, timeout=30)

    # ----------------------------------------------------------------------
    # step suits : List[StepSuit]
    step_suits = [StepSuit(scrapers[i], steps_class) for i in range(thread_num)]

    # ----------------------------------------------------------------------
    # suit suit_start
    [x.suit_start() for x in step_suits]
    processor_suit.suit_start()

    # ----------------------------------------------------------------------
    # proxy : producer
    proxy = build_proxy(config)


def collect_scheme(scheme: str):
    """
    load scheme.
    get attr in __init__ and init global variable.
    """

    global steps_class, processors_class, config, scrapers, tasks, models_pipeline, proxy

    module = import_module(scheme)

    steps_class = module.steps
    processors_class = module.components

    # config
    config = module.config

    # ----------------------------------------------------------------------
    # scraper : scraper_callable
    scrapers = _default_scraper(module.scraper_callable)

    # ----------------------------------------------------------------------
    # task queue : tasks_callable
    tasks = Queue()
    for task in module.tasks_callable():
        tasks.put(task)

    # ----------------------------------------------------------------------
    # proxy : producer
    # TODO: proxy
    if config.get('proxy') and config.get('proxy_url'):
        url = config.get('proxy_url')
        thread = config.get('thread', 5)
        query_dict = config.get('query_dict', {})

        gen = proxy_generation(rebuild_url(url, query_dict))

        proxy = get_proxy_producer(gen, thread)

    # ----------------------------------------------------------------------
    # init pipeline
    models_pipeline = Pipeline(processors_class)


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

    # duplication
    current_steps = list(set(current_steps))

    # remove active
    current_steps = [x for x in current_steps if x.active]

    # sort
    current_steps.sort(key=lambda x: x.priority, reverse=True)
    return current_steps


def collect_processors(module: ModuleType) -> List[Processor]:
    """
    load processors
    """
    current_processor = _load_components(module, Processor)
    # remove active
    current_processor = [x for x in current_processor if x.active]

    # sort
    current_processor.sort(key=lambda x: x.priority, reverse=True)
    return current_processor


def collect_settings(module: ModuleType):
    """
    load setting.py as a dict.
    """
    current_config = {}

    # command settings
    current_config['keep_log'] = getattr(module, 'KEEP_LOG', False)

    # implicit settings
    current_config['scheme_path'] = path.dirname(module.__file__)

    # common setting
    current_config['thread'] = getattr(module, 'THREAD', 5)
    current_config['timeout'] = getattr(module, 'TIMEOUT', 1.5)

    # global setting
    current_config['global_config'] = getattr(module, 'GLOBAL_CONFIG', False)
    current_config['global_task'] = getattr(module, 'GLOBAL_TASK', False)
    current_config['global_scraper'] = getattr(module, 'GLOBAL_SCRAPER', False)

    # File setting
    # TODO: global
    current_config['file_folder'] = getattr(module, 'FILE_FOLDER', os.path.join(path.dirname(module.__file__), 'data'))
    current_config['file_name'] = getattr(module, 'FILE_NAME', str(int(time.time())))

    current_config['download_folder'] = getattr(module, 'DOWNLOAD_FOLDER',
                                                os.path.join(path.dirname(module.__file__), 'download'))

    # proxy
    current_config['proxy'] = getattr(module, 'PROXY', False)
    current_config['proxy_url'] = getattr(module, 'PROXY_URL', '')
    current_config['query_dict'] = getattr(module, 'PROXY_DICT', {})

    # Task
    tasks_callable = getattr(module, 'generate_tasks')
    assert callable(tasks_callable), "profile's generate_tasks must be callable."

    # scraper
    scraper_callable = getattr(module, 'generate_scraper')
    assert callable(scraper_callable), "profile's generate_scraper must be callable."

    return current_config, tasks_callable, scraper_callable


# utils
# ----------------------------------------------------------------------


default_flag = True


def _default_scraper(scraper_callable) -> Callable:
    """

    :param scraper_callable: The function from profile's generate_scraper.That should return a Scraper instance.
    :return: Scraper instance.
    """

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

    executor = ThreadPoolExecutor(number)

    futures = [executor.submit(inner) for x in range(number)]

    # method result will raise exception when timeout.
    [x.result(timeout) for x in futures]

    # TODO: exit executor.
    executor.shutdown(False)

    return res_list
