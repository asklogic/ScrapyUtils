from unittest import TestCase

from base import core

from base.components.prepare import Prepare
from base.components.model import Model
from base.components.scheme import Scheme
from base.components.proceesor import Processor
from base.libs.scraper import Scraper, RequestScraper


class TestBuild(TestCase):

    def tearDown(self) -> None:
        super().tearDown()

    def setUp(self) -> None:
        # target_name = "TestMock"
        # modules: List[ModuleType] = core.load_files(target_name)

        self.normal = core.load_components('TestMock')
        self.normal_setting = core.build_setting('TestMock')

        self.custom_setting = core.build_setting('TestMockCustom')

        # prepare, schemes, models, processors = core.load_components(modules, target_name=target_name)

        # modules = core.load_files('TestMockError')
        # self.failed = core.load_components('TestMockErrorFile')
        self.failed_setting = core.build_setting('TestMockFailed')

        from base.log import act
        act.disabled = True

    def test_build_components(self):
        current_target = 'TestMock'
        prepares, schemes, models, processors = core.load_components(current_target)

        [self.assertTrue(issubclass(x, Prepare)) for x in prepares]
        [self.assertTrue(issubclass(x, Scheme)) for x in schemes]
        [self.assertTrue(issubclass(x, Model)) for x in models]
        [self.assertTrue(issubclass(x, Processor)) for x in processors]

    def test_build_components_failed(self):
        with self.assertRaises(ModuleNotFoundError) as e:
            current_target = 'TestMockErrorFile'
            prepare, schemes, models, processors = core.load_components(current_target)
        self.assertIn('No module named', str(e.exception))

    def test_build_components_not_exist(self):
        with self.assertRaises(ModuleNotFoundError) as e:
            current_target = 'TestMockNotExist'
            prepare, schemes, models, processors = core.load_components(current_target)

        self.assertIn('cannot found target named', str(e.exception))

    def test_build_prepare_default(self):
        with self.assertWarns(Warning) as w:
            scraper, tasks = core.build_prepare(self.normal_setting.CurrentPrepare)
            scraper.quit()
        self.assertIn('scraper_prepared must return a Scraper Instance', str(w.warning))

    def test_build_prepare_custom(self):
        scraper, tasks = core.build_prepare(self.custom_setting.CurrentPrepare)

        self.assertIsInstance(scraper, RequestScraper)

    def test_build_thread_prepare(self):
        scrapers, tasks = core.build_thread_prepare(prepare=self.custom_setting.CurrentPrepare,
                                                    thread=self.custom_setting.Thread)
        [self.assertIsInstance(x, Scraper) for x in scrapers]

        ids = [id(x) for x in scrapers]
        self.assertEqual(len(ids), len(set(ids)))
        [x.quit() for x in scrapers]

    def test_build_prepare_failed(self):
        with self.assertRaises(Exception) as e:
            scraper, tasks = core.build_prepare(prepare=self.failed_setting.Prepare)
            scraper.quit()
        self.assertIn('build_prepare failed', str(e.exception))

    def test_build_demo(self):
        '''
        build all components
        :return:
        '''
        setting = core.build_setting('TestMock')

        scrapers, tasks = core.build_thread_prepare(prepare=setting.CurrentPrepare,
                                                    thread=setting.Thread)
        schemes = core.build_schemes(setting.CurrentSchemeList)

        sys_hub, dump_hub = core.build_hub(setting=setting)
