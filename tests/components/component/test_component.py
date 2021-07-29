# -*- coding: utf-8 -*-
"""Testcase for Component class.
"""
import unittest

from ScrapyUtils.components import Component


class Mock(Component):
    pass


class Modify(Component):
    pass


class ComponentTestCase(unittest.TestCase):

    def test_attribute_active_default(self):
        """Attribute - active: default to False"""
        self.assertFalse(Mock.active)
        self.assertFalse(Mock().active)

    def test_attribute_name_default(self):
        """Attribute: name default to the class name"""
        self.assertEqual(Mock.name, 'Mock')

    def test_attribute_priority_default(self):
        """Attribute: priority default 500"""
        self.assertEqual(Mock.priority, 500)

    def test_method_on_stast_default(self):
        """Abstract method: on_start."""
        Mock().on_start()

    def test_method_on_exit_default(self):
        """Abstract method: on_exit."""
        Mock().on_exit()

    def test_method_ready_state(self):
        """Abstract method: ready_state."""
        self.assertTrue(Mock().ready_state())

    def test_method_exit_state(self):
        """Abstract method: exit_state."""
        self.assertTrue(Mock().exit_state())


if __name__ == '__main__':
    unittest.main()
