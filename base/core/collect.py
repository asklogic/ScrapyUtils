from types import ModuleType
from typing import List, Callable

from queue import Queue
from importlib import import_module

from base.components import Component, Step, ActionStep, ParseStep, Processor, Pipeline
from base.libs import Scraper, RequestScraper
from base.log import Wrapper

# global:
# *******************************************************************************
# component
steps = None
processors = None
config = None

# callable
scraper = None

# pipeline's
tasks = Queue()
models_pipeline: Pipeline = None

# others
log = Wrapper
proxy = Queue()


# *******************************************************************************
def collect_scheme(scheme: str):
    """
    load scheme.
    get attr in __init__ and init global variable.
    :return: None
    """

    global steps, processors, config, scraper, tasks, models_pipeline

    module = import_module(scheme)

    steps = module.steps
    processors = module.processors
    config = module.config

    scraper = _default_scraper(module.scraper_callable)
    for task in module.tasks_callable():
        tasks.put(task)

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

    # common setting(
    current_config['thread'] = getattr(module, 'THREAD', 5)
    current_config['timeout'] = getattr(module, 'TIMEOUT', 1.5)

    # Task
    tasks_callable = getattr(module, 'generate_tasks')
    assert callable(tasks_callable), "profile's generate_tasks must be callable."

    # scraper
    scraper_callable = getattr(module, 'generate_scraper')
    assert callable(scraper_callable), "profile's generate_scraper must be callable."

    return current_config, tasks_callable, scraper_callable


def _default_scraper(scraper_callable) -> Scraper:
    """

    :param scraper_callable: The function from profile's generate_scraper.That should return a Scraper instance.
    :return: Scraper instance.
    """

    def inner():
        try:
            scraper = scraper_callable()
            assert scraper
            scraper.scraper_activate()
        except Exception as e:
            # log.exception('Scraper', e)
            pass
        else:
            log.warning('able default RequestScraper.')
            scraper = RequestScraper()
        return scraper

    return inner
