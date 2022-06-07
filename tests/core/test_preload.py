import unittest
import os
import sys
from os.path import dirname, abspath

from ScrapyUtils.core import collect_action, collect_processors
from ScrapyUtils import configure


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        mock_schema_home = os.path.join(dirname(dirname(abspath(__file__))), 'mock_schema')
        sys.path.insert(0, mock_schema_home)
        # the mock modules
        cls.single_action = __import__('single_action')
        cls.other_components = __import__('other_components')

    def tearDown(self) -> None:
        configure.action_classes = []
        configure.processor_classes = []

    def test_preload_action(self):
        """从一个模块中加载指定的组件（action），并置入全局的configure模块中"""
        collect_action(self.single_action)

        assert len(configure.action_classes) == 1
        assert configure.action_classes[0].name == 'TestAction'

    def test_preload_action_not_exist(self):
        """如果没有符合条件的组件，会生成空列表"""
        collect_action(self.other_components)

        assert configure.action_classes == []
        assert len(configure.action_classes) == 0

    def test_preload_processor(self):
        """从一个模块中加载指定的组件（processor），并置入全局的configure模块中"""
        collect_processors(self.other_components)
        assert len(configure.processor_classes) == 1
        assert configure.processor_classes[0].name == 'TestProcessor'

    def test_preload_processor_not_exist(self):
        """如果没有符合条件的组件，会生成空列表"""
        collect_processors(self.single_action)
        assert len(configure.processor_classes) == 0


if __name__ == '__main__':
    unittest.main()
