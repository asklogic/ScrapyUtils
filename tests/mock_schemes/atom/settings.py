# -*- coding: utf-8 -*-
"""
scheme's profile for atom scheme.

generate by Generate command.
"""

from ScrapyUtils.libs import Task

THREAD = 2
TIMEOUT = 2

PROXY = False
PROXY_URL = ''


# generator your tasks in here.

def generate_tasks(**kwargs):
    for i in range(10):
        t = Task(url='http://127.0.0.1:8090/mock/random/dynamic')
        yield t


# setting your scraper here.
# default scraper is RequestScraper.
def generate_scraper(**kwargs):
    pass
