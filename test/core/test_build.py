from unittest import TestCase
from typing import *
from types import *
import unittest

from base import core, common, command
from base.lib import BaseSetting, Setting

from base.Scraper import Scraper, FireFoxScraper, RequestScraper
from base.task import Task

from base.Model import ModelManager, TaskModel


class TestBuild(TestCase):

    def tearDown(self) -> None:
        super().tearDown()

    def setUp(self) -> None:
        target_name = "TestMock"
        modules: List[ModuleType] = core.load_files(target_name)

        self.normal = core.load_components(modules, target_name=target_name)
        # prepare, schemes, models, processors = core.load_components(modules, target_name=target_name)

        modules = core.load_files('TestMockError')
        self.failed = core.load_components(modules, 'TestMockError')

        super().setUp()



    def test_build_components(self):
        current_target = 'TestMock'
        prepare, schemes, models, processors = core.load_components(current_target)

    def test_build_components_failed(self):
        self.fail()

    def test_build_prepare(self):
        scraper, tasks = core.build_prepare(prepare=self.normal[0])
        scraper.quit()

    def test_build_thread_prepare(self):
        scrapers, tasks = core.build_thread_prepare(prepare=self.normal[0], thread=5)
        [x.quit() for x in scrapers]

    @unittest.skip
    def test_build_prepare_failed(self):
        with self.assertRaises(Exception) as e:
            scraper, tasks = core.build_prepare(prepare=self.failed[0])
            scraper.quit()
        self.assertIn('build_prepare failed', str(e.exception))

    def test_load_setting(self):
        self.fail()

    def test_load_setting_failed(self):
        self.fail()


    def test_build_scheme(self):
        pass

    def test_demo(self):
        pass
