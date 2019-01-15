from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import base.core as core
from base.lib import Config
from base.Container import Container
from base.Conserve import Conserve
from base.scrapy_thread import threadTask
import queue
import scrapy_config
import time
from base.log import getLog

log = getLog()


def single_run(conf: Dict[str, str or List[str]]):
    config: Config = Config(conf)

    scraper, task = core.do_prepare(config.prepare, config.job)
    conserve = core.load_conserve(config.conserve, config.job)

    allow_processes = core.load_process(config.process, config.job)
    pipeline = core.build_process(allow_processes)

    # models = core.load_models(config.models, config.job)

    manager = core.register_manager(allow_model=config.models, job=config.job)
    schemes = core.load_scheme(config.schemes, config.job)

    current_conserve = core.build_conserve(conserve)
    # containers = core._register_containers(config.models, config.job, current_conserve)
    containers = core.register_containers(config.models, config.job, pipeline)

    core.scrapy(scheme_list=schemes, manager=manager, task=task[0], scraper=scraper)

    core.thread_conserve(manager=manager, containers=containers)

    # core.do_conserve(manager=manager, conserve=current_conserve)

    # end functions
    for container in containers:
        containers[container].dump()
    pipeline.end_task()
    # current_conserve.end_conserve()


def thread_run(conf: Dict[str, str or List[str]]):
    # config init
    config: Config = Config(conf)

    log.info("thread run!")
    log.info("config: {0}".format(str(conf)))

    # prepare
    current_prepare = core.load_prepare(config.prepare, config.job)
    tasks = current_prepare.get_tasks()

    # task init
    # q = queue.Queue()
    c = Container(timeout=10)
    for task in tasks:
        # FIXME task 对象转换
        c.add(task)
    log.info("task init! number: {0}".format(len(tasks)))

    log.info("init conserve")
    # conserve init
    conserve = core.load_conserve(config.conserve, config.job)
    current_conserve = core.build_conserve(conserve)
    log.info("conserve ready")

    allow_processes = core.load_process(config.process, config.job)
    pipeline = core.build_process(allow_processes)
    log.info("pipeline ready")

    # container init
    # containers = core._register_containers(config.models, config.job, current_conserve)
    containers = core.register_containers(config.models, config.job, pipeline)

    # TODO 一个对象 -> 一行

    thread_List = []


    for i in range(scrapy_config.Thread):
        t = threadTask(c, config, containers)
        thread_List.append(t)
        t.setDaemon(True)
        t.start()

    for i in thread_List:
        i.join()

    # TODO log
    log.info("thread end!")
    for container in containers:
        containers[container].dump()
    pipeline.end_task()

    from base.Container import pool
    pool.wait()
    # current_conserve.end_conserve()


if __name__ == '__main__':
    pass
