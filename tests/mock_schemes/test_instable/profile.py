# -*- coding: utf-8 -*-
"""
scheme's profile for atom scheme.

generate by Generate command.
"""

from base.libs import Task

THREAD = 2
TIMEOUT = 0.1


# generator your tasks in here.

def generate_tasks(**kwargs):
    for i in range(20):
        t = Task(url='http://127.0.0.1:8090/mock/random/violation')
        yield t


# setting your scraper here.
# default scraper is RequestScraper.
def generate_scraper(**kwargs):
    pass
