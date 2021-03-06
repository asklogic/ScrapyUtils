from .collect import scheme_preload, scheme_initial, scheme_start, scheme_exit, initial_configure
from . import collect


def set_processors(processors):
    """
    Args:
        processors:
    """
    collect.processors_class = processors


def set_steps(steps):
    """
    Args:
        steps:
    """
    collect.steps_class = steps


def set_scraper_callable(scraper_callable):
    """
    Args:
        scraper_callable:
    """
    collect.scraper_callable = scraper_callable


def set_task_callable(task_callable):
    """
    Args:
        task_callable:
    """
    collect.tasks_callable = task_callable


def get_steps():
    from .collect import steps_class
    return steps_class


def get_processors():
    from .collect import processors_class
    return processors_class


def get_pipeline():
    from .collect import models_pipeline
    return models_pipeline


def get_config() -> dict:
    from .collect import config
    return config


def get_tasks():
    from .collect import tasks
    return tasks


def get_scraper():
    from .collect import scrapers
    return scrapers


def get_proxy():
    from .collect import proxy
    return proxy


def get_suits():
    from .collect import step_suits
    return step_suits
