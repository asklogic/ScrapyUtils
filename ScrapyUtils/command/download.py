# -*- coding: utf-8 -*-
"""仅下载.

Todo:
    * For module TODOs

"""
import os.path
import time
from os import getcwd
from logging import getLogger
from threading import Lock
from typing import Iterator, NoReturn, Optional, Union

import click

from ScrapyUtils import configure
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.core import load, scrape
from ScrapyUtils.components import Action, Processor
from ScrapyUtils.core.end import end
from ScrapyUtils.libs import Task, Scraper, Model, Field

logger = getLogger('download')


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=getcwd(), type=click.Path())
def download(scheme: str, path):
    """普通爬取"""

    logger.info(f'start command. Target: {scheme}')

    # 设置Scheme
    configure.target_name = scheme

    # 引入Scheme包 - 预加载
    __import__(scheme)

    # 去除Parser
    configure.action_classes = [_ for _ in configure.action_classes if not _.is_parser]
    configure.action_classes.append(DownloadSaveAction)

    configure.processor_classes = [DownloadSaveProcessor]

    # 加载各类组件
    load()
    # 开启爬取
    scrape()

    # TODO: 阻塞
    configure.tasks.join()

    end()


class DownloadSaveAction(Action):
    """生成PageContent对象"""
    priority = 1
    is_parser = True

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        file_name: str = content.parameters.get('file_name')

        yield PageContent(
            file_name=file_name,
            bytes_content=content.bytes_content,
            str_content=content.str_content,
        )


class PageContent(Model):
    file_name = Field()
    bytes_content = Field()
    str_content = Field()


class DownloadSaveProcessor(Processor):
    """保存PageContent对象"""
    file_index = 0

    def on_start(self) -> NoReturn:
        self.batch_id = int(time.time())
        self.suffix = configure.DOWNLOAD_SUFFIX

        self.download_folder = os.path.join(configure.DOWNLOAD_FOLDER_PATH, str(self.batch_id))

        os.makedirs(self.download_folder)

    def get_current_index(self):
        self.file_index += 1
        return self.file_index

    def process_item(self, model: PageContent) -> Optional[Union[Model, bool]]:
        # file name
        file_name: str = model.file_name if model.file_name else str(self.get_current_index())
        if not file_name.endswith(self.suffix):
            file_name = f'{file_name}{self.suffix}'

        # case: 如果有bytes型 优先
        if model.bytes_content:
            with open(os.path.join(self.download_folder, file_name), 'wb') as f:
                f.write(model.bytes_content)
        # case: str型
        elif model.str_content:
            with open(os.path.join(self.download_folder, file_name), 'w', encoding='utf-8') as f:
                f.write(model.str_content)