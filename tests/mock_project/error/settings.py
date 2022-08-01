# -*- coding: utf-8 -*-
"""
Setting for Error scheme.

generate by Generate command.
"""

from ScrapyUtils.libs import Task

THREAD: int = 2
"""The thread number"""
DELAY = 2
"""The delay for every task."""
RETRY: int = 3
"""The retry times."""
TIMEOUT: int = 15
"""The limit of a single task execute time."""


# generator your tasks in here.

def generate_tasks(**kwargs):
    for i in range(10):
        t = Task(url='http://yoursite.com')
        yield t


# setting your scraper here.
# default scraper is RequestScraper.
def generate_scraper(**kwargs):
    pass

# from os.path import join, sep

# DOWNLOAD_SUFFIX = 'html'
# DOWNLOAD_FOLDER = join('{class_name}', 'download')
# DOWNLOAD_PATH =
