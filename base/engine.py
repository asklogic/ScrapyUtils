from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import base.core as core
from base.lib import Config
from base.Container import ProxyContainer
from base.Conserve import Conserve
from base.scrapy_thread import threadTask
import queue
import scrapy_config


def single_run(conf: Dict[str, str or List[str]]):
    # job: str = conf.get("job")
    # allow: List[str] = conf.get("allow")
    # prepare: str = conf.get("prepare")
    # conserve: str = conf.get("conserve")
    # models: List[str] = conf.get("model")

    config: Config = core.load_conf(conf)


    scraper, task = core.do_prepare(config.prepare, config.job)
    manager = core.register_manager(config.models, config.job)
    schemes = core.load_scheme(config.schemes, config.job)
    current_conserve = core.load_conserve(config.conserve, config.job)
    current_conserve = current_conserve()
    current_conserve.start_conserve()

    core.scrapy(scheme_list=schemes, manager=manager, task=task[0], scraper=scraper)

    core.do_conserve(manager=manager, conserve=current_conserve)


def thread_run(conf: Dict[str, str or List[str]]):
    # job: str = conf.get("job")
    # allow: List[str] = conf.get("allow")
    # prepare: str = conf.get("prepare")
    # conserve: str = conf.get("conserve")
    # models: List[str] = conf.get("model")

    config: Config = core.load_conf(conf)

    current_prepare = core.load_prepare(config.prepare, config.job)
    tasks = current_prepare.get_tasks()
    q = queue.Queue()

    proxy_container = ProxyContainer(conserve=None, gather=50, supply=40)

    conserve: Conserve = core.load_conserve(config.conserve, config.job)()
    conserve.start_conserve()

    for task in tasks:
        q.put(task)

    for i in range(scrapy_config.Thread):
        t = threadTask(q, config, conserve, proxy_container)
        t.start()
