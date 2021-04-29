import unittest

from ScrapyUtils.components import Component


class Mock(Component):
    pass


class Modify(Component):
    pass


class Redis(Component):
    def on_start(self):
        start = 100

    def on_exit(self):
        exit = '200'


class ComponentTestCase(unittest.TestCase):
    def test_sample(self):
        pass

    def test_attribute_active_default(self):
        """Attribute: active default False"""
        assert Mock.active is False
        assert Mock().active is False

    def test_attribute_name_default(self):
        """Attribute: name default <class.__name__>"""
        assert Mock.name == 'Mock'
        assert Mock().name == 'Mock'

    def test_attribute_proprity_default(self):
        """Attribute: proprity default 500"""
        assert Mock.priority == 500
        assert Mock().priority == 500

    def test_attribute_modify(self):
        """Attribute: Assign class will affect instance"""
        assert Modify().priority == 500

        Modify.priority = 400

        assert Modify().priority == 400

    def test_method_on_stast_default(self):
        """Method: abstract on_start."""
        Mock().on_start()

    def test_method_on_exit_default(self):
        """Method: abstract on_exit."""
        Mock().on_exit()


if __name__ == '__main__':
    unittest.main()
