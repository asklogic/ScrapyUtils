import unittest

from base import core
from base.lib import Setting, BaseSetting
from base.Prepare import Prepare


class TestSetting(unittest.TestCase):

    def setUp(self) -> None:
        self.prepare: Prepare = core.load_components('TestMock')[0]

        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_init(self):
        setting = Setting()

        self.assertEqual(setting.SchemeList, [])
        self.assertEqual(setting.Thread, 5)
        self.assertEqual(setting.Block, 0.5)

    def test_load_prepare(self):
        setting = Setting()

        setting.load_prepare(self.prepare)

        self.assertNotEqual(setting.SchemeList, [])
        self.assertEqual(len(setting.SchemeList), 2)

        # default
        self.assertEqual(setting.Thread, 5)
        # custom
        self.assertEqual(setting.Block, 1)


    def test_load_config(self):
        setting = Setting()

        setting.load_config(__import__('config'))
        setting.load_prepare(self.prepare)


        # default
        self.assertEqual(setting.Thread, 5)

        # prepare custom
        self.assertEqual(setting.Block, 1)

        # config custom
        self.assertEqual(setting.FailedBlock, 10)

