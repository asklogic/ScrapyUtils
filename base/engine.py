import time
import threading

from base.log import logger
from base import core


def single_run(target_name):
    components = core.load_components(target_name)

    prepare, schemes, models, processors = components

    logger.info("single run")
    logger.info("Target Job: " + target_name)
    logger.info("Target Prepare: " + prepare._name + str(prepare))
    logger.info("Target Schemes list: " + str([x._name for x in prepare.schemeList]))
    logger.info("Target Models: " + str([x._name for x in models]))
    logger.info("Target Process: " + str([x._name for x in processors]))

    # step 3.1: build single scraper
    scraper, tasks = core.build_prepare(prepare)

    # step 3.2: build single schemes
    schemes = core.build_schemes(schemes)

    # step 3.3: build context
    current_task = tasks[0]
    core.load_context(current_task, schemes)

    # step 3.4: build hub
    sys_hub, dump_hub = core.build_hub(models, processors, prepare.setting)

    sys_hub.scraper_activate()
    dump_hub.scraper_activate()

    # step 4: Scrapy
    core.scrapy(schemes, scraper, current_task, dump_hub, sys_hub)

    # step 5: exit
    scraper.quit()
    dump_hub.stop()
    sys_hub.stop()


def thread_run(target_name: str):
    setting = core.build_setting(target_name)

    scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)
    schemes = core.build_thread_schemes(setting.CurrentSchemeList, setting.Thread)

    sys_hub, dump_hub = core.build_hub(setting=setting)

    logger.info("thread run")
    logger.info("Target Job: " + target_name)
    logger.info("Target Prepare: " + setting.CurrentPrepare._name + str(setting.CurrentPrepare))
    logger.info("Target Schemes list: " + str([x._name for x in setting.CurrentSchemeList]))
    logger.info("Target Models: " + str([x._name for x in setting.CurrentModels]))
    logger.info("Target Process: " + str([x._name for x in setting.CurrentProcessorsList]))

    logger.info("Detect Task number : " + str(len(tasks)))
    logger.info("Build Scraper finish. Thread number: " + str(setting.Thread))

    sys_hub.scraper_activate()
    dump_hub.scraper_activate()

    for task in tasks:
        sys_hub.save(task)

    thread_List = []
    for i in range(setting.Thread):
        t = core.ScrapyThread(sys_hub, dump_hub, schemes[i], scrapers[i], setting)
        thread_List.append(t)
        t.setDaemon(True)
        t.start()

    [t.join() for t in thread_List]
    sys_hub.stop(True)
    dump_hub.stop(True)

    [x.quit() for x in scrapers]


if __name__ == '__main__':
    pass
