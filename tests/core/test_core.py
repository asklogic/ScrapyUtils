import unittest
from typing import List, Type
import os
import os.path

from tests.telescreen import tests_path
schemes_path = os.path.join(tests_path, 'mock_schemes')

from base.components.step import ActionStep, ParseStep, Step
from base.components import Processor, Component

import os, sys
import importlib
from types import ModuleType

# origin
# def _load_file(scheme_path: str, file_name: str, component: type) -> List[Component]:
#     assert os.path.exists(scheme_path)
#     assert os.path.isdir(schemes_path)
#     file_path = os.path.join(scheme_path, file_name)
#
#     assert os.path.exists(file_path)
#     assert os.path.isfile(file_path)
#
#     scheme = os.path.basename(scheme_path)
#
#     # TODO: imp
#     module = importlib.import_module(scheme + '.' + file_name.split('.')[0])
#
#     components: List[Component] = []
#     for attr in dir(module):
#         attribute = getattr(module, attr)
#         # 短路判断类
#         if isinstance(attribute, type) and issubclass(attribute, component) and attribute is not component:
#             components.append(attribute)
#     return components


def collect(scheme_path: str, file_name: str, component: Type) -> List[Component]:
    module = _load_file(scheme_path, file_name)
    components = _load_components(module, component)

    return components


def _load_file(scheme_path: str, file_name: str) -> ModuleType:
    assert os.path.exists(scheme_path)
    assert os.path.isdir(scheme_path)
    file_path = os.path.join(scheme_path, file_name)

    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

    scheme = os.path.basename(scheme_path)

    # TODO: imp
    module = importlib.import_module(scheme + '.' + file_name.split('.')[0])
    return module


def _load_components(module: ModuleType, component: Type):
    components: List[Component] = []
    for attr in dir(module):
        attribute = getattr(module, attr)
        # 短路判断类
        if isinstance(attribute, type) and issubclass(attribute, component) and attribute is not component:
            components.append(attribute)
    return components


atom_path = os.path.join(schemes_path, 'atom')
sys.path.append(schemes_path)


class TestCore(unittest.TestCase):

    def test_collect_component(self):
        actions = collect(atom_path, 'action.py', ActionStep)
        parses = collect(atom_path, 'parse.py', ParseStep)

        processors = collect(atom_path, 'processor.py', Processor)

        steps: List[Step] = actions + parses

        assert len(steps) == 5
        assert steps[0].name == 'Abort'

        assert len(processors) == 3
        assert processors[0].name == 'Count'

    def test_load_file(self):
        from tests.mock_schemes.atom import action
        from tests.mock_schemes.atom import parse

        module = _load_file(atom_path, 'action.py')

        assert module.__file__ == action.__file__

    def test_load_component(self):

        # from tests.mock_schemes.atom.action import Single
        # from tests.mock_schemes.atom import action

        # ! sys.path
        from atom import action

        actions = _load_components(action, ActionStep)

        #
        assert actions[0].name == 'Abort'
        assert actions[2] == action.Single

        collect_actions = collect(atom_path, 'action.py', ActionStep)
        assert collect_actions[2] == action.Single

    def test_collect(self):
        """
        to test_components' collect_steps,collect_processors
        """
        pass

if __name__ == '__main__':
    unittest.main()
