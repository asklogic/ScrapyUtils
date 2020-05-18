from typing import List, Any
import os
import time

from base.command.entity.thread_ import Thread
from base.components import *
from base.libs import Model, Field, Task


class Download(Thread):

    @classmethod
    def command_components(cls, steps: List[type(ActionStep)], processors: List[type(ParseStep)], **kwargs):

        last_action = 0

        for index in range(len(steps)):
            if issubclass(steps[index], ActionStep):
                last_action = index

        steps = steps[:last_action + 1]
        steps.append(DownloadAction)
        steps.append(DownloadParse)

        processors = [DownloadProcessor]

        return steps, processors


class DownloadModel(Model):
    page_name = Field()
    page_content = Field()


class DownloadAction(ActionStep):

    def scraping(self, task: Task):
        self.context['page_name'] = task.url


class DownloadParse(ParseStep):
    def parsing(self):
        model = DownloadModel()

        model.page_content = self.content
        model.page_name = self.context['page_name']
        yield model


class DownloadProcessor(Processor):
    target = DownloadModel

    def __init__(self, config: dict = None):
        super().__init__(config)

        self.download_folder = config.get('download_folder')
        if not os.path.isdir(self.download_folder):
            os.mkdir(self.download_folder)

        self.download_name = str(int(time.time()))

        self.current_download_path = os.path.join(self.download_folder, self.download_name)
        if not os.path.isdir(self.current_download_path):
            os.mkdir(self.current_download_path)

        log.info('download path {}'.format(self.current_download_path), 'Download')

        self.download_index = 0

    def process_item(self, model: DownloadModel) -> Any:
        # name = os.path.join(self.current_download_path, str(model.page_name))
        # while os.path.exists(name):
        #     name = os.path.join(self.current_download_path, str(model.page_name) + str(self.download_index))
        #     self.download_index += 1
        name = os.path.join(self.current_download_path, str(self.download_index) + '.html')
        while os.path.exists(name):
            self.download_index += 1
            name = os.path.join(self.current_download_path, str(self.download_index) + '.html')

        with open(name, 'w', encoding='utf8') as f:
            f.writelines(model.page_content)

    def on_start(self):
        pass

    def on_exit(self):
        pass
