from typing import *

from queue import Empty
import threading
import time

from base import core
from base.components import *
from base.libs import *
from base.hub import *
from base.command import Command

lock = threading.Lock()


class ScrapyThread(threading.Thread):

    def __init__(self, sys_hub: Hub, dump_hub: Hub, schemes: List[Scheme], scraper: Scraper, setting: Setting, log):
        threading.Thread.__init__(self)
        super(ScrapyThread, self).__init__()

        self.sys: Hub = sys_hub
        self.dump: Hub = dump_hub
        self.scraper: Scraper = scraper
        self.schemes: List[Scheme] = schemes

        self.setting: Setting = setting

        # todo
        self.current_task = None
        self.cmd_status = 1
        self.log = log

        # print('id ', id(self.schemes))
        # print('context 0 id ', id(self.schemes[0].context))
        # print('context 1 id ', id(self.schemes[1].context))

    def run(self) -> None:
        while self.cmd_status > 0 and self._get_task():
            task = self.current_task
            core.load_context(task, self.schemes)

            res = core.scrapy(self.schemes, self.scraper, task, self.dump, self.sys)
            if res:
                self.log("success. Task url:{} param {} count - {}".format(task.url, task.param, task.count))
            elif task.count < self.setting.FailedRetry:
                # reset
                self._reset()

                # sleep
                time.sleep(self.setting.FailedBlock)
                # status.info("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))

                # back to sys
                task.count = task.count + 1
                self.sys.save(task)
            else:
                time.sleep(self.setting.FailedBlock)
                self.log("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))

        if self.cmd_status is 1:
            self.log('thread named: %s finish!' % self.getName())
            self.cmd_status = 0
        elif self.cmd_status is -1:
            self.log('thread named: %s aborted!' % self.getName())
        elif self.cmd_status is 0:
            self.log('thread named: %s has already run!' % self.getName())

    def _get_task(self):
        self.current_task = None
        try:
            task = self.sys.pop('TaskModel')
            self.current_task = task
            return True
        except Empty as e:
            return False

    def _reset(self):
        self.scraper.clear_session()
        if self.setting.ProxyAble:
            proxy_model = self.sys.pop("ProxyModel")
            self.scraper.set_proxy((proxy_model.ip, proxy_model.port))

        # fixme
        for scheme in self.schemes:
            scheme.context.clear()

    def _sync(self, delay: int = 0):
        lock.acquire()
        if delay:
            time.sleep(delay)
        else:
            time.sleep(0.5)
        lock.release()

    def cmd_stop(self):
        self.cmd_status = -1


class Thread(Command):
    require_target = True

    def syntax(self):
        return '[Thread]'

    def __init__(self):
        super().__init__()
        self.sys_hub: Hub = None
        self.dump_hub: Hub = None

        self.schemes: List[List[Scheme]] = []
        self.scrapers: List[Scraper] = []

        self.tasks: List = []

        #
        self.thread_list: List[ScrapyThread] = []

    def signal_callback(self, signum, frame):
        from logging import WARN
        self.log('signal! stop', level=WARN)
        [x.cmd_stop() for x in self.thread_list]

    def options(self, **kw):
        # require_target
        setting = self.setting

        self.sys_hub, self.dump_hub = core.build_hub(setting=setting)
        self.schemes = core.build_thread_schemes(setting.CurrentSchemeList, setting.Thread)
        # self.schemes = core.build_schemes(setting.CurrentSchemeList)

        self.scrapers, self.tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

        # TODO : in options or run
        # preview
        for task in self.tasks:
            self.sys_hub.save(task)

    def run(self, **kw):
        setting = self.setting
        # log thread setting info

        # thread List
        # temp

        for i in range(setting.Thread):
            thread = ScrapyThread(self.sys_hub, self.dump_hub, self.schemes[i], self.scrapers[i], setting, self.log)
            thread.setDaemon(True)
            thread.start()

            self.thread_list.append(thread)

        while self._thread_status():
            time.sleep(0.618)
        # [x.join() for x in self.thread_list]

    def failed(self):
        pass

    def exit(self):
        self.sys_hub.stop(True)
        self.dump_hub.stop(True)

        for scraper in self.scrapers:
            scraper.quit()

    def _thread_status(self):
        count = len([None for x in self.thread_list if x.cmd_status is 1])
        return bool(count)