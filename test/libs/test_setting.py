import unittest

from base import core
from base.lib import Setting, BaseSetting

from base.Prepare import Prepare
from base.scheme import Scheme, Action, Parse
from base.Model import Model
from base.Process import Processor


class TestSetting(unittest.TestCase):

    def setUp(self) -> None:
        self.prepare: Prepare = core.load_components('TestMock')[0]

        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_init(self):
        # init
        setting = Setting()

        # default
        self.assertEqual(setting.SchemeList, [])
        self.assertEqual(setting.Thread, 5)
        self.assertEqual(setting.Block, 0.5)

    def test_build_demo(self):
        target = 'TestMock'

        # 1. init object
        setting = Setting()
        setting.Target = target

        # 2. load config.py
        config = __import__('config')
        setting.load_config(config)

        # TODO refact
        # 从setting中剥离
        # 3. load components
        components = core.load_components(target)
        setting.check_components(components)
        # overwrite prepare

        # 4. add default and check
        setting.check(components)

        # assert type
        self.components_type(setting)

    def components_type(self, setting: Setting):
        self.assertTrue(issubclass(setting.CurrentPrepare, Prepare))

        [self.assertTrue(issubclass(x, Scheme)) for x in setting.CurrentSchemeList]
        [self.assertTrue(issubclass(x, Model)) for x in setting.CurrentModels]
        [self.assertTrue(issubclass(x, Processor)) for x in setting.CurrentProcessorsList]

    def test_load_prepare(self):
        setting = Setting()

        components = core.load_components('TestMock')
        setting.check_components(components)
        setting.load_prepare()

        # default
        self.assertEqual(setting.Thread, 5)
        # custom
        self.assertEqual(setting.Block, 1)

    def test_build_setting(self):
        target = 'TestMock'
        setting: Setting = core.build_setting(target)

        self.assertIsInstance(setting, Setting)

    def test_load_config(self):
        setting = Setting()

        setting.load_config(__import__('config'))

        # default
        self.assertEqual(setting.Thread, 5)

        # prepare custom
        self.assertEqual(setting.Block, 2.2)

        # config custom
        self.assertEqual(setting.FailedBlock, 5)

    def test_custom_setting(self):
        target = 'TestMockCustom'

        setting = core.build_setting(target=target)

        self.assertEqual(setting.Block, 0.4)
        self.assertEqual(setting.ProxyURL,
                         'https://docs.python.org/3/library/urllib.request.html#module-urllib.request')

        self.assertEqual(len(setting.CurrentModels), 2)
        self.assertEqual(setting.CurrentSchemeList[1]._name, 'TestAction')

        self.assertEqual(len(setting.CurrentProcessorsList), 2)
        # fixme 顺序问题
        # self.assertEqual(setting.CurrentProcessorsList[0]._name, 'TestMockCustomProcess')

        self.components_type(setting=setting)

    def test_error_file_setting(self):
        target = 'TestMockErrorFile'

        with self.assertRaises(ModuleNotFoundError) as e:
            setting = core.build_setting(target=target)

        self.assertIn('No module named', str(e.exception))

    def test_failed_setting(self):
        target = 'TestMockFailed'
        # 由于prepare import 各组件 导致不能缺少任意一个component file
        setting = core.build_setting(target=target)

        # abort
        # 转为component加载出错用例

    def test_error_component_setting(self):
        target = 'TestMockErrorCom'
        with self.assertRaises(KeyError) as e:
            setting = core.build_setting(target=target)

        self.assertIn('cannot found ', str(e.exception))

    def test_error_target(self):
        target = 'TestMockNotExist'

        with self.assertRaises(ModuleNotFoundError) as e:
            setting = core.build_setting(target=target)

        self.assertIn('cannot found target named', str(e.exception))
