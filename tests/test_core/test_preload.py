import unittest
import os
import sys
from os.path import dirname, abspath

from ScrapyUtils.core import collect_action, collect_processors, initial_configure
from ScrapyUtils import configure


class PreloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        mock_project_home = os.path.join(dirname(dirname(abspath(__file__))), 'mock_project')
        sys.path.insert(0, mock_project_home)
        # the mock modules
        cls.single_action = __import__('single_action')
        cls.other_components = __import__('other_components')
        cls.normal_setting = __import__('normal_setting')

    def setUp(self) -> None:
        configure.action_classes = []
        configure.process_classes = []

    def test_collect_action(self):
        """函数: collect_action"""

        with self.subTest('collect action'):
            collect_action(self.single_action)

            assert len(configure.action_classes) == 1
            assert configure.action_classes[0].name == 'TestAction'

        with self.subTest('no actions'):
            collect_action(self.other_components)

            assert configure.action_classes == []

    def test_collect_processor(self):
        """函数: collect_processor"""

        with self.subTest('collect process'):
            collect_processors(self.other_components)
            assert len(configure.process_classes) == 1
            assert configure.process_classes[0].name == 'TestProcessor'

        with self.subTest('no process'):
            collect_processors(self.single_action)

            assert configure.process_classes == []

    def test_initial_configure(self):
        """函数: initial_configure"""

        with self.subTest('initial configure'):
            initial_configure(self.normal_setting)

    def test_import_error(self):
        """格式问题"""

        with self.assertRaises(Exception) as e:
            __import__('error')


if __name__ == '__main__':
    unittest.main()
