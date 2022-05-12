# -*- coding: utf-8 -*-
"""仅分析.

Todo:
    * For module TODOs

"""
from typing import Iterator

import click

from logging import getLogger
from os import getcwd, sep

from ScrapyUtils import configure
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.core import load, scrape
from ScrapyUtils.components import Action
from ScrapyUtils.core.end import end
from ScrapyUtils.libs import Task, Scraper, Model

logger = getLogger('generate')


@click.command()
@click.argument('scheme')
@click.option('overwrite', '--overwrite/--no-overwrite', default=False, is_flag=True)
@click.option('path', '--path', default=getcwd(), type=click.Path())
def parsing(scheme: str, overwrite: bool, path):
    """仅分析"""
    logger.info(f'start command. Target: {scheme}')

    # 设置Scheme
    configure.target_name = scheme

    # 引入Scheme包 - 预加载
    __import__(scheme)

    # 去除Parser
    configure.action_classes = [_ for _ in configure.action_classes if not _.is_parser]
    configure.action_classes.insert(0, DownloadSaveAction)

    # 加载各类组件
    load()
    # 开启爬取
    scrape()

    # TODO: 阻塞
    configure.tasks.join()

    end()


class ParsingLoadAction(Action):
    priority = 1000000

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        pass


