import unittest

from base.core import collect

from tests.telescreen import schemes_path
from importlib import import_module

from base.components import *
from base.libs import *


class TestCollect(unittest.TestCase):

    def test_init_collect(self):
        """
        test_mock_scheme
        """

        # /tests/mock_schemes in sys.path
        with self.assertRaises(ModuleNotFoundError) as mnfe:
            import_module('not_exist')

        # case: test_collect_active (step)
        module = import_module('test_collect_active')

        assert len(module.steps) is 1
        assert module.steps[0].name == 'Actived'

        # case: test_collect_priority
        priority = import_module('test_collect_priority')

        assert len(priority.processors) == 3
        assert priority.processors[0].name == 'Duplication'
        assert priority.processors[1].name == 'Count'
        assert priority.processors[2].name == 'MysqlSave'

        # case: test_profile

        profile = import_module('test_profile')

        assert profile.config['thread'] is 2
        assert profile.config['timeout'] == 1.5
        assert callable(profile.scraper_callable)
        assert callable(profile.tasks_callable)

        tasks = profile.tasks_callable()
        assert len(list(tasks)) == 10

        # final case: atom

        atom = import_module('atom')

        # step
        assert len(atom.steps) is 4
        for step in atom.steps:
            assert issubclass(step, Step)

    def test_collect_scheme(self):
        """
        -> core.collect.collect_scheme
        method invoked before Command run.
        """

        collect.collect_scheme('atom')

        assert collect.steps
        assert len(collect.steps) == 4

        r = collect.scraper_generate
        assert callable(r)
        assert isinstance(r(), RequestScraper)

    def test_collect_scraper(self):
        """
        -> core.collect.collect_scheme
        method invoked before Command run.
        """

        collect.collect_scheme('atom')

        scraper_generate = collect.scraper_generate

        assert callable(scraper_generate)
        assert isinstance(scraper_generate(), Scraper)

    def test_collect_suit(self):
        collect.collect_scheme('atom')

        scraper = collect.scraper_generate()
        step = collect.steps

        suit = StepSuit(step, scraper)

    def test_deep(self):
        import copy

        class Demo(object):
            def __init__(self, attr=2):
                self.attr = attr
                pass

            def __copy__(self):
                print('copy')
                return '2'

        d = Demo(3)
        d.a = 1
        assert copy.copy(d) == '2'

        # assert False


if __name__ == '__main__':
    unittest.main()
