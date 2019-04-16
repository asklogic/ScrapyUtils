import unittest
from unittest import TestCase

import sys

import base.common
import base.task

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base import lib as Lib
from base import Action
from base import Scraper
from base import Conserve
from base import Prepare
from base import Container
from base import Model
from base import _core


class Engine_Core_Test(TestCase):
    def test_single(self):
        """
        single run test
        :return:
        """

        test_conf = {
            "job": "hope",
            "allow": [
                "xpath",
            ],
            "models": [
                'ProxyInfoModel'
            ],
            "prepare": "test_prepare",
            "conserve": "test_conserve",

        }
        config = Lib.Config(test_conf)

        self.assertIsInstance(config, Lib.Config)

        # prepare 是类方法 不需要实例化

        scraper, task = _core.do_prepare(config.prepare, config.job)

        self.assertIsInstance(scraper, Scraper.Scraper)
        self.assertIsInstance(task[0], base.task.Task)

        # conserve
        conserve = _core.load_conserve(config.conserve, config.job)
        current_conserve = _core.build_conserve(conserve)

        self.assertTrue(issubclass(conserve, Conserve.Conserve))
        self.assertTrue(hasattr(current_conserve, "data"))
        self.assertIsInstance(current_conserve, Conserve.Conserve)

        # models
        models = _core.load_models(config.models, config.job)
        self.assertEqual(len(models), 3)

        # container

        containers = _core._register_containers(models, config.job)

        for container in containers:
            # self.assertIsInstance(container, Container.Container)
            self.assertTrue(issubclass(containers[container].__class__, Container.Container))

        # manager
        manager = _core.register_manager(models=models)
        self.assertIsInstance(manager, Model.ModelManager)

        # scheme
        schemes = _core.load_scheme(config.schemes, config.job)

        # core.scrapy(scheme_list=schemes,manager=manager,task=task[0],scraper=scraper)

        _core.do_conserve(manager=manager, conserve=conserve)

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()