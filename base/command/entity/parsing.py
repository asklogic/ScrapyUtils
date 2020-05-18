from typing import List, Any
import os
import time

from .thread_ import Thread

from base.libs import Task
from base.components import *


class Parsing(Thread):
    download = None

    @classmethod
    def syntax(cls):
        return '[Parsing]'

    @classmethod
    def command_config(cls, **kwargs):
        cls.config['thread'] = 1
        cls.config['timeout'] = 0

        download = str(kwargs.get('download'))

        # TODO: fixed path

        download_folder = cls.config.get('download_folder')

        dirs = os.listdir(download_folder)

        download_target = [x for x in dirs if os.path.isdir(os.path.join(download_folder, x))]
        assert download_target

        download_target.sort(key=lambda x: int(x), reverse=True)

        if download_target:
            if not (download and download in download_target):
                download = download_target[0]

        cls.download = os.path.join(download_folder, download)
        assert os.path.isdir(cls.download)

        log.info('parsing download path: {}'.format(cls.download), 'Config')
        log.info('parsing download target: {}'.format(download), 'Config')

    @classmethod
    def command_task(cls, **kwargs):

        # TODO: inner
        # dirs = os.listdir(cls.download)
        # dirs = [x for x in dirs if os.path.isfile(x)]

        def inner():
            dirs = [os.path.join(cls.download, x) for x in os.listdir(cls.download)]
            dirs = [x for x in dirs if os.path.isfile(x)]

            for file in dirs:
                with open(file, 'r', encoding='utf8') as f:
                    content = f.read()
                t = Task()
                t.param = content
                yield t

        return inner

    @classmethod
    def command_scraper(cls, **kwargs):
        def inner():
            return None

        return inner

    @classmethod
    def command_components(cls, steps, processors, **kwargs):
        last_action = 0

        for index in range(len(steps)):
            if issubclass(steps[index], ActionStep):
                last_action = index

        steps = [ParsingLoadAction] + steps[last_action + 1:]

        return steps, processors


class ParsingLoadAction(ActionStep):
    def scraping(self, task: Task):
        return task.param
