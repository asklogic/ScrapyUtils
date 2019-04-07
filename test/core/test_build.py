from unittest import TestCase
from typing import *
from types import *

from base import core, common, command
from base.lib import BaseSetting, Setting


class TestBuild(TestCase):

    def tearDown(self) -> None:
        super().tearDown()

    def setUp(self) -> None:
        target_name = "TestMock"
        modules: List[ModuleType] = core.load_files(target_name)
        prepare, schemes, models, processors = core.load_components(modules, target_name=target_name)

        self.prepare = prepare
        self.schemes = schemes
        self.models = models
        self.processors = processors

        super().setUp()

    def test_prepare(self):
        scraper, tasks = core.build_prepare(self.prepare)
        setting = self.prepare.generate()
