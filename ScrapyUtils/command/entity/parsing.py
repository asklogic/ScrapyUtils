from typing import List, Any
import os
import time

from .thread_ import Thread

from ScrapyUtils.libs import Task
from ScrapyUtils.components import *
from ScrapyUtils.core import configure

from . import log


class Parsing(Thread):
    download: str = None
    index: int = None

    @classmethod
    def syntax(cls):
        return '[Parsing]'

    @classmethod
    def command_config(cls, options):
        configure.TIMEOUT = 0
        configure.THREAD = 1

        kwargs = options.get('kwargs')

        download = kwargs.get('download')
        index = int(kwargs.get('index', -1))

        # TODO: fixed download folder path
        download_folder = configure.DOWNLOAD_FOLDER_PATH

        # list download target.
        dirs = os.listdir(download_folder)
        download_target = [x for x in dirs if os.path.isdir(os.path.join(download_folder, x))]

        assert download_target, 'there are no download targets.'

        # sort and reverse.
        download_target.sort(key=lambda x: int(x))

        # select download target.
        if not (download and download in download_target):
            download = download_target[index]

        cls.download = os.path.join(download_folder, download)
        assert os.path.isdir(cls.download), 'download target {} not exist.'.format(cls.download)

    @classmethod
    def command_collect_logout(cls):
        files = list(os.walk(cls.download))[0][2]

        log.info('Parsing from: ' + cls.download)
        # log.info(cls.download, 'Command')
        log.info('Download target name: ' + os.path.basename(cls.download))
        # log.info(os.path.basename(cls.download), 'Command')
        log.info('Page count: ' + str(len(files)))
        # log.info(str(len(files)), 'Command')

        super().command_collect_logout()

    @classmethod
    def command_task(cls, options):
        def inner():
            time.sleep(0.618)

            dirs = [os.path.join(cls.download, x) for x in os.listdir(cls.download)]
            dirs = [x for x in dirs if os.path.isfile(x)]
            log.info('Load download files.')
            log.info(f'Files number:{len(dirs)}, from {cls.download}')

            for file in dirs:
                with open(file, 'r', encoding='utf8') as f:
                    content = f.read()
                t = Task()
                t.url = os.path.basename(file)
                t.param = content
                yield t

            log.info('done.')

        return inner

    @classmethod
    def command_scraper(cls, options):
        """
        Args:
            options:
        """

        def inner():
            return None

        return inner

    @classmethod
    def command_components(cls, steps, processors, options):
        """
        Args:
            steps:
            processors:
            options:
        """
        last_action = 0

        for index in range(len(steps)):
            if issubclass(steps[index], ActionStep):
                last_action = index

        steps = [ParsingLoadAction] + steps[last_action + 1:]

        return steps, processors


class ParsingLoadAction(ActionStep):
    def scraping(self, task: Task, content):
        """
        Args:
            task (Task):
        """
        self.context['page_name'] = task.url
        return task.param
