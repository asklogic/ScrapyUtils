# -*- coding: utf-8 -*-
"""普通单次爬取.

Todo:
    * For module TODOs
    
"""
from os import getcwd
from logging import getLogger

import click

from ScrapyUtils import configure
from ScrapyUtils.core import load, scrape
from ScrapyUtils.core.end import end

logger = getLogger('execute')


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=getcwd(), type=click.Path())
def execute(scheme: str, path):
    """普通爬取"""

    logger.info(f'start command. Target: {scheme}')

    # 设置Scheme
    configure.target_name = scheme

    # 引入Scheme包 - 预加载
    target_module = __import__(scheme)

    # 加载各类组件
    load()
    # 开启爬取
    scrape()

    # TODO: 阻塞
    configure.tasks.join()

    end()
