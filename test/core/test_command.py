from unittest import TestCase
from typing import *
from types import *

from base import core
from base import common, command

from base.log import act, status
from base.lib import Config, ComponentMeta, Component
from base.task import Task
from base.Prepare import Prepare, DefaultRequestPrepare
from base.Model import Model, TaskModel, ProxyModel, ModelManager, ModelMeta
from base.scheme import Action, Parse
from base.Process import Processor, Pipeline
from base.hub import Hub
from base.Scraper import Scraper
from base.scheme import Scheme



class TestCommand(TestCase):

    def test_run(self):

        pass