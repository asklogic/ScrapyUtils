from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
from types import *
from base.lib import Config

import queue
import scrapy_config
import time
import threading

from base.log import status, act
from base.Process import Pipeline
from base import core


def single_run(target: str):
    act.info("single run")
    act.info("Target Job: " + target)

    prepare = core.initPrepare(target)
    prepare.setting['target'] = target

    act.info("Target Prepare: " + prepare._name + str(prepare))
    act.info("Target Schemes list: " + str([x._name for x in prepare.schemeList]))

    model = core.initModel(target)
    act.info("Target Models: " + str([x._name for x in model]))

    if not prepare.processorList:
        processors = core.initProcessor(target)
    else:
        processors = prepare.processorList
    act.info("Target Process: " + str([x._name for x in processors]))

    time.sleep(1)

    # TODO init
    schemes = [x() for x in prepare.schemeList]
    context = {}
    for scheme in schemes:
        scheme.context = context

    scraper = prepare.get_scraper()
    task = prepare.get_tasks()
    # TODO load taks
    if task[0].param:
        if type(task[0].param) == dict:
            for key, item in task[0].param.items():
                schemes[0].context[key] = item

    sys_hub, dump_hub = core.build_hub(model, processors, prepare.setting)

    sys_hub.activate()
    dump_hub.activate()

    core.scrapy(schemes, scraper, task[0], dump_hub, sys_hub)

    scraper.quit()
    dump_hub.stop()
    sys_hub.stop()


def _thread_run(target: str):
    # loading
    act.info("thread run")
    act.info("Target Job: " + target)

    prepare = core.initPrepare(target)
    prepare.setting['target'] = target
    act.info("Target Prepare: " + prepare._name + str(prepare))
    act.info("Target Schemes list: " + str([x._name for x in prepare.schemeList]))

    model = core.initModel(target)
    act.info("Target Models: " + str([x._name for x in model]))

    if not prepare.processorList:
        processors = core.initProcessor(target)
    else:
        processors = prepare.processorList
    act.info("Target Process: " + str([x._name for x in processors]))

    # set threading
    core.barrier = threading.Barrier(prepare.Thread)

    sys_hub, dump_hub = core.build_hub(model, processors, prepare.setting)

    # setting
    # proxy
    if not prepare.ProxyAble:
        sys_hub.remove_pipeline("ProxyModel")
    else:
        core.temp_appendProxy(sys_hub, prepare.Thread)

    # init hub
    sys_hub.activate()
    dump_hub.activate()

    #
    # fixme
    # append init task
    for t in core.generate_task(prepare):
        sys_hub.save(t)

    thread_List = []

    for i in range(prepare.Thread):
        t = core._ScrapyThread(sys_hub=sys_hub, dump_hub=dump_hub, prepare=prepare)
        thread_List.append(t)
        t.setDaemon(True)
        t.start()

    [t.join() for t in thread_List]
    sys_hub.stop()
    dump_hub.stop()


def thread_run(target_name: str):
    # step 1: load files
    modules: List[ModuleType] = core.load_files(target_name)

    # step 2: load components
    components = core.load_components(modules, target_name=target_name)
    prepare, schemes, models, processors = components

    act.info("thread run")
    act.info("Target Job: " + target_name)
    act.info("Target Prepare: " + prepare._name + str(prepare))
    act.info("Target Schemes list: " + str([x._name for x in prepare.schemeList]))
    act.info("Target Models: " + str([x._name for x in models]))
    act.info("Target Process: " + str([x._name for x in processors]))

    thread = prepare.Thread
    # step 3.1: build thread scraper list
    scraper_list, tasks = core.build_thread_prepare(prepare, thread)
    act.info("Detect Task number : " + str(len(tasks)))
    act.info("Build Scraper finish. Thread number: " + str(len(scraper_list)))

    # step 3.2: build thread scheme list ( context
    schemes_list = core.build_thread_schemes(schemes, thread)

    # step 3.3: build hub
    sys_hub, dump_hub = core.build_hub(models, processors, prepare.setting)
    # temp
    # TODO
    if not prepare.ProxyAble:
        sys_hub.remove_pipeline("ProxyModel")
        act.info("Proxy Pipeline shutdown")

    else:
        core.temp_appendProxy(sys_hub, prepare.Thread)
        act.info("Proxy Pipeline startup")

    sys_hub.activate()
    dump_hub.activate()

    for task in tasks:
        sys_hub.save(task)

    # step 4: init thread
    core.barrier = threading.Barrier(prepare.Thread)

    thread_List = []

    act.info("run thread")

    for i in range(prepare.Thread):
        t = core.ScrapyThread(sys_hub=sys_hub, dump_hub=dump_hub, prepare=prepare, schemes=schemes_list[i],
                              scraper=scraper_list[i])
        thread_List.append(t)
        t.setDaemon(True)
        t.start()

    [t.join() for t in thread_List]

    # step 5: run command

    # step 6: exit

    sys_hub.stop()
    dump_hub.stop()


if __name__ == '__main__':
    pass
