import unittest

from ScrapyUtils.core import *


# change tests path
# TODO: change to /tests/mock_schemes.

class TestSchemePreloadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        assert collect.steps_class == []
        assert collect.processors_class == []

    # def test_default_process(self):
    #     assert collect.steps_class == []
    #     assert collect.processors_class == []

    def test_default_atom_var(self):
        scheme_preload('atom')

        assert collect.steps_class != []
        assert collect.processors_class != []

        # atom default step

        assert len(collect.steps_class) == 2
        assert len(collect.processors_class) == 1

    # TODO: more priority test case.
    def test_feature_step_priority(self):
        """
        Action default priority : 600
        Parse default priority : 400
        """
        scheme_preload('TestPriority')

        assert len(collect.steps_class) == 4
        print(collect.steps_class)

        assert collect.steps_class[0].name == 'FirstAction'
        assert collect.steps_class[1].name == 'TestPriorityAction'
        assert collect.steps_class[2].name == 'TestPriorityParse'
        assert collect.steps_class[3].name == 'ThirdAction'

    # TODO: step active state test case.

    # TODO: custom preload exception
    def test_error_syntax(self):
        with self.assertRaises(Exception) as e:
            scheme_preload('TestSyntaxError')

        assert 'Failed in scheme preload.' in str(e.exception)


if __name__ == '__main__':
    unittest.main()
