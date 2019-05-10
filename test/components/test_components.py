import unittest
from typing import Any

from base.components import Prepare
from base.components import Action, Parse, Scheme
from base.components import Processor
from base.components import Model
from base.components.model import Field
from base.components.base import Component

from base.libs.setting import Setting


class MockProcessor(Processor):

    def process_item(self, model: Model) -> Any:
        return model


class MockPrepare(Prepare):
    pass


class MockModel(Prepare):
    f = Field()
    pass


class MockAction(Prepare):
    pass


def active(component_class: type(Component)):
    component_class._active = True
    return component_class


@active
class MockTestDecoratorAction(Action):
    pass


class TestComponents(unittest.TestCase):

    def setUp(self) -> None:
        self.setting = Setting()
        super().setUp()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_init(self):
        '''
        components init
        这里为Processor
        :return:
        '''
        mock_processor = MockProcessor()

        self.assertTrue(hasattr(mock_processor, '_name'))
        self.assertEqual(mock_processor._name, 'MockProcessor')

        self.assertTrue(issubclass(mock_processor.__class__, Component))

        mock_processor.check()
        pass

    def test_prepare(self):
        '''
        prepare init
        :return:
        '''
        mock_prepare = MockPrepare()

        self.assertTrue(hasattr(mock_prepare, '_name'))
        self.assertEqual(mock_prepare._name, 'MockPrepare')

        self.assertTrue(type(mock_prepare), MockPrepare)
        self.assertTrue(issubclass(mock_prepare.__class__, Component))
        self.assertTrue(issubclass(mock_prepare.__class__, Prepare))

    # components _active
    # 默认为false 通过@active装饰器来控制components是否启用
    def test_active(self):
        # default
        self.assertEqual(MockAction._active, False)
        # add active decorator
        self.assertEqual(MockTestDecoratorAction._active, True)
