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
@click.argument('scheme')
@click.option('overwrite', '--overwrite/--no-overwrite', default=False, is_flag=True)
@click.option('path', '--path', default=getcwd(), type=click.Path())
def generate(scheme: str, overwrite: bool, path):
    """生成Scheme模板"""
    logger.info(f'start command. Target: {scheme}')

    if overwrite:
        logger.warning(f'Remove the exist folder {path + sep + scheme}')
        remove(scheme)

    create_folder(scheme)
    logger.info('Folder is created.')

    create_components(scheme)
    logger.info('Files is created.')
