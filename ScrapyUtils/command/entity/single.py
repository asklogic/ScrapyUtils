from typing import *
from queue import Queue

import os
import ast

from . import Command, ComponentMixin
from ScrapyUtils.components import *
from ScrapyUtils.libs import *

import click


class Single(Command):

    def options(self, **kwargs):
        # path = kwargs.get('path', PROJECT_PATH)
        # scheme = kwargs.get('scheme')
        # assert scheme, 'no scheme'
        #
        # path = os.path.join(path, scheme)
        # assert os.path.exists(path), path + ' not exist'
        """
        Args:
            **kwargs:
        """
        pass

    def run(self):

        content = ''
        context = {}
        scraper = collect.scraper()
        models = []

        task = collect.tasks.get()

        # init step
        suit = StepSuit(collect.steps_class, scraper, self.log, models)

        for step in suit.steps:
            res = step.do(task)
            self.log.info('{} - <{}>, res:{}'.format(suit.steps.index(step) + 1, step.name, res), 'Step')

            if not step.do(task):
                self.log.info('failed. count: {0}, url: {1}.'.format(task.mock_count, task.url))

            cmd = input('command:')

            if cmd == '':
                continue
            elif cmd == '0':
                self.log.info('interrupted!')
                break
            else:
                try:
                    res = eval(cmd)
                    res = 'None' if res is None else res
                    self.log.info('Executed. output:' + str(res))
                except Exception as e:
                    self.log.exception(e)

    def exit(self):
        self.log.info('exit.')

    def syntax(self) -> str:
        return '[Single]'

    def signal_callback(self, signum, frame):
        """
        Args:
            signum:
            frame:
        """
        print('signal_callback')

    def failed(self):
        print('failed')
