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
from base.hub import Hub
from base.Scraper import Scraper
from base.scheme import Scheme

from base import core
import os

import threading


class TestEngine(TestCase):

    def setUp(self) -> None:
        # mock env

        # set test path
        import sys
        core.path = r'E:\cloudWF\python\ScrapyUtils\test'
        sys.path.append(r'E:\cloudWF\python\ScrapyUtils\test')

        super().setUp()

    def _test_single_run(self):
        target_name = "TestMockSingle"
        # step 1 & 2: load components
        components = core.load_components(target_name)
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

        current_task = tasks[0]

        core.load_context(current_task, schemes)

        # step 3.4: build hubs
        sys_hub, dump_hub = core.build_hub(models, processors, prepare.setting)

        sys_hub.activate()
        dump_hub.activate()

        # step 4: Scrapy
        core.scrapy(schemes, scraper, current_task, dump_hub, sys_hub)

        for i in range(15):
            model = dump_hub.pop("TestMockSingleModel")
            self.assertIsInstance(model, Model)

        # step 5: Scrapy
        scraper.quit()
        dump_hub.stop()
        sys_hub.stop()

    def _test_thread_run(self):
        target_name = "TestMockThread"
        # step 1 & 2: load components
        components = core.load_components(target_name)
        prepare, schemes, models, processors = components

        # step 3: build components

        thread = prepare.Thread

        # step 3.1: build thread scraper list
        scraper_list, tasks = core.build_thread_prepare(prepare, thread)

        for scraper in scraper_list:
            # print(scraper)
            # print(id(scraper))
            self.assertIsInstance(scraper, Scraper)

        for task in tasks:
            self.assertIsInstance(task, Model)

        # step 3.2: build thread scheme list ( context
        schemes_list = core.build_thread_schemes(schemes, thread)

        for thread_schemes in schemes_list:
            for scheme in thread_schemes:
                # print(scheme)
                # print(id(scheme))
                self.assertIsInstance(scheme, Scheme)

        # step 3.3: build hub
        sys_hub, dump_hub = core.build_hub(models, processors, prepare.setting)

        # temp
        # TODO
        if not prepare.ProxyAble:
            sys_hub.remove_pipeline("ProxyModel")
        else:
            core.temp_appendProxy(sys_hub, prepare.Thread)

        sys_hub.activate()
        dump_hub.activate()

        for task in tasks:
            sys_hub.save(task)

        # step 4: init thread
        core.barrier = threading.Barrier(prepare.Thread)

        thread_List = []

        for i in range(prepare.Thread):
            t = core.ScrapyThread(sys_hub=sys_hub, dump_hub=dump_hub, prepare=prepare, schemes=schemes_list[i],
                                  scraper=scraper_list[i])
            thread_List.append(t)
            t.setDaemon(True)
            t.start()

        [t.join() for t in thread_List]

        # step 5: run command

        # step 6: exit

        sys_hub.stop()
        dump_hub.stop()

    def test_thread_run(self):
        target_name = "TestMockThread"
        setting = core.build_setting(target_name)

        # temp
        setting.Thread = 1

        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)
        schemes = core.build_schemes(setting.CurrentSchemeList)

        sys_hub, dump_hub = core.build_hub(setting=setting)

        # assert

        self.assertIs(len(setting.CurrentSchemeList), 2)
        self.assertIs(setting.CurrentSchemeList[0]._name, 'TestPageAction')
        self.assertIs(setting.CurrentSchemeList[1]._name, 'Mapping')

        self.assertIs(len(setting.CurrentModels), 1)
        self.assertIs(setting.CurrentModels[0]._name, 'TestMockThreadModel')

        self.assertIs(len(setting.CurrentProcessorsList), 1)
        self.assertIs(setting.CurrentProcessorsList[0]._name, 'TestMockThreadProcess')

        sys_hub.activate()
        dump_hub.activate()

        ##### no task
        # for task in tasks:
        #     sys_hub.save(task)

        thread_List = []
        for i in range(setting.Thread):
            t = core.ScrapyThread(sys_hub, dump_hub, schemes, scrapers[i], setting)
            thread_List.append(t)
            t.setDaemon(True)
            t.start()

        [t.join() for t in thread_List]
        sys_hub.stop()
        dump_hub.stop()
