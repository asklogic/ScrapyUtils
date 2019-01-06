from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import threading, time
import queue
import base.core as core
import scrapy_config

from base.lib import Task, Config
from base.Container import Container
from base.Conserve import Conserve

lock = threading.Lock()
barrier = threading.Barrier(scrapy_config.Thread)

from base.log import getLog,getbriefLog

log = getLog()

class threadTask(threading.Thread):

    def __init__(self, task_queue: queue.Queue, conf: Config, conserve: Conserve, container: Container = None):
        threading.Thread.__init__(self)
        self.tasks: queue.Queue[Task] = task_queue
        self.conf: Config = conf

        self.container: Container = container
        self.conserve: Conserve = conserve
        pass

    def run(self):
        # core prepare
        current_prepare = core.load_prepare(self.conf.prepare, self.conf.job)

        # context
        scraper = current_prepare.get_scraper()
        manager = core.register_manager(self.conf.models, self.conf.job)

        # no context
        schemes = core.load_scheme(self.conf.schemes, self.conf.job)
        # current_conserve = core.load_conserve(self.conf.conserve, self.conf.job)
        current_conserve = self.conserve

        barrier.wait()

        # TODO thread conf 设置
        scraper.set_ProxyContainer(self.container)

        # self.sync(2)
        core.thread_reset(scraper, manager)
        try:
            while True:
                self.sync(0.1)

                task: Task = self.tasks.get(block=True, timeout=10)
                # check before
                # print(task.url)

                scheme_state = core.scrapy(scheme_list=schemes, manager=manager, task=task, scraper=scraper)
                conserve_state = False
                if scheme_state:
                    conserve_state = core.do_conserve(manager=manager, conserve=current_conserve)


                failed_task = core.thread_check(task=task, scheme_state=scheme_state, conserve_state=conserve_state)
                if failed_task:


                    core.thread_reset(scraper, manager)
                    self.tasks.put(failed_task)

                manager.clear_data()



        except queue.Empty as qe:
            print("finish!")
            pass
        # except Exception as e:
        #     print(e.args)
        #     print("some error")
        #     pass

    def sync(self, delay: int = 0):
        lock.acquire()
        if delay:
            time.sleep(delay)
        else:
            time.sleep(0.5)
        lock.release()
