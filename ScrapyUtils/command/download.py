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
from typing import Iterator, NoReturn

import click

from ScrapyUtils import configure
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.core import load, scrape
from ScrapyUtils.components import Action
from ScrapyUtils.core.end import end
from ScrapyUtils.libs import Task, Scraper, Model

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

    # 加载各类组件
    load()
    # 开启爬取
    scrape()

    # TODO: 阻塞
    configure.tasks.join()

    end()


class DownloadSaveAction(Action):
    priority = 1
    is_parser = True

    def on_start(self) -> NoReturn:
        self.batch_id = int(time.time()) % 10000000
        self.suffix = configure.DOWNLOAD_SUFFIX

        self.download_folder = configure.DOWNLOAD_FOLDER_PATH

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        file_name: str = content.parameters.get('file_name', f'{self.batch_id}_{get_current_index()}')

        if not file_name.endswith(self.suffix):
            file_name = f'{file_name}{self.suffix}'

        if content.bytes_content:
            with open(os.path.join(self.download_folder, file_name), 'wb') as f:
                f.write(content.bytes_content)

        elif content.str_content:
            with open(os.path.join(self.download_folder, file_name), 'w', encoding='utf-8') as f:
                f.write(content.str_content)


# count

count_lock = Lock()
count_index = 0


def get_current_index():
    global count_index, count_lock
    with count_lock:
        count_index += 1
        return count_index
