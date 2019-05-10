from .Command import Command
from base import core

from base.generate.generator import PROJECT_PATH, generate

import time


class Generate(Command):

    def syntax(self):
        return '[Generate]'

    def signal_callback(self, signum, frame):
        # print(self, signum, frame)

        self.interrupt = True

    def options(self, **kw):
        self.path = kw.get('path', PROJECT_PATH)

        self.target_name = kw.get('target')

        # necessary property
        assert self.path, 'no path'
        assert self.target_name, 'no target name'

    def run(self, **kw):
        path = self.path
        target_name = self.target_name


        time.sleep(0.5)
        self.log('project path: ' + path)
        self.log('target name: ' + target_name)

        remain = 0
        while remain > 0:
            remain = remain - 1
            time.sleep(1)
            self.log('loop')

    def exit(self):
        time.sleep(1)

