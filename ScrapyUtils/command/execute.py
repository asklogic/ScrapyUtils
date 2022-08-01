# -*- coding: utf-8 -*-
"""普通单次爬取.

Todo:
    * For module TODOs
    
"""

from ScrapyUtils.command import UtilsCommand
from ScrapyUtils import configure
from ScrapyUtils.core import start_engine
from ScrapyUtils.core.end import end
from ScrapyUtils.core.engine import exit_engine


class Execute(UtilsCommand):
    """Execute some fixed tasks which generate by task_generate()."""

    name: str = 'execute'

    # some fixed option
    activated_common_options = ['path', 'project']

    @classmethod
    def command_callback(cls, **kwargs):
        """"""
        start_engine()

        # Load Task
        for task in configure.tasks_callable():
            configure.tasks.put(task)

        configure.tasks.join()

        exit_engine()
