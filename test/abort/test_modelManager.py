import unittest
from unittest import TestCase

import sys

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base.Model import ModelManager, ProxyModel, FailedTaskModel


class TestModelManager(TestCase):

    def test_init(self):
        ModelManager.add_model(ProxyModel)
        print(ModelManager.registered)
        [ModelManager.model("ProxyModel") for i in range(5000)]
        print([ModelManager.model("ProxyModel") for i in range(10)])
        pass

    def test_model(self):
        ModelManager.add_model(ProxyModel)

        self.assertRaises(KeyError, ModelManager.model, "o1")


if __name__ == '__main__':
    unittest.main()
