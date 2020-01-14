import unittest
import os

from base.components import Component, active, Processor

from base.components.step import ActionStep, ParseStep, Step
from base.libs import Task, Model, Field
from base.core import collect

from typing import List
# test
from tests.telescreen import schemes_path


class MyTestCase(unittest.TestCase):

    def test_property(self):
        """
        component common property

        active
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

        assert TestAction().active is False
        assert TestComponent().active is True

        assert issubclass(TestAction, Component)
        assert issubclass(TestComponent, Component)

        action = TestAction()
        assert isinstance(action, ActionStep)
        assert isinstance(action, Component)

    def test_name_property(self):
        class CustomName(ActionStep):
            pass

        # class & instance
        assert CustomName.name == 'CustomName'
        assert CustomName().name == 'CustomName'

        class CustomParse(ParseStep):
            pass

        assert CustomParse.name == 'CustomParse'
        assert CustomParse().name == 'CustomParse'

        class CustomProcessor(Processor):
            pass

        assert CustomProcessor.name == 'CustomProcessor'
        assert CustomProcessor().name == 'CustomProcessor'

    def test_step_property(self):
        """
        to test_step_base.py
        """
        pass

    def test_processor_property(self):
        """
        to test_processor.py
        """
        pass

    def test_priority(self):
        """
        property priority
        """

        # default processor priority: 500
        # default action priority: 600
        # default parse priority: 400
        class TestPriorityAction(ActionStep):
            pass

        assert TestPriorityAction.priority == 600
        assert TestPriorityAction().priority == 600

        # collect and sort

        priority = os.path.join(schemes_path, 'test_collect_priority')
        actions = collect(priority, 'action.py', ActionStep)

        # origin list sequence
        assert actions[0].name == 'Eno'
        assert actions[1].name == 'First'
        assert actions[2].name == 'Second'
        assert actions[3].name == 'Third'

        assert len(actions) == 4

        actions.sort(key=lambda x: x.priority, reverse=True)

        # after sort
        assert actions[0].name == 'First'
        assert actions[1].name == 'Eno'
        assert actions[2].name == 'Second'
        assert actions[3].name == 'Third'

        # processors
        processors = collect(priority, 'processor.py', Processor)
        processors.sort(key=lambda x: x.priority, reverse=True)

        assert processors[0].name == 'Duplication'
        assert processors[1].name == 'Count'
        assert processors[2].name == 'MysqlSave'

    def test_active(self):
        active = os.path.join(schemes_path, 'test_collect_active')
        actions = collect(active, 'action.py', ActionStep)

        assert len(actions) == 2

        actions = [x for x in actions if x._active]

        assert len(actions) == 1
        assert actions[0].name == 'Actived'

        # processor
        processors = collect(active, 'processor.py', Processor)
        assert len(processors) == 2

        processors = [x for x in processors if x._active]
        assert len(processors) == 1
        assert processors[0].name == 'Count'

    def test_collect(self):
        """
        collect step in command
        """
        atom = os.path.join(schemes_path, 'atom')
        actions = collect(atom, 'action.py', ActionStep)

        # collect_steps function:

        def collect_steps(scheme_path) -> List[Step]:
            actions = collect(scheme_path, 'action.py', ActionStep)
            parses = collect(scheme_path, 'parse.py', ParseStep)

            # remove deactive
            steps = [x for x in actions + parses if x.active]

            # sort
            steps.sort(key=lambda x: x.priority, reverse=True)

            return steps

        steps = collect_steps(atom)

        assert steps[0].name is 'Nooope'
        assert steps[1].name is 'Single'
        assert steps[2].name is 'MockPersonParse'
        assert steps[3].name is 'CountParse'

        for step in steps:
            assert issubclass(step, Step)

        def collect_processors(scheme_path) -> List[Processor]:
            origin_processors = collect(scheme_path, 'processor.py', Processor)
            # remove deactive
            processors = [x for x in origin_processors if x.active]

            # sort
            processors.sort(key=lambda x: x.priority, reverse=True)
            return processors

        processors = collect_processors(atom)
        assert processors[0].name == 'Duplication'
        assert processors[1].name == 'Count'

        for processor in processors:
            assert issubclass(processor, Processor)


if __name__ == '__main__':
    unittest.main()
