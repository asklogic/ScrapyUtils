# -*- coding: utf-8 -*-
"""Testcase for ComponentSuit.
"""

import unittest

from ScrapyUtils.components import Component, ComponentSuit


class ComponentSuitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.suit = ComponentSuit([])

        class Alpha(Component):
            priority = 800
            pass

        class Beta(Component):
            priority = 600

        class Gamma(Component):
            priority = 400

        class ErrorStart(Component):
            def on_start(self):
                assert False

        class ErrorExit(Component):
            def on_exit(self):
                assert False

        self.mock_components = [Alpha(), Beta(), Gamma()]
        self.alpha = Alpha()
        self.beta = Beta()
        self.gamma = Gamma()
        self.error_start = ErrorStart()
        self.error_exit = ErrorExit()

    def test_arguments_components(self):
        """Arguments components: several components"""
        suit = ComponentSuit(components=self.mock_components)

        self.assertEqual(len(suit.components), 3)

    def test_arguments_components_positional(self):
        """Arguments components: several components in positional arguments"""
        suit = ComponentSuit(self.mock_components)

        self.assertEqual(len(suit.components), 3)

    def test_arguments_components_none(self):
        """Arguments components: None"""
        suit = ComponentSuit()

        self.assertEqual(len(suit.components), 0)

    def test_method_append_component(self):
        """Method append component in suit"""
        suit = ComponentSuit()

        suit.add_component(self.mock_components[0])

        self.assertEqual(len(suit.components), 1)
        self.assertEqual(suit.components[0].name, 'Alpha')

    def test_property_components_in_sort(self):
        """Property components will be sort by key."""
        suit = ComponentSuit()

        suit.add_component(Component())
        suit.add_component(self.alpha)
        suit.add_component(self.gamma)

        self.assertEqual(suit.components[0].name, 'Alpha')
        self.assertEqual(suit.components[1].name, 'Component')
        self.assertEqual(suit.components[2].name, 'Gamma')

    def test_method_on_start(self):
        """Method start components"""
        suit = ComponentSuit()

        suit.suit_start()

    def test_method_on_exit(self):
        """exit components"""
        suit = ComponentSuit()

        suit.suit_exit()

    def test_method_on_start_error_components(self):
        """Some components error."""
        suit = ComponentSuit(self.mock_components)
        suit.add_component(self.error_start)
        suit.add_component(self.error_exit)

        # success append
        self.assertEqual(len(suit.components), 5)

        error = suit.suit_start()

        # remove error components
        self.assertEqual(len(suit.components), 4)

        self.assertEqual(error[0].name, 'ErrorStart')

    def test_method_on_exit_error_components(self):
        """Some components error."""
        suit = ComponentSuit(self.mock_components)
        suit.add_component(self.error_start)
        suit.add_component(self.error_exit)

        # success append
        self.assertEqual(len(suit.components), 5)

        error = suit.suit_exit()

        # remove error components
        self.assertEqual(len(suit.components), 4)

        self.assertEqual(error[0].name, 'ErrorExit')


if __name__ == '__main__':
    unittest.main()
