import unittest
import types

from typing import Any

from base.libs import Model, Field, Task, Proxy


class MockModel(Model):
    age = Field()
    name = Field()


class TestModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()

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
        m = MockModel(name='this', age=12)

        assert m.pure_data == {'age': 12, 'name': 'this'}

    def test_field_default_value(self):
        class DefaultTestModel(Model):
            name = Field('no_name')
            segment = Field(default='seg')

        m = DefaultTestModel()

        assert m.pure_data == {'name': 'no_name', 'segment': 'seg'}

    def test_set_value(self):
        """set value like a data model get value from property"""

        class TestDataModel(Model):
            age = Field()
            name = Field()

        m1 = TestDataModel()
        m2 = TestDataModel()

        m1.age = 12
        m1.name = 'Aiur'
        m2.age = 18

        self.assertEqual(m1.age, 12)
        self.assertEqual(m2.age, 18)

    def test_field(self):
        """Default field without default and convert argument."""
        m = MockModel()
        assert m.pure_data == {'name': '', 'age': ''}

    def test_field_demo(self):
        """Default field without default and convert argument."""
        m = MockModel()
        m.age = 18
        m.name = 'Test_Name'
        assert m.pure_data == {'name': 'Test_Name', 'age': 18}

    def test_field_convert_default(self):
        """Default convert. Do not convert any object."""
        m = MockModel()
        m.age = 20
        assert m.pure_data == {'name': '', 'age': 20}
        m.age = '20'
        assert m.pure_data == {'name': '', 'age': '20'}

    def test_field_convert(self):
        """Convert function in Field"""

        class ConvertModel(Model):
            count = Field(convert=int)

        m = ConvertModel()
        m.count = '12'

        assert m.pure_data == {'count': 12}

    def test_field_default(self):
        """Default value in field."""

        class DefaultModel(Model):
            name = Field('John')

        assert DefaultModel().pure_data == {'name': 'John'}

    def test_common_model_Task(self):
        """Common Model: Task"""
        t = Task()
        t.url = 'https://www.google.com/'
        t.param = 'python object'

        assert t.pure_data == {'url': 'https://www.google.com/', 'count': 0, 'param': 'python object'}

    def test_common_model_Proxy(self):
        """Common Model: Proxy"""
        p = Proxy()



if __name__ == '__main__':
    unittest.main()
