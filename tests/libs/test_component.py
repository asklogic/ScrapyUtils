import unittest

from base.components import Component, active

from base.components import Model, Field
from base.components.step import ActionStep, ParseStep
from base.libs import Task


class MyTestCase(unittest.TestCase):

    def test_property(self):
        """
        component common property
        """

        @active
        class TestComponent(Component):
            pass

        assert TestComponent.name == 'TestComponent'

        class TestAction(ActionStep):
            def scraping(self, task: Task):
                pass

            def check(self, content):
                pass

        assert TestAction.active is False
        assert TestComponent.active is True

        assert issubclass(TestAction, Component)
        assert issubclass(TestComponent, Component)

        action = TestAction()
        assert isinstance(action, ActionStep)
        assert isinstance(action, Component)

    def test_collect(self):
        pass

    # conflict

    # class TestModel(Model):
    #     name = Field()
    #     age = Field()
    #
    # model = TestModel()
    # model.name = 'Who'
    #
    # assert model.name == 'Who'
    #
    # assert model.get_name() == 'TestModel'


if __name__ == '__main__':
    unittest.main()
