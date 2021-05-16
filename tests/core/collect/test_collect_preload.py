import unittest
import os
import sys
from importlib import import_module
from queue import Queue

from ScrapyUtils import configure
from ScrapyUtils.core.preload import initial_configure

# add mock work path
from tests import telescreen


class TestCollectPreloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # sys.path.remove(os.getcwd())
        pass

    def test_sample(self):
        import lianjia

        pass

    def test_method(self):
        """TODO"""
        self.assertEqual(True, False)

        # assert configure.scraper_callable
        # assert configure.tasks_callable

    # def test_variable(self):
    #     """import before preload."""
    #     assert steps_class is None
    #     assert processors_class is None
    #     assert scraper_callable is None
    #     assert tasks_callable is None
    #     assert config is None
    #
    # def test_variable_steps_class(self):
    #     collect_scheme_preload('test_preload')
    #
    #     # import steps_class after preload.
    #     from base.core.collect import steps_class
    #     assert steps_class is not None
    #
    # def test_variable_processors_class(self):
    #     pass
    #
    # @unittest.skip
    # def test_global_origin(self):
    #     collect_scheme_preload('test_preload')
    #     from base.core.collect import config
    #
    #     assert config.get('thread') == 2
    #     assert config.get('timeout') == 2
    #
    # # @unittest.skip
    # def test_global(self):
    #     collect_scheme_preload('test_preload')
    #     from base.core.collect import config, tasks_callable
    #
    #     assert config.get('thread') == 3
    #     assert config.get('timeout') == 0.5
    #
    #     assert len(list(tasks_callable())) == 10


if __name__ == '__main__':
    unittest.main()
