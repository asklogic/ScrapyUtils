from types import ModuleType
from typing import List, Callable

from queue import Queue
from importlib import import_module
from urllib import parse
from concurrent.futures import ThreadPoolExecutor

from base.components import Component, Step, StepSuit, ActionStep, ParseStep, Processor, Pipeline
from base.libs import Scraper, RequestScraper, ItemPool, Proxy, MultiProducer, Producer
from base.log import Wrapper

# global:
# *******************************************************************************
module = None

# component
processors = None
steps_class = None
scrapers = None

config = None

# property
tasks = Queue()
suits: List[StepSuit] = None
models_pipeline: Pipeline = None

# others
log = Wrapper
proxy: Producer = None


# *******************************************************************************

def collect_scheme_prepare(scheme: str):
    global steps_class, processors, config, module

    try:

        module = import_module(scheme)

        steps_class = module.steps_class
        processors = module.processors

        # ----------------------------------------------------------------------
        # config : dict
        config = module.config
    except Exception as e:
        log.exception('Collect Prepare', e)
        raise Exception('interrupt.')


def collect_scheme_initial():
    global module, tasks, scrapers, proxy, config, steps_class, suits, processors, models_pipeline

    try:

        thread_num = config.get('thread')

        # ----------------------------------------------------------------------
        # task queue : tasks_callable
        tasks = Queue()
        for task in module.tasks_callable():
            tasks.put(task)

        # ----------------------------------------------------------------------
        # scrapers* : list[Scraper]
        gen = _default_scraper(module.scraper_callable)
        scrapers = list_builder(gen, thread_num, timeout=30)

        # ----------------------------------------------------------------------
        # step* : List[step]
        steps_list = list_builder(lambda: [x() for x in steps_class], thread_num, timeout=10)

        # ----------------------------------------------------------------------
        # suits : List[StepSuit]
        suits = [StepSuit(steps_list[i], scrapers[i]) for i in range(thread_num)]

        # ----------------------------------------------------------------------
        # proxy : producer
        proxy = build_proxy(config)

        # ----------------------------------------------------------------------
        # init pipeline
        models_pipeline = Pipeline(processors)
    except Exception as e:
        log.exception('Collect Initial', e)
        raise Exception('interrupt.')


def collect_scheme(scheme: str):
    """
    load scheme.
    get attr in __init__ and init global variable.
    """

    global steps_class, processors, config, scrapers, tasks, models_pipeline, proxy

    module = import_module(scheme)

    steps_class = module.steps
    processors = module.processors

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
    models_pipeline = Pipeline(processors)


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
    load steps
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


def collect_profile(module: ModuleType):
    """
    load profile
    """
    current_config = {}

    # common setting
    current_config['thread'] = getattr(module, 'THREAD', 5)
    current_config['timeout'] = getattr(module, 'TIMEOUT', 1.5)

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

def _default_scraper(scraper_callable) -> Callable:
    """

    :param scraper_callable: The function from profile's generate_scraper.That should return a Scraper instance.
    :return: Scraper instance.
    """

    def inner():
        try:
            current_scraper = scraper_callable()
            assert isinstance(current_scraper, Scraper)
            # current_scraper.scraper_activate()
        except Exception as e:
            # log.exception('Scraper', e)
            log.warning('able default RequestScraper.')
            current_scraper = RequestScraper()
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
