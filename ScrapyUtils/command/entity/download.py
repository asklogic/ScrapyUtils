from typing import List, Any
import os
import time

from ScrapyUtils.command.entity.thread_ import Thread
from ScrapyUtils.components import *
from ScrapyUtils.libs import Model, Field, Task

from urllib.parse import urlparse, urlencode


class DownloadModel(Model):
    page_name = Field()
    page_content = Field()


class Download(Thread):
    @classmethod
    def syntax(cls):
        return '[Download]'

    @classmethod
    def command_config(cls, options):

        kwargs = options.get('kwargs')

        if kwargs.get('download'):
            cls.config['download_target'] = options.get('download')

    @classmethod
    def command_components(cls, steps: List[type(ActionStep)], processors: List[type(ParseStep)], options):
        """Remove other parsing steps.

        """
        # mark the last ActionStep.
        last_action = 0

        for index in range(len(steps)):
            if issubclass(steps[index], ActionStep):
                last_action = index

        steps = steps[:last_action + 1]

        # add the downalod steps.
        steps.append(DownloadAction)
        steps.append(DownloadParse)

        # fixed processor.
        processors = [DownloadProcessor]

        return steps, processors


class DownloadAction(ActionStep):
    """Add page_name in the context."""

    def scraping(self, task: Task):
        """if url. parse and get uri"""

        path: str = urlparse(task.url).path

        if path.count(r'/') > 1:
            uri_name = path.split('/')[-1]
        else:
            uri_name = path

        # TODO: task.param in uri
        param = urlencode(task.param)
        if param:
            self.context['page_name'] = ''.join((uri_name, '.', param))
        else:
            self.context['page_name'] = uri_name


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

        download_path = os.path.join(self.download_folder, self.download_name)

        self.download_index = 0

        # settings
        # Download suffix.
        self.suffix = config.get('download_suffix', 'html')

        # Download path.
        # Force override.
        self.download_path = config.get('download_path', download_path)

        if not os.path.isdir(self.download_path):
            os.mkdir(self.download_path)

        log.info('Target folder: ' + os.path.basename(self.download_path), 'Download')
        log.info('suffix: ' + self.suffix, 'Download')
        log.info('path: ' + self.download_path, 'Download')

    def process_item(self, model: DownloadModel) -> Any:
        page_name = str(model.page_name)
        page_content = model.page_content

        with_suffix = self.suffix in page_name and page_name[-len(self.suffix):] == self.suffix
        if with_suffix:
            name = os.path.join(self.download_path, ''.join((str(model.page_name))))
        else:
            name = os.path.join(self.download_path, ''.join((str(model.page_name), '.', self.suffix)))

        # TODO: refactor name
        while os.path.exists(name):
            self.download_index += 1
            name = os.path.join(self.download_path,
                                ''.join((page_name, str(self.download_index), '.', self.suffix)))

        if type(page_content) is bytes:
            with open(name, 'wb') as f:
                f.write(model.page_content)

        elif type(page_content) is str:
            with open(name, 'w', encoding='utf-8') as f:
                f.write(model.page_content)

    def on_start(self):
        pass

    def on_exit(self):
        pass
