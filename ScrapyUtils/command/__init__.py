# -*- coding: utf-8 -*-
"""命令集.

Todo:
    * For module TODOs

"""
import os

from abc import abstractmethod
from logging import Logger, getLogger
from typing import List

import click

from ScrapyUtils import configure

logger = getLogger('command')


@click.group()
def cli():
    """ScrapyUtils command group."""
    pass


common_option = {
    'project':
        click.Argument(
            param_decls=['project'],
        ),
    'path':
        click.Option(
            param_decls=['--path', 'path'],
            default=os.getcwd(),
            help='项目工作目录',
        ),

}


def common_click_options_hook(kwargs):
    if path := kwargs.get('path'):
        os.chdir(path)

    if project := kwargs.get('project'):
        configure.project_package_path = project


class UtilsCommandMeta(type):
    """Metaclass of UtilsCommand to add command into cli automatically ."""

    def __new__(mcs, name, bases, attrs: dict):
        attrs['name'] = attrs.get('name', name)
        attrs['logger'] = attrs.get('logger', getLogger(name.lower()))
        utils_command_class = type.__new__(mcs, name, bases, attrs)

        # add into cli group and skip the base command
        if name != 'UtilsCommand':
            cli.add_command(utils_command_class.click_command())
        return utils_command_class


class UtilsCommand(object, metaclass=UtilsCommandMeta):
    """The base command class of ScrapyUtils"""
    logger: Logger

    activated_common_options: List[str] = []

    @classmethod
    def click_command(cls) -> click.Command:
        """The click command to generate cli program.

        The UtilsCommand have a common click command with "project" arguments and "path" options.
        """

        def inner_callback(**kwargs):
            common_click_options_hook(kwargs)
            cls.logger.info(f'Command {cls.__name__} start.')
            cls.command_callback(**kwargs)

        cmd = click.Command(name=cls.name, callback=inner_callback, help=cls.__doc__)

        for activated_common_option in cls.activated_common_options:
            cmd.params.append(common_option.get(activated_common_option))
        logger.info(f'common options: {[_ for _ in cls.activated_common_options]}')
        return cmd

    @classmethod
    @abstractmethod
    def command_callback(cls, **kwargs):
        """"""
        raise NotImplementedError('Command must have their own execute() method.')


from ScrapyUtils.command import execute, generate, download, parsing
