import unittest
from typing import *
from base import core
from base.libs.setting import BaseSetting, Setting

from base.components import Prepare, Scheme, Model, Processor, Action, Parse, Component


class TestSetting(unittest.TestCase):

    def setUp(self) -> None:
        self.prepare: Prepare = core.load_components('TestMock')[0]

        self.setting = core.build_setting('TestEmptyThread')

    def tearDown(self) -> None:
        super().tearDown()

    # test function
    def components_type(self, setting: Setting):
        self.assertTrue(issubclass(setting.CurrentPrepare, Prepare))

        [self.assertTrue(issubclass(x, Scheme)) for x in setting.CurrentSchemeList]
        [self.assertTrue(issubclass(x, Model)) for x in setting.CurrentModels]
        [self.assertTrue(issubclass(x, Processor)) for x in setting.CurrentProcessorsList]

    def test_init(self):
        # init
        setting = Setting()

        # default
        self.assertEqual(setting.SchemeList, [])
        self.assertEqual(setting.Thread, 5)
        self.assertEqual(setting.Block, 0.5)

    # function
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
        setting.default()

        # assert type
        self.components_type(setting)

    def test_build_setting(self):
        target = 'TestMock'
        setting: Setting = core.build_setting(target)

        self.assertIsInstance(setting, Setting)

    def test_load_prepare(self):
        setting = Setting()

        components = core.load_components('TestMock')
        setting.check_components(components)
        setting.load_prepare()

        # default
        self.assertEqual(setting.Thread, 5)
        # custom
        self.assertEqual(setting.Block, 1)

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

        # scheme

        self.assertEqual(len(setting.CurrentSchemeList), 3)

        self.assertEqual(setting.CurrentSchemeList[1]._name, 'TestAction')

        self.assertEqual(len(setting.CurrentModels), 2)

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

    def test_default(self):
        from base.common import XpathMappingParse
        target = 'TestMock'

        setting = Setting()
        setting.Target = target

        components = core.load_components(target)
        setting.check_components(components)

        setting.Mapping = True
        setting.MappingAutoYield = True

        setting.default()

        # scheme
        self.assertEqual(len(setting.CurrentSchemeList), 3)

        self.assertEqual(setting.CurrentSchemeList[1]._name, 'XpathMappingParse')

        schemes_list = core.build_thread_schemes(setting.CurrentSchemeList, 5)

        for schemes in schemes_list:
            mapping = schemes[1]
            mapping: XpathMappingParse
            self.assertEqual(mapping.get_name(), 'XpathMappingParse')
            self.assertIsInstance(mapping, object)

            # autoyield
            self.assertEqual(mapping.autoyield, True)
            # 2 个model
            self.assertEqual(len(mapping.models), 2)
            # mapper 为空
            [self.assertEqual(bool(x._mapper), False) for x in mapping.models]

    def test_setting_detail(self):
        setting = self.setting

        def components_detail(components: List[Component], head: str = 'components'):
            head = 'Activated {}:  {}\n'.format(head, len(components))
            content = '\n'.join(['\t{}) {}'.format(components.index(x), x.get_name()) for x in components])
            return head + content

        def detail(setting: Setting):
            res = []

            prepare: Prepare = setting.CurrentPrepare
            schemes: List[Scheme] = setting.CurrentSchemeList
            models: List[Model] = setting.CurrentModels
            processors: List[Processor] = setting.CurrentProcessorsList

            prepare_detail = 'Selected Prepare: {} - {}'.format(prepare.get_name(), str(prepare))

            schemes_head = 'Activated Model: {}\n'.format(len(models))
            schemes_list = '\n'.join(['\t{}) {}'.format(models.index(model) + 1, model.get_name()) for model in models])

            processor_head = 'Activated Processor: {}\n'.format(len(processors))
            processor_list = '\n'.join(['\t{}) {}'.format(processors.index(x) + 1, x.get_name()) for x in processors])

            scheme_head = 'Activated Scheme: {}\n'.format(len(schemes))
            scheme_list = '\n'.join(['\t{}) {}'.format(schemes.index(x) + 1, x.get_name()) for x in schemes])

            res.append(prepare_detail)
            res.append(schemes_head + schemes_list)
            res.append(scheme_head + scheme_list)
            # res.append(processor_head + processor_list)
            res.append(components_detail(processors, 'Processor'))
            return res

        detail_info = detail(setting)

        self.assertIsInstance(detail_info, list)

        print(detail_info[0])
        print(detail_info[1])
        print(detail_info[2])
        print(detail_info[3])
