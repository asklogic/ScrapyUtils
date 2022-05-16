# -*- coding: utf-8 -*-
"""命令集.

Todo:
    * For module TODOs

"""
from .execute import execute
from .generate import generate
from .download import download
from .parsing import parsing

import click


@click.group()
def cli():
    pass


cli.add_command(execute)
cli.add_command(generate)
cli.add_command(download)
cli.add_command(parsing)
