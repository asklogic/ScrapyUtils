from unittest import TestCase, skip
from base.command import Command, get_command

from base import core
from base.hub import Hub
from base.components import *
from base.libs import *
from typing import *
from base.command import get_command, trigger

import multiprocessing
import threading
from queue import Empty


# from types import *
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

    def signal_callback(signum, frame, self):
        super().signal_callback(frame, self)

    def options(self, **kw):
        # require_target
        setting = self.setting

        self.sys_hub, self.dump_hub = core.build_hub(setting=setting)
        self.schemes = core.build_schemes(setting.CurrentSchemeList)

        self.scrapers, self.tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

    def run(self, **kw):
        # preview

        # log thread setting info

        # thread List

        pass

    def failed(self):
        pass

    def exit(self):
        self.sys_hub.stop(True)
        self.dump_hub.stop(True)

        for scraper in self.scrapers:
            scraper.quit()


class ScrapyThread(threading.Thread):

    def __init__(self, sys_hub: Hub, dump_hub: Hub, schemes: List[Scheme], scraper: Scraper, setting: Setting):
        threading.Thread.__init__(self)

        self.sys: Hub = sys_hub
        self.dump: Hub = dump_hub
        self.schemes: List[Scheme] = schemes
        self.scraper: Scraper = scraper

        self.setting: Setting = setting

    def run(self) -> None:
        task = None
        while 'cmd_signal' and (task = self.get_task()):
            pass
        pass

    def get_task(self):
        task = None
        try:
            task = self.sys.pop('TaskModel')
        except Empty as e:
            pass
        finally:
            return task





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

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_init(self):
        cmd: Thread = self.cmd
        kw = {
            'target': 'TestEmptyThread'
        }
        cmd.build_setting(**kw)

    def test_option(self):
        cmd = self.cmd

        cmd.options()

    # @skip
    def test_run(self):
        cmd = self.cmd

        cmd.options()
        cmd.run()
        cmd.exit()

    def test_trigger(self):
        pass
