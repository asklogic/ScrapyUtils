import unittest
from unittest import TestCase

import sys

sys.path.insert(0, r"E:\cloudWF\python\ScrapyUtils")
from base.lib import Config

import scrapy_config
from base.Prepare import Prepare
from base.Model import Model
from base.Action import Action
from base.Parse import Parse

import base.core as core


class TestCore(TestCase):
    def setUp(self):
        mock_config = {
            "job": "core_test",
            "allow": [
                "CoreTestAction",
                # "CoreTestNextAction",
                # "CoreTestParse",
                "CoreProxyTestParse",
            ],
            "process": [
                "CoreTestProcessor",
                "CoreOtherTestProcessor",
            ],
            "model": [
                "CoreTestModel",
                "IpModel",
            ],
            "prepare": "CoreTestPrepare",
        }
        self.config = Config(mock_config)

    def tearDown(self):
        pass



    def test_single(self):
        self.assertEqual(1, 1)

        con = self.config

        prepare = core.load_prepare(con)

        processor = core.load_processor(con)

        model = core.load_model(con)

        scheme = core.load_scheme(con)

        scraper, task = core.build_prepare(prepare)

        # print(scheme)
        # print(task)
        # print(scraper)

        # sys_hub, dump_hub = core.build_Hub(model, processor)

        # core.scrapy(scheme, scraper, task[0], dump_hub)

        # dump_hub.stop()

    def test_thread(self):
        return

        con = self.config

        prepare = core.load_prepare(con)

        processor = core.load_processor(con)

        model = core.load_model(con)

        # scheme = core.load_scheme(con)

        sys_hub, dump_hub = core.build_Hub(model, processor)

        # init prepare
        for t in core.generate_task(prepare):
            sys_hub.save(t)

        thread_List = []

        for i in range(scrapy_config.Thread):
            t = core.ScrapyThread(sys_hub=sys_hub, dump_hub=dump_hub, config=con)
            thread_List.append(t)
            t.setDaemon(True)
            t.start()


        [t.join() for t in thread_List]
        sys_hub.stop()
        dump_hub.stop()

    def test_core_review(self):
        self.assertEqual(scrapy_config.Project_Path, "E:\cloudWF\python\ScrapyUtils")

    # target_path = "\\".join([scrapy_config.Project_Path, self.config.job])
    # self.assertEqual("\\".join([scrapy_config.Project_Path, self.config.job]),
    #                  r"E:\cloudWF\python\ScrapyUtils\core_test")
    #
    # sys.path.append(target_path)
    #
    # # 仅在job目录中存在
    # # 加载target file
    # target_process = __import__("process")
    # # target_processor = getattr(target_process, "CoreTestProcessor")
    # # print(target_processor)
    # # [print(x) for x in dir(target_processor)]
    # # [print(getattr(target_processor, x)) for x in dir(target_processor)]
    # # 寻找具体类
    # [print(getattr(target_process, x)) for x in self.config.process]
    #
    # # 在项目和job目录中都存在
    # # 加载target file
    # try:
    #     target_prepare = __import__(".".join([self.config.job, "prepare"]), fromlist=("prepare"))
    # except ModuleNotFoundError as e:
    #     target_prepare = __import__("prepare")
    #
    # print("###############\n")
    # try:
    #     target_prepareClass = getattr(target_prepare, self.config.prepare)
    # except AttributeError as e:
    #     target_prepare = __import__("prepare")
    #     # print("#####", target_prepare)
    #     # [print("### ", getattr(target_prepare, x)) for x in dir(target_prepare) if not x.startswith("_")]
    #     prepaer_list = [getattr(target_prepare, x) for x in dir(target_prepare) if not x.startswith("_")]
    #     [print(x) for x in prepaer_list if issubclass(x, Prepare) and x is not Prepare]
    #     # [print(x) for x in prepaer_list if isinstance(x, Prepare)]
    #
    #     # [print(x) for x in dir(target_prepare)]
    #     # target_prepareClass = getattr(target_prepare, self.config.prepare)
    #
    # # model
    # target_prepare = __import__("model")
    # # print([getattr(target_prepare, x) for x in dir(target_prepare) if not x.startswith("_")])
    # [print(i) for i in [getattr(target_prepare, x) for x in dir(target_prepare) if not x.startswith("_")] if
    #  issubclass(i, Model) and i is not Model]
    #
    # # scheme
    #
    # for i in ["action", "parse"]:
    #     target_scheme = __import__(i)
    #
    #
    #     [print("#",i) for i in [getattr(target_scheme, x) for x in dir(target_scheme) if not x.startswith("_")] if
    #      issubclass(i, Action) and i is not Action]
    #
    #     [print("#", i) for i in [getattr(target_scheme, x) for x in dir(target_scheme) if not x.startswith("_")] if
    #      issubclass(i, Parse) and i is not Parse]
