from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
from base.lib import Config

import queue
import scrapy_config
import time
from base.log import status, act
from base.Process import Pipeline
from base import core

def single_run(config: Config):
    act.info("single run")
    act.info("Target Job:" + config.job)
    act.info("Target Prepare:" + config.prepare)
    act.info("Target Schemes:" + str(config.schemes))
    act.info("Target Models:" + str(config.models))
    act.info("Target Process:" + str(config.process))
    act.info("Target Setting:" + str(config.project))

    time.sleep(1)

    prepare = core.load_prepare(config)

    processor = core.load_processor(config)

    model = core.load_model(config)

    scheme = core.load_scheme(config)

    scraper, task = core.build_prepare(prepare)

    sys_hub, dump_hub = core.build_Hub(model, processor)
    sys_hub.activate()
    dump_hub.activate()

    # if config.project.get("Proxy_Able"):
    #     core.temp_appendProxy(sys_hub)

    core.scrapy(scheme, scraper, task[0], dump_hub)

    dump_hub.stop()
    sys_hub.stop()



def thread_run(config: Config):
    act.info("thread run")
    act.info("Target Job:" + config.job)
    act.info("Target Prepare:" + config.prepare)
    act.info("Target Schemes:" + str(config.schemes))
    act.info("Target Models:" + str(config.models))
    act.info("Target Process:" + str(config.process))
    act.info("Target Setting:" + str(config.project))


    prepare = core.load_prepare(config)

    processor = core.load_processor(config)

    model = core.load_model(config)

    sys_hub, dump_hub = core.build_Hub(model, processor)

    if config.project.get("Proxy_Able"):
        core.temp_appendProxy(sys_hub)

    sys_hub.activate()
    dump_hub.activate()



    for t in core.generate_task(prepare):
        sys_hub.save(t)

    thread_List = []

    for i in range(scrapy_config.Thread):
        t = core.ScrapyThread(sys_hub=sys_hub, dump_hub=dump_hub, config=config)
        thread_List.append(t)
        t.setDaemon(True)
        t.start()

    [t.join() for t in thread_List]
    sys_hub.stop()
    dump_hub.stop()



if __name__ == '__main__':
    pass
