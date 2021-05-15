# -*- coding: utf-8 -*-
"""Testcase for ComponentSuit.
"""

import unittest

from ScrapyUtils.components import Component, ComponentSuit

import unittest


class Mock(Component):
    pass


class SubMock(Mock):
    pass


class NotSub(Component):
    pass


class Error(Component):

    def __init__(self) -> None:
        super().__init__()
        raise Exception('failed __init__ case')


class ComponentSuitTestCase(unittest.TestCase):

    def test_sample(self):
        pass

    def test_init_component_single(self):
        """__init__ with single component."""
        suit = ComponentSuit([Mock, ])

        assert len(suit.components) == 1

    def test_init_component_multi(self):
        """__init__ with multi components."""
        suit = ComponentSuit([Mock, SubMock])

        assert len(suit.components) == 2

    def test_init_component_incorrect_component_type(self):
        """ComponentSuit will skip incorrect component type."""
        assert len(ComponentSuit([1]).components) == 0

        assert len(ComponentSuit([Mock(), list, lambda: 0]).components) == 1

    def test_init_component_error(self):
        """__init__ failed in component's init method."""
        with self.assertRaises(Exception) as e:
            suit = ComponentSuit([Error])
        assert 'failed __init__ case' in str(e.exception)

    def test_init_component_incorrect_type(self):
        """ComponentSuit need a component list."""

        ComponentSuit([])

        with self.assertRaises(TypeError) as te:
            ComponentSuit(None)

        with self.assertRaises(TypeError) as te:
            ComponentSuit(0)

        with self.assertRaises(TypeError) as te:
            ComponentSuit(True)

    def test_method_append_component(self):
        """TODO"""
        self.assertEqual(True, False)

    def test_method_suit_start(self):
        """TODO"""
        self.assertEqual(True, False)

    def test_method_suit_exit(self):
        """TODO"""
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
