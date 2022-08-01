# -*- coding: utf-8 -*-
"""生成爬取对象.

Todo:
    * For module TODOs

"""
from logging import getLogger
from os import getcwd, sep

import click
from ScrapyUtils.generate.generator import create_components, create_folder, remove

logger = getLogger('generate')


@click.command()
@click.argument('project')
@click.option('overwrite', '--overwrite/--no-overwrite', default=False, is_flag=True)
@click.option('path', '--path', default=getcwd(), type=click.Path())
def generate(project: str, overwrite: bool, path):
    """生成project模板"""
    logger.info(f'start command. Target: {project}')

    if overwrite:
        logger.warning(f'Remove the exist folder {path + sep + project}')
        remove(project)

    create_folder(project)
    logger.info('Folder is created.')

    create_components(project)
    logger.info('Files is created.')
