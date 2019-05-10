from .Command import Command
from base import core

from base.generate.generator import PROJECT_PATH, generate


class Generate(Command):

    def syntax(self):
        return '[Generate]'

    def build_setting(self):
        pass

    def options(self):
        pass

    def run(self, **kw):
        path = kw.get('path', PROJECT_PATH)
        self.log('project path: ' + path)

    def failed(self):
        super().failed()

    def exit(self):
        super().exit()
