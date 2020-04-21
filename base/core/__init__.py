from base.core.collect import collect_scheme, collect_scheme_initial, collect_scheme_prepare


def get_steps():
    from .collect import steps_class
    return steps_class


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
