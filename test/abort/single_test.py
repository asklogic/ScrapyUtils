import unittest
from unittest import TestCase

import sys

import base.components.model

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")


class do_core_Test(TestCase):
    # def test_generator(self):
    # import os
    # from os import path
    #
    # from base import generator
    # p = generator.PROJECT_PATH
    #
    # self.assertEqual(1, 2)

    def test_core(self):
        import base._core as core
        from base.libs.task import Task
        import base.libs.scraper as s
        import base.Model as m

        # prepare
        scraper, task = core.do_prepare("default", "")

        self.assertIsInstance(scraper, s.RequestScraper)
        self.assertIsInstance(task[0], Task)
        # self.assertEqual(task[0].param, "1")  # Done

        # model and manager
        from hope.model import ProxyModel
        models = core.load_models([], "hope")
        manager = core.register_manager([], "hope")

        self.assertEqual(core.load_models([], "hope"), [ProxyModel])
        self.assertEqual(core.load_models(["nope"], "hope"), [])

        self.assertIsInstance(manager, base.components.model.ModelManager)
        self.assertEqual(manager.get("ProxyModel"), [])

        # load scheme
        from base.common import DefaultXpathParse
        # Done
        schemes = core.load_scheme(["xpath"], 'hope')
        self.assertEqual(schemes[0], DefaultXpathParse)

        # Done
        # self.assertEqual(core.load_conserve(), DefaultConserve)

        conserve = core.load_conserve()

        # self.assertEqual(core.load_scheme(["new"], 'hope')[0], newAction)
        # core.scrapy(scheme_list=schemes, scraper=scraper, task=task[0], manager=manager)
        core.do_conserve(manager, conserve)

        # self.assertEqual(manager.get("ProxyModel")[0].ip, "12")

if __name__ == '__main__':
    unittest.main()
