from unittest import TestCase
from typing import *
from types import ModuleType

from base import core
from base import common, command

from base.log import act, status
from base.lib import Config, ComponentMeta, Component
from base.task import Task
from base.Prepare import Prepare, DefaultRequestPrepare
from base.Model import Model, TaskModel, ProxyModel, ModelManager, ModelMeta
from base.scheme import Action, Parse
from base.Process import Processor, Pipeline
from base.common import Proxy_Processor
from base.hub import Hub
from base.Scraper import Scraper
from base.scheme import Scheme

from base import core
import os


class TestEngine(TestCase):

    def setUp(self) -> None:
        # mock env

        # set test path
        core.path = r'E:\cloudWF\python\ScrapyUtils\test'

        super().setUp()

    def _test_init(self):
        # step 1: load files
        target_name = "TestMock"
        modules: List[ModuleType] = core.load_files(target_name)

        # not exist target project
        # not complete files

        # step 2: load components

        components = core.load_components(modules, target_name=target_name)

        prepare, schemes, models, processors = components

        # must have prepare component ( or not?
        # default scheme component
        # TODO

        # step 3: build component

        scraper, tasks = core.build_prepare(prepare)
        sys_hub, dump_hub = core.build_hub(modules, processors, prepare.setting)

        # step 3.1: thread

        thread_shemes: List[List[Scheme]] = core.build_thread_shemes(schemes)
        thread_scraper: List[scraper] = core.build_thread_scrapers(scraper)

        # step4 : wait and finish

        sys_hub.activate()
        dump_hub.activate()

        # core.scrapy(scheme_list=schemes, scraper=scraper, task=tasks[0], dump_hub=dump_hub, sys_hub=sys_hub)

        sys_hub.stop()
        dump_hub.stop()

    def _test_thread_run(self):

        target_name = "TestMock"

        # step 1: load files
        modules: List[ModuleType] = core.load_files(target_name)

        # not exist target project
        # not complete files

        # step 2: load components

        components = core.load_components(modules)
        prepare, schemes, models, processors = components

        pass

    def test_single_run(self):
        target_name = "TestMock"
        # step 1: load files
        modules: List[ModuleType] = core.load_files(target_name)

        # step 2: load components
        components = core.load_components(modules, target_name=target_name)
        prepare, schemes, models, processors = components

        # step 3: build components

        # step 3.1: build single scraper
        scraper, tasks = core.build_prepare(prepare)

        for task in tasks:
            self.assertIsInstance(task, TaskModel)
        self.assertIsInstance(scraper, Scraper)

        # step 3.2: build single schemes
        schemes = core.build_schemes(schemes)

        # step 3.3: build context
        current_task = task[0]
        if current_task.param and type(current_task.param) is dict:
            for key, item in current_task.param.items():
                schemes[0].context[key] = item

        # step 3.4: build hubs
        sys_hub, dump_hub = core.build_hub(models, processors, prepare.setting)

        # step 4: Scrapy
        core.scrapy(schemes, scraper, current_task, dump_hub, sys_hub)

        # step 5: Scrapy
        scraper.quit()
        dump_hub.stop()
        sys_hub.stop()

    def test_core_load_files(self):
        target_name = "TestMockThread"
        # step 1: load files
        modules: List[ModuleType] = core.load_files(target_name)

        # step 2: load components
        components = core.load_components(modules, target_name=target_name)
        prepare, schemes, models, processors = components

        # step 3: build components

        # step 3.1: build thread scraper list
        scraper_list, tasks = core.build_thread_prepare(prepare, thread)

        # step 3.2: build thread scheme list ( context
        schemes_list = core.build_thread_schemes(schemes, thread)

        # step 3.3: build hub
        sys_hub, dump_hub = core.build_hub(models, processors, prepare.setting)

        # step 4: init thread

        # step 5: run command

        # step 6: exit

    def test_core_load_files_no_preapre(self):
        target_name = "TestMockFailed"

        # not have prepare

        self.assertRaises(ModuleNotFoundError, core.load_files, target_name)
        # modules: List[ModuleType] = core.load_files(target_name)

    def test_load_component(self):
        target_name = "TestMock"
        modules: List[ModuleType] = core.load_files(target_name)
        prepare, schemes, models, processors = core.load_components(modules, target_name=target_name)

        self.assertTrue(issubclass(prepare, Prepare))
        for scheme in schemes:
            self.assertTrue(issubclass(scheme, Scheme))
        for model in models:
            self.assertTrue(issubclass(model, Model))
        for processor in processors:
            self.assertTrue(issubclass(processor, Processor))

        # 不为空
        self.assertNotEqual(schemes, [])
        # TODO

    def __test_load_component_default(self):
        # abort
        target_name = "TestMockSimple"
        modules: List[ModuleType] = core.load_files(target_name)
        prepare, schemes, models, processors = core.load_components(modules, target_name=target_name)

        self.assertTrue(issubclass(prepare, Prepare))
