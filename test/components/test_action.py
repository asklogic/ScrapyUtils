import unittest
from typing import *
from types import *

from base.components import Prepare
from base.components import Action, Parse, Scheme
from base.components import Processor
from base.components import Model
from base.components.model import Field
from base.components.base import Component
from base.libs.scraper import Scraper

from base.libs.setting import Setting
from base.libs.task import Task


class ParamAction(Action):

    def scraping(self, task: Task, scraper: Scraper) -> str:
        pass


class URIAction(Action):
    def scraping(self, task: Task, scraper: Scraper) -> str:
        pass
