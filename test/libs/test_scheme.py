import unittest
from typing import *

from base import core
from base.lib import Setting, BaseSetting
from base.Prepare import Prepare

from base.scheme import Scheme


class TestScheme(unittest.TestCase):

    def setUp(self) -> None:
        self.normal = core.load_components('TestMock')

        self.normal_setting = core.load_setting(self.normal[0])

        self.prepare: Prepare = self.normal[0]
        self.schemes: List[Scheme] = self.normal_setting.SchemeList

        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_init(self):
        pass
