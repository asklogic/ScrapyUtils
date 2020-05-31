import unittest
import types

from typing import Any

from base.libs import Model, Field
from collections import namedtuple


class MockModel(Model):
    age = Field()
    name = Field()


class TestModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()

    def test_exception_extended(self):
        # must be extends
        class MockTestType(object):
            def __getattr__(self, item):
                print('attr')

            def __setattr__(self, name: str, value: Any) -> None:
                print('setattr')

                super().__setattr__(name, value)

            def __getattribute__(self, name: str) -> Any:
                print('attribute')
                return super().__getattribute__(name)

        class MockTest(MockTestType):
            age = Field()

            @property
            def pure_data(self):
                return 'pure_data'

        m = MockTest()

        # m.age = 10
        # m.name = 20
        # m.age
        # m.name

    def test_attribute_pure_data(self):
        m1 = MockModel()
        m2 = MockModel()

        # same value
        assert m1.pure_data == m2.pure_data
        # different reference
        assert m1.pure_data is not m2.pure_data
        assert id(m1.pure_data) != id(m2.pure_data)

    def test_attribute_field(self):
        m1 = MockModel()
        m2 = MockModel()

        # same value and same reference.
        assert m1._fields == m2._fields
        assert m1._fields is m2._fields
        assert id(m1._fields) == id(m2._fields)

    def test_attribute_convert(self):
        m1 = MockModel()
        m2 = MockModel()

        # same value and same reference.
        assert m1._converts == m2._converts
        assert m1._converts is m2._converts
        assert id(m1._converts) == id(m2._converts)

    def test_method_get_name(self):
        assert MockModel.get_name() == 'MockModel'

    def test_property_pure_data(self):
        m = MockModel()
        m.age = 10
        m.name = 'test_name'
        assert m.pure_data == {'age': 10, 'name': 'test_name'}

    def test_function_init(self):
        m = MockModel(name='this',age=12)

        assert m.pure_data == {'age': 12, 'name': 'this'}

    def test_field_default_value(self):
        class DefaultTestModel(Model):
            name = Field('no_name')
            segment = Field(default='seg')

        m = DefaultTestModel()

        assert m.pure_data == {'name': 'no_name', 'segment': 'seg'}

    def test_set_value(self):
        """
        set value like a data model
        get value from property
        """

        class TestDataModel(Model):
            age = Field()
            name = Field()

        m1 = TestDataModel()
        m2 = TestDataModel()

        m1.age = 12
        m1.name = 'Auir'
        m2.age = 18

        # self.assertNotEqual(id(m1.pure_data), id(m2.pure_data))

        self.assertEqual(m1.age, 12)
        self.assertEqual(m2.age, 18)

        # self.assertEqual(m1.pure_data, {'age': 12, 'name': 'Auir'})

        # assert m1.get_name() == 'TestDataModel'

