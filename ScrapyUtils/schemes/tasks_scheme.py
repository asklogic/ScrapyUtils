# -*- coding: utf-8 -*-
"""Task scheme.

根据函数定义新的Tasks，或者读取上次未爬取完成的Tasks.

Todo:
    * load_remains
    
"""

from queue import Queue

from .scheme import Scheme

from ScrapyUtils import configure

tasks = configure.tasks
tasks_callable = configure.tasks_callable


class TasksScheme(Scheme):
    pass


def load_remains():
    pass


def load_iterator():
    for task in tasks_callable:
        tasks.put(task)


@TasksScheme.register_start
def build_tasks():
    if False:
        load_remains()
    else:
        load_iterator()
