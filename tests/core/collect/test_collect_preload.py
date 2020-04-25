import unittest
import os
import sys
from importlib import import_module
from queue import Queue

from base.core import collect_scheme_initial, collect_scheme_preload

from base.core.collect import steps_class, processors_class, tasks_callable, scraper_callable, config

from tests import telescreen


class TestCollectPreloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # sys.path.remove(os.getcwd())
        pass

    def test_test(self):
        # global_profile = import_module('profile')
        global_profile = __import__('settings')

    def test_demo(self):
        collect_scheme_preload('test_preload')

    def test_variable(self):
        """
        import before preload.
        """
        assert steps_class is None
        assert processors_class is None
        assert scraper_callable is None
        assert tasks_callable is None
        assert config is None

    def test_variable_steps_class(self):
        collect_scheme_preload('test_preload')

        # import steps_class after preload.
        from base.core.collect import steps_class
        assert steps_class is not None

    def test_variable_processors_class(self):
        pass

    @unittest.skip
    def test_global_origin(self):
        collect_scheme_preload('test_preload')
        from base.core.collect import config

        assert config.get('thread') == 2
        assert config.get('timeout') == 2

    # @unittest.skip
    def test_global(self):
        collect_scheme_preload('test_preload')
        from base.core.collect import config, tasks_callable

        assert config.get('thread') == 3
        assert config.get('timeout') == 0.5

        assert len(list(tasks_callable())) == 10


if __name__ == '__main__':
    unittest.main()
