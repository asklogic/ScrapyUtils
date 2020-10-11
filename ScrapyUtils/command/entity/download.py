from typing import List, Any
import os
import time

from ScrapyUtils.command.entity.thread_ import Thread
from ScrapyUtils.components import *
from ScrapyUtils.libs import Model, Field, Task
from ScrapyUtils.core import configure

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

        """
        Args:
            options:
        """
        kwargs = options.get('kwargs')

        if kwargs.get('download'):
            cls.config['download_target'] = options.get('download')

    @classmethod
    def command_components(cls, steps: List[type(ActionStep)], processors: List[type(ParseStep)], options):
        """Remove other parsing steps.

        Args:
            steps:
            processors:
            options:
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
        """if url. parse and get uri

        Args:
            task (Task):
        """

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


def safe_create_path(abs_path: str) -> str:
    # case 1: Exist path.
    # case 2: Exist duplicate file.
    # case 3: Not exist.
    if os.path.isdir(abs_path):
        return abs_path
    elif os.path.isfile(abs_path):
        raise Exception('Exist file named: {}'.format(abs_path))
    else:
        os.mkdir(abs_path)

    assert os.path.isdir(abs_path), f'Assert failed in safe_create_path. Path: {abs_path}'
    return abs_path


class DownloadProcessor(Processor):
    target = DownloadModel

    # property:
    current_path: str = None
    download_index: int = 0

    download_target: str = None

    def __init__(self, config: dict = None):
        """
        Args:
            config (dict):
        """
        super().__init__(config)

        download_path = configure.DOWNLOAD_PATH
        download_folder = configure.DOWNLOAD_FOLDER_PATH

        # fixed download path:
        if download_path:
            safe_create_path(download_path)
            self.current_path = download_path

        # no fixed download path:
        else:
            safe_create_path(download_folder)

            # TODO: from command kwargs
            # create download target folder.
            self.download_target = config.get('download_target', str(int(time.time())))
            download_path = os.path.join(download_folder, self.download_target)

            safe_create_path(download_path)
            self.current_path = download_path

        # settings
        # Download suffix.
        self.suffix = configure.DOWNLOAD_SUFFIX

        if self.download_target:
            log.info('Target folder: ' + self.download_target, 'Download')
        log.info('suffix: ' + self.suffix, 'Download')
        log.info('path: ' + os.path.join(os.getcwd(), self.current_path), 'Download')

    def process_item(self, model: DownloadModel) -> Any:
        page_name = str(model.page_name)
        if page_name.startswith('/'):
            page_name = page_name[1:]
        page_content = model.page_content

        # check if the suffix in the page_name.
        with_suffix = self.suffix in page_name and page_name[-len(self.suffix):] == self.suffix
        if with_suffix:
            name = os.path.join(self.current_path, ''.join((str(page_name))))
        else:
            name = os.path.join(self.current_path, ''.join((str(page_name), '.', self.suffix)))

        # TODO: refactor name

        # Check if existed name. If existed, add file index.
        while os.path.exists(name):
            self.download_index += 1
            name = os.path.join(self.current_path,
                                ''.join((page_name, str(self.download_index), '.', self.suffix)))

        if type(page_content) is bytes:
            with open(name, 'wb') as f:
                f.write(page_content)

        elif type(page_content) is str:
            with open(name, 'w', encoding='utf-8') as f:
                f.write(page_content)

    def on_start(self):
        pass

    def on_exit(self):
        pass
