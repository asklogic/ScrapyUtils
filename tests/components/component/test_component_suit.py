# -*- coding: utf-8 -*-
"""Testcase for ComponentSuit.
"""

import unittest

from ScrapyUtils.components import Component, ComponentSuit

import unittest

from ScrapyUtils.components.component import Component, method_checker


class Mock(Component):
    pass


class SubMock(Mock):
    pass


class NotSub(Component):
    pass

class Failed(Component):

    def __init__(self) -> None:
        raise Exception()
        super().__init__()


class ComponentSuitTestCase(unittest.TestCase):

    def test_sample(self):
        pass

    def test_init_component(self):
        suit = ComponentSuit([Mock, SubMock()])

        assert len(suit.components) == 2

    def test_init_component_failed(self):
        with self.assertRaises(Exception) as e:
            suit = ComponentSuit([Failed])

    @unittest.skip
    def test_checker(self):
        from typing import List, Dict
        number = 10

        components = [Component(), Mock()]

        mapper = {
            'com': Component(),
            'mock': Mock(),
        }

        @method_checker
        def mock_function(number: int, components: List[Component],mapper: Dict[str, Component],
                          nested: List[Dict[str, Component]]):
            pass


        mock_function(number, components, mapper, nested=[mapper, mapper])



if __name__ == '__main__':
    unittest.main()
