# -*- coding: utf-8 -*-
"""仅分析.

Todo:
    * For module TODOs

"""
import os
import time
import types
from cmd import Cmd
from typing import Iterator

import click

from logging import getLogger
from os import getcwd, sep

from ScrapyUtils import configure
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.core import start_engine
from ScrapyUtils.components import Action
from ScrapyUtils.core.end import end
from ScrapyUtils.libs import Task, Scraper, Model

logger = getLogger('generate')


@click.command()
@click.argument('project')
@click.option('overwrite', '--overwrite/--no-overwrite', default=False, is_flag=True)
@click.option('path', '--path', default=getcwd(), type=click.Path())
def parsing(project: str, overwrite: bool, path):
    """仅分析"""
    logger.info(f'start command. Target: {project}')

    # 设置project
    configure.project_package_path = project

    # 引入project包 - 预加载
    __import__(project)

    # 修改设置
    # 重试次数为1次 线程数为1个 任务间隔为0秒
    configure.RETRY = 1
    configure.THREAD = 1
    configure.DELAY = 0

    # 去除普通Action
    configure.action_classes = [_ for _ in configure.action_classes if _.is_parser]
    configure.action_classes.insert(0, ParsingLoadAction)

    # 覆盖Task生成
    configure.tasks_callable = load_parsing_task

    # 加载各类组件
    start_engine()
    # 开启爬取
    scrape()

    # TODO: 阻塞
    exit_flag = False
    while not configure.tasks.join() and not exit_flag:
        time.sleep(configure.EXIT_WAIT)
        exit_flag = configure.tasks.qsize() == 0

    end()


def load_parsing_task():
    logger.info(f'Download Folder Path: {configure.DOWNLOAD_FOLDER_PATH}')
    # 当前目录的子文件夹列表
    sub_dirs = list(os.walk(configure.DOWNLOAD_FOLDER_PATH))[0][1]
    sub_dirs_content = r'\n'.join(sub_dirs)

    if sub_dirs:
        # 默认最新的
        sub_dirs.sort(reverse=True)
        target_download_folder = os.path.join(configure.DOWNLOAD_FOLDER_PATH, sub_dirs[0])
        # 当前目录下的文件
        files_name = list(os.walk(target_download_folder))[0][-1]
        # 拼接文件的绝对路径
        files_path = [os.path.join(target_download_folder, file_name) for file_name in files_name]

        logger.info(f'Parsing folder: {target_download_folder}')
        # TODO: bytes and str content
        for file_path in files_path:
            with open(file_path, encoding='utf-8') as f:
                str_content = f.read()
            with open(file_path, 'rb') as f:
                bytes_content = f.read()

            task = Task()
            task.url = os.path.basename(file_path)
            task.param = {
                'str_content': str_content,
                'bytes_content': bytes_content,
            }
            yield task

    # TODO: menu?
    # if sub_dirs:
    #     class Selector(Cmd):
    #         intro = f"There are {1} download records.\n {sub_dirs_content}"
    #
    #     selector = Selector()
    #     for index, sub_dir in enumerate(sub_dirs):
    #         setattr(t, f'do_{i}', types.MethodType(lambda self, args: print(f'hello! {args}'), t))


class ParsingLoadAction(Action):
    priority = 1000000

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        content.str_content = task.param.get('str_content')
        content.bytes_content = task.param.get('bytes_content')
