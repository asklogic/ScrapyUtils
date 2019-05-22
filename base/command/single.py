from typing import *
from base.command import Command

from base import core
from base.components import *
from base.libs import *
from base.hub import *
from base.command import Command

import click


@click.command()
@click.option('--count', default=1, prompt='first prompt')
def step(count):
    pass


class Single(Command):
    require_target = True

    def __init__(self):
        super().__init__()

        # self.sys_hub: Hub = None
        self.dump_hub: Hub = None

        self.schemes: List[Scheme] = []

        self.scraper: Scraper = None
        self.task = None

    def syntax(self):
        return '[Single]'

    def signal_callback(self, signum, frame):
        super().signal_callback(signum, frame)

    def options(self, **kw):
        setting = self.setting

        self.sys_hub, self.dump_hub = core.build_hub(setting=setting)
        self.schemes = core.build_schemes(setting.CurrentSchemeList)

        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

        self.task = tasks[0]
        self.scraper = scrapers[0]

    def run(self, **kw):
        for scheme in self.schemes:
            step()
            print('step dones')
            pass

        pass

    def failed(self):
        pass

    def exit(self):
        pass
