import unittest
from unittest import TestCase

import sys

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base import core
from base import lib as Lib
from base import *


class Engine_Core_Test(TestCase):
    def test_single(self):
        """
        single run test
        :return:
        """

        test_conf = {
            "job": "hope",
            "allow": [],
            "model": 'ProxyModel',

        }
        config = Lib.Config(test_conf)

        self.assertIsInstance(config, Lib.Config)

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
