from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import base.core as core
from base.lib import Config
from base.Container import Container
from base.Conserve import Conserve
from base.scrapy_thread import threadTask
import queue
import scrapy_config
import time
from base.log import status, act
from base.Process import Pipeline


def single_run(conf: Dict[str, str or List[str]]):
    config: Config = Config(conf)
    act.info("single task run. Target: " + config.job)

    scraper, task = core.do_prepare(config)

    processes = core.load_process(config)
    pipeline = Pipeline(processes, config)

    manager = core.register_manager(config)
    schemes = core.load_scheme(config.schemes, config.job)

    containers = core.register_containers(config, pipeline)

    act.info("start scraping!")

    core.scrapy(scheme_list=schemes, manager=manager, task=task[0], scraper=scraper)

    core.thread_conserve(manager=manager, containers=containers)

    # end functions
    core.finish(containers, pipeline)


def thread_run(conf: Dict[str, str or List[str]]):
    # config init
    config: Config = Config(conf)

    log.info("thread run!")
    log.info("config: {0}".format(str(conf)))

    # prepare
    current_prepare = core.load_prepare(config.prepare, config.job)
    tasks = current_prepare.get_tasks()

    c = Container(timeout=10)
    for task in tasks:
        # FIXME task 对象转换
        c.add(task)
    log.info("task init! number: {0}".format(len(tasks)))

    # log.info("init conserve")
    # conserve init
    # conserve = core.load_conserve(config.conserve, config.job)
    # current_conserve = core.build_conserve(conserve)
    # log.info("conserve ready")

    processes = core.load_process(config)
    pipeline = Pipeline(processes, config=config)

    log.info("pipeline ready")

    # container init
    # containers = core._register_containers(config.models, config.job, current_conserve)
    containers = core.register_containers(config, pipeline)

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

    core.finish(containers, pipeline)
    log.info("thread end!")

    # current_conserve.end_conserve()


if __name__ == '__main__':
    pass
