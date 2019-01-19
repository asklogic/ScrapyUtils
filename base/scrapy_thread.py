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

from base.log import status, act



class threadTask(threading.Thread):

    def __init__(self, task_queue: Container, conf: Config, containers: Dict[str, Container] = None):
        threading.Thread.__init__(self)
        self.tasks: Container = task_queue
        self.conf: Config = conf

        # self.container: Container = container
        # self.conserve: Conserve = conserve

        self.containers: Dict[str, Container] = containers

        pass

    def run(self):
        # FIXME 单个Scraper生成
        # core prepare
        current_prepare = core.load_prepare(self.conf.prepare, self.conf.job)

        # context
        scraper = current_prepare.get_scraper()

        # models = core.load_models(self.conf.models, self.conf.job)
        manager = core.register_manager(config=self.conf)

        # no context
        schemes = core.load_scheme(self.conf.schemes, self.conf.job)

        barrier.wait()

        if scrapy_config.Proxy_Able:
            scraper.set_ProxyContainer(self.containers.get("ProxyModel"))

        # self.sync(2)
        core.thread_reset(scraper, manager)
        try:
            while True:
                self.sync(scrapy_config.Block)

                task: Task = self.tasks.pop()
                if not task:
                    break
                # check before
                # print(task.url)

                scheme_state = core.scrapy(scheme_list=schemes, manager=manager, task=task, scraper=scraper)
                conserve_state = False
                if scheme_state:
                    # conserve_state = core.do_conserve(manager=manager, conserve=current_conserve)
                    conserve_state = core.thread_conserve(manager=manager, containers=self.containers)

                failed_task = core.thread_check(task=task, scheme_state=scheme_state, conserve_state=conserve_state)
                if failed_task:
                    core.thread_reset(scraper, manager)
                    self.tasks.add(failed_task)

                manager.clear_data()



        except queue.Empty as qe:
            print("finish!")
            pass
        # except Exception as e:
        #     print(e.args)
        #     print("some error")
        #     pass

        scraper.quit()

    def sync(self, delay: int = 0):
        lock.acquire()
        if delay:
            time.sleep(delay)
        else:
            time.sleep(0.5)
        lock.release()
