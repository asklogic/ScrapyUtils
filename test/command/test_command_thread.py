from unittest import TestCase, skip
from base.command import Command, get_command

from base import core
from base.hub import Hub
from base.components import *
from base.libs import *
from typing import *


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

        self.tasks : List = []

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


class TestCommandThread(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    @classmethod
    def setUpClass(cls) -> None:
        cls.cmd = Thread()
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
        pass
