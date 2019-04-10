from unittest import TestCase
from typing import *
from types import *
import unittest

from base import core, common, command

from base.log import act, status
from base.lib import Config, ComponentMeta, Component,Setting
from base.task import Task
from base.Prepare import Prepare, DefaultRequestPrepare
from base.Model import Model, TaskModel, ProxyModel, ModelManager, ModelMeta
from base.scheme import Action, Parse
from base.Process import Processor, Pipeline
from base.common import Proxy_Processor, DefaultAction, DefaultXpathParse
from base.hub import Hub
from base.Scraper import Scraper
from base.scheme import Scheme


class TestBuild(TestCase):

    def tearDown(self) -> None:
        super().tearDown()

    def setUp(self) -> None:
        # target_name = "TestMock"
        # modules: List[ModuleType] = core.load_files(target_name)

        self.normal = core.load_components('TestMock')
        # prepare, schemes, models, processors = core.load_components(modules, target_name=target_name)

        # modules = core.load_files('TestMockError')
        self.failed = core.load_components('TestMockError')

        from base.log import act
        act.disabled = True

    def test_build_components(self):
        current_target = 'TestMock'
        prepare, schemes, models, processors = core.load_components(current_target)

        self.assertTrue(issubclass(prepare, Prepare))
        [self.assertTrue(issubclass(x, Scheme)) for x in schemes]
        [self.assertTrue(issubclass(x, Model)) for x in models]
        [self.assertTrue(issubclass(x, Processor)) for x in processors]

    def test_build_components_failed(self):
        with self.assertRaises(ModuleNotFoundError):
            current_target = 'TestMockFailed'
            prepare, schemes, models, processors = core.load_components(current_target)

    def test_build_components_not_exist(self):
        with self.assertRaises(ModuleNotFoundError):
            current_target = 'TestMockNotExist'
            prepare, schemes, models, processors = core.load_components(current_target)


    def test_build_prepare(self):
        scraper, tasks = core.build_prepare(prepare=self.normal[0])
        scraper.quit()

    def test_build_thread_prepare(self):
        scrapers, tasks = core.build_thread_prepare(prepare=self.normal[0], thread=5)
        [x.quit() for x in scrapers]

    def test_build_prepare_failed(self):
        with self.assertRaises(Exception) as e:
            scraper, tasks = core.build_prepare(prepare=self.failed[0])
            scraper.quit()
        self.assertIn('build_prepare failed', str(e.exception))

    def test_load_setting(self):

        setting = core.load_setting(self.normal[0])

        self.assertIsInstance(setting, Setting)

        self.assertEqual(setting.Thread, 15)
        self.assertEqual(len(setting.Scheme), 3)

    @unittest.skip
    def test_load_setting_failed(self):
        self.fail()

    def test_build_scheme(self):
        pass

    def test_demo(self):
        pass

