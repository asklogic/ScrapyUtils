from types import ModuleType
from typing import List, Callable

from queue import Queue
from importlib import import_module
from urllib import parse

from base.components import Component, Step, ActionStep, ParseStep, Processor, Pipeline
from base.libs import Scraper, RequestScraper, ItemPool, Proxy
from base.log import Wrapper

# global:
# *******************************************************************************
# component
steps = None
processors = None
config = None

# callable
scraper_generate = None

# pipeline's
tasks = Queue()
models_pipeline: Pipeline = None

# others
log = Wrapper
proxy: ItemPool = None


# *******************************************************************************
def collect_scheme(scheme: str):
    """
    load scheme.
    get attr in __init__ and init global variable.
    """

    global steps, processors, config, scraper_generate, tasks, models_pipeline, proxy

    module = import_module(scheme)

    steps = module.steps
    processors = module.processors

    # config
    config = module.config

    # ----------------------------------------------------------------------
    # scraper : scraper_callable
    scraper_generate = _default_scraper(module.scraper_callable)

    # ----------------------------------------------------------------------
    # task queue : tasks_callable
    tasks = Queue()
    for task in module.tasks_callable():
        tasks.put(task)

    # ----------------------------------------------------------------------
    # proxy : producer
    # TODO: proxy

    # if config.get('proxy') and config.get('proxy_url'):
    #     limit = config['thread']
    #     generate = _get_proxy_generation(config.get('proxy_url'))
    #
    #     pool = ItemPool(generate, limit=limit)
    #     pool.start()
    #     proxy = pool

    # init
    models_pipeline = Pipeline(processors)


def _load_components(module: ModuleType, component: type(Component)):
    """
    Load the specified subclass from module
    :param module: the module
    :param component: the super class(type)
    :return: subclass list
    """
    components: List[Component] = list()
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
def _get_proxy_generation(url):
    res = parse.urlparse(url)

    query = parse.parse_qs(res.query)

    r = RequestScraper()
    r.scraper_activate()

    def proxy_generation(number):
        query['qty'] = number
        query_str = parse.urlencode(query, doseq=True)
        res._replace(query=query_str)

        current_url = res.geturl()

        content = r.get(current_url)

        proxy_list = content.split('\r\n')

        for proxy_info in proxy_list:
            ip, port = proxy_info.split(':')
            proxy = Proxy(ip=ip, port=port)

            assert ip
            assert port

            yield proxy

    return proxy_generation
