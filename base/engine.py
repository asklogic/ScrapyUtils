from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
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
    act.info("Target Prepare: " + prepare._name + str(prepare))
    act.info("Target Schemes list: " + str([x._name for x in prepare.schemeList]))

    model = core.initModel(target)
    act.info("Target Models: " + str([x._name for x in model]))

    processors = core.initProcessor(target)
    act.info("Target Process: " + str([x._name for x in processors]))

    time.sleep(1)

    scheme = [x() for x in prepare.schemeList]

    scraper = prepare.get_scraper()
    task = prepare.get_tasks()

    sys_hub, dump_hub = core.build_Hub(model, processors)

    sys_hub.activate()
    dump_hub.activate()

    core.scrapy(scheme, scraper, task[0], dump_hub)

    dump_hub.stop()
    sys_hub.stop()


def thread_run(target: str):
    # loading
    act.info("thread run")
    act.info("Target Job: " + target)

    prepare = core.initPrepare(target)
    act.info("Target Prepare: " + prepare._name + str(prepare))
    act.info("Target Schemes list: " + str([x._name for x in prepare.schemeList]))

    model = core.initModel(target)
    act.info("Target Models: " + str([x._name for x in model]))

    processors = core.initProcessor(target)
    act.info("Target Process: " + str([x._name for x in processors]))

    # set threading
    core.barrier = threading.Barrier(prepare.Thread)

    sys_hub, dump_hub = core.build_Hub(model, processors)

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
        t = core.ScrapyThread(sys_hub=sys_hub, dump_hub=dump_hub, prepare=prepare)
        thread_List.append(t)
        t.setDaemon(True)
        t.start()

    [t.join() for t in thread_List]
    sys_hub.stop()
    dump_hub.stop()


if __name__ == '__main__':
    pass
