from typing import List, Any
import os
import time

from base.command.entity.thread_ import Thread
from base.components import *
from base.libs import Model, Field, Task

from base.common import DownloadModel
from urllib.parse import urlparse

file_type = 'html'


class Download(Thread):
    @classmethod
    def syntax(cls):
        return '[Download]'

    @classmethod
    def command_config(cls, **kwargs):

        # TODO: refactor
        """
        Args:
            **kwargs:
        """
        global file_type
        if kwargs.get('file_type', 'html'):
            file_type = str(kwargs.get('file_type', 'html'))

        if kwargs.get('download'):
            cls.config['download_target'] = kwargs.get('download')

    @classmethod
    def command_components(cls, steps: List[type(ActionStep)], processors: List[type(ParseStep)], **kwargs):

        """
        Args:
            steps:
            processors:
            **kwargs:
        """
        last_action = 0

        for index in range(len(steps)):
            if issubclass(steps[index], ActionStep):
                last_action = index

        steps = steps[:last_action + 1]
        steps.append(DownloadAction)
        steps.append(DownloadParse)

        processors = [DownloadProcessor]

        return steps, processors


class DownloadAction(ActionStep):
    """add page_name"""

    def scraping(self, task: Task):
        # if url. parse and get uri
        """
        Args:
            task (Task):
        """
        path: str = urlparse(task.url).path

        if path.count(r'/') > 1:
            page_name = path.split('/')[-1]
        else:
            page_name = path

        # TODO: get page_name from Task

        self.context['page_name'] = page_name


class DownloadParse(ParseStep):

    def parsing(self):
        model = DownloadModel()

        model.page_name = self.context['page_name']
        model.page_content = self.content

        yield model


class DownloadProcessor(Processor):
    target = DownloadModel

    def __init__(self, config: dict = None):
        """
        Args:
            config (dict):
        """
        super().__init__(config)

        # download folder.
        self.download_folder = config.get('download_folder')

        if not os.path.isdir(self.download_folder):
            os.mkdir(self.download_folder)

        # create download target folder.

        self.download_name = config.get('download_target', str(int(time.time())))

        self.current_download_path = os.path.join(self.download_folder, self.download_name)
        if not os.path.isdir(self.current_download_path):
            os.mkdir(self.current_download_path)

        self.download_index = 0
        # assert False

        log.info(os.path.basename(self.current_download_path), 'Target')
        log.info(file_type, 'Suffix')
        log.info(self.current_download_path, 'Path')

        # log.info('download path target: {}'.format(os.path.basename(self.current_download_path)), 'Download')

    def process_item(self, model: DownloadModel) -> Any:
        # name = os.path.join(self.current_download_path, str(model.page_name))
        # while os.path.exists(name):
        #     name = os.path.join(self.current_download_path, str(model.page_name) + str(self.download_index))
        #     self.download_index += 1

        """
        Args:
            model (DownloadModel):
        """
        name = os.path.join(self.current_download_path, ''.join((str(model.page_name), '.', file_type)))
        while os.path.exists(name):
            self.download_index += 1
            name = os.path.join(self.current_download_path,
                                ''.join((str(model.page_name), str(self.download_index), '.', file_type)))

        with open(name, 'w', encoding='utf-8') as f:
            # with open(name, 'wb') as f:
            f.write(model.page_content)

    def on_start(self):
        pass

    def on_exit(self):
        pass
