from unittest import TestCase, skip
from base.command import Command, get_command

from base import core
from base.hub import Hub
from base.components import *
from base.libs import *
from typing import *
from base.command import get_command, trigger

# from multiprocessing import dummy as multiprocessing
import multiprocessing
import multiprocessing.dummy

import threading
from queue import Empty
from concurrent.futures import ThreadPoolExecutor
import time

from base.command.thread import ScrapyThread
from base.command.thread import Thread

# from types import *


lock = threading.Lock()


# class ScrapyThread(threading.Thread):
#
#     def __init__(self, sys_hub: Hub, dump_hub: Hub, schemes: List[Scheme], scraper: Scraper, setting: Setting, log):
#         threading.Thread.__init__(self)
#         super(ScrapyThread, self).__init__()
#
#         self.sys: Hub = sys_hub
#         self.dump: Hub = dump_hub
#         self.schemes: List[Scheme] = schemes
#         self.scraper: Scraper = scraper
#
#         self.setting: Setting = setting
#
#         # todo
#         self.current_task = None
#         self.cmd_status = True
#         self.log = log
#
#     def run(self) -> None:
#         task = None
#
#         while self.cmd_status and self.get_task():
#             task = self.current_task
#             core.load_context(task, self.schemes)
#
#             res = core.scrapy(self.schemes, self.scraper, task, self.dump, self.sys)
#             if res:
#                 self.log("success. Task url:{} param {} count - {}".format(task.url, task.param, task.count))
#             elif task.count < self.setting.FailedRetry:
#                 # reset
#                 self.reset()
#
#                 # sleep
#                 time.sleep(self.setting.FailedBlock)
#                 # status.info("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))
#
#                 # back to sys
#                 task.count = task.count + 1
#                 self.sys.save(task)
#             else:
#                 time.sleep(self.setting.FailedBlock)
#                 self.log("failed. Task url:{} param {} count - {}".format(task.url, task.param, task.count))
#
#         self.log('thread named: %s finish!' % self.getName())
#
#     def get_task(self):
#         self.current_task = None
#         try:
#             task = self.sys.pop('TaskModel')
#             self.current_task = task
#             return True
#         except Empty as e:
#             return False
#
#     def reset(self):
#         self.scraper.clear_session()
#         if self.setting.ProxyAble:
#             proxy_model = self.sys.pop("ProxyModel")
#             self.scraper.set_proxy((proxy_model.ip, proxy_model.port))
#
#         # fixme
#         for scheme in self.schemes:
#             scheme.context.clear()
#
#     def sync(self, delay: int = 0):
#         lock.acquire()
#         if delay:
#             time.sleep(delay)
#         else:
#             time.sleep(0.5)
#         lock.release()
#
#     def cmd_stop(self):
#         self.cmd_status = False


class TestCommandThread(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    @classmethod
    def setUpClass(cls) -> None:
        cls.cmd = Thread()
        kw = {
            'target': 'TestEmptyThread'
        }
        cls.cmd.build_setting(**kw)

        setting = core.build_setting('TestEmptyThread')

        sys_hub, dump_hub = core.build_hub(setting=setting)
        sys_hub.set_timeout('TaskModel', 0.1)
        schemes = core.build_schemes(setting.CurrentSchemeList)
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

        cls.thread = ScrapyThread(sys_hub, dump_hub, schemes, scrapers[0], setting, cls.cmd.log)

        cls.mock_cmd = Thread()
        kw = {
            'target': 'TestEmptyThread'
        }
        cls.cmd.build_setting(**kw)
        cls.mock_cmd.thread_list.append(cls.thread)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_init(self):
        cmd = get_command('thread')
        kw = {
            'target': 'TestEmptyThread'
        }
        cmd.build_setting(**kw)

    def test_option(self):
        cmd = self.cmd

        # property
        self.assertEqual(cmd.dump_hub, None)
        self.assertEqual(cmd.sys_hub, None)

        self.assertEqual(cmd.scrapers, [])
        self.assertEqual(cmd.schemes, [])
        self.assertEqual(cmd.tasks, [])

        self.assertEqual(cmd.thread_list, [])

        # options init components

        cmd.options()

        self.assertIsInstance(cmd.dump_hub, Hub)
        self.assertIsInstance(cmd.sys_hub, Hub)

        # [self.assertTrue(issubclass(x, Scheme)) for x in cmd.schemes]
        [[self.assertIsInstance(x, Scheme) for x in schemes] for schemes in self.cmd.schemes]
        [self.assertIsInstance(x, Scraper) for x in cmd.scrapers]
        [self.assertTrue(x.get_name(), 'TaskModel') for x in cmd.tasks]

    def test_signal_callback(self):
        [self.assertEqual(x.cmd_status, 1) for x in self.mock_cmd.thread_list]
        self.mock_cmd.signal_callback(1, object)
        [self.assertEqual(x.cmd_status, -1) for x in self.mock_cmd.thread_list]

    def test_exit(self):
        pass

    def test_failed(self):
        pass

    @skip
    def test_run(self):
        cmd = Thread()
        kw = {
            'target': 'TestEmptyThread'
        }
        cmd.build_setting(**kw)

        # cmd = self.cmd

        import signal
        signal.signal(signal.SIGINT, cmd.signal_callback)

        cmd.options()
        cmd.run()
        cmd.exit()

    def test_scrapy_thread_init(self):
        setting = core.build_setting('TestEmptyThread')

        sys_hub, dump_hub = core.build_hub(setting=setting)
        sys_hub.set_timeout('TaskModel', 0.1)
        schemes = core.build_schemes(setting.CurrentSchemeList)
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

        thread = ScrapyThread(sys_hub, dump_hub, schemes, scrapers[0], setting, self.cmd.log)

        self.assertIsInstance(thread.sys, Hub)
        self.assertIsInstance(thread.dump, Hub)
        self.assertIsInstance(thread.scraper, Scraper)
        self.assertIsInstance(thread.setting, Setting)

        [self.assertIsInstance(x, Scheme) for x in thread.schemes]

        self.assertEqual(thread.current_task, None)
        self.assertEqual(thread.cmd_status, 1)
        self.assertEqual(thread.log, self.cmd.log)

        # special
        context_id = id(thread.schemes[0].context)
        [self.assertEqual(context_id, id(x.context)) for x in thread.schemes]

    @skip
    def test_scrapy_thread_run(self):
        setting = core.build_setting('TestEmptyThread')

        sys_hub, dump_hub = core.build_hub(setting=setting)
        sys_hub.set_timeout('TaskModel', 0.1)
        schemes = core.build_schemes(setting.CurrentSchemeList)
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

        thread = ScrapyThread(sys_hub, dump_hub, schemes, scrapers[0], setting, self.cmd.log)

        sys_hub.save(tasks[0])

        # add model
        self.assertEqual(dump_hub.get_number(dump_hub.model_list[0]), 0)
        thread.run()
        self.assertEqual(dump_hub.get_number(dump_hub.model_list[0]), 1)

    @skip
    def test_trigger(self):
        kw = {
            # 'target': 'TestBlockThread'
            'target': 'TestEmptyThread'
        }
        trigger('thread', **kw)
