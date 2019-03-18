import unittest
from unittest import TestCase

import sys

sys.path.insert(0, r"E:\cloudWF\python\ScrapyUtils")

from base.Prepare import Prepare
from base.Model import Model
from base.scheme import Action, Parse
from base.Process import Processor

import base.core as core
import threading


class TestCore(TestCase):

    def test_component_loading(self):
        return
        # init prepare
        print("### init prepare ###")

        pm = core._load_module("scjst", "prepare")

        prepare = core._load_component(pm, Prepare)

        print(prepare)

        actives = [x for x in prepare if x._active]

        print(actives)

        currnet_prepare: Prepare = actives[0]

        # init model
        print("### init model ###")

        mm = core._load_module("scjst", "model")
        model = core._load_component(mm, Model)

        print(model)

        actives = [x for x in model if x._active]

        print(actives)

        # init scheme
        print("### init scheme ###")
        schemeList = currnet_prepare.schemeList
        print(schemeList)

        # init process
        print("### init process ### ")

        pm = core._load_module("scjst", "process")
        processor = core._load_component(pm, Processor)

        print(processor)

        actives = [x for x in processor if x._active]
        print(actives)

    def test_single(self):
        return
        target = "ReCore"
        prepare = core.initPrepare(target)

        scheme = [x() for x in prepare.scheme]

        model = core.initModel(target)

        processors = core.initProcessor(target)

        scraper = prepare.get_scraper()
        task = prepare.get_tasks()

        sys_hub, dump_hub = core.build_hub(model, processors)

        sys_hub.activate()
        dump_hub.activate()

        # core.scrapy(scheme, scraper, task[0], dump_hub)

        dump_hub.stop()
        sys_hub.stop()

    def test_thread_run(self):
        return

        target = "ReCore"

        prepare = core.initPrepare(target)
        prepare.Thread = 2
        prepare.Block = 0.1
        prepare.ProxyAble = False

        barrier = threading.Barrier(prepare.Thread)
        core.barrier = barrier

        processors = core.initProcessor(target)
        model = core.initModel(target)

        sys_hub, dump_hub = core.build_hub(model, processors)

        # proxy
        if not prepare.ProxyAble:
            sys_hub.remove_pipeline("ProxyModel")
        else:
            core.temp_appendProxy(sys_hub, prepare.Thread)

        sys_hub.activate()
        dump_hub.activate()

        # append init task
        for t in core.generate_task(prepare):
            sys_hub.save(t)

        thread_List = []

        for i in range(prepare.Thread):
            t = core._ScrapyThread(sys_hub=sys_hub, dump_hub=dump_hub, prepare=prepare)
            thread_List.append(t)
            t.setDaemon(True)
            t.start()

        [t.join() for t in thread_List]
        sys_hub.stop()
        dump_hub.stop()
