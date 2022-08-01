import unittest
import types

from typing import Any
from types import MethodType

from ScrapyUtils.libs import Model, field, Task, Proxy


class MockModel(Model):
    age: int = field()
    name: str = field()


class TestModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()

    def test_sample_set_value(self):
        """Set value like a data model get value from property"""

        class TestDataModel(Model):
            age = field()
            name = field()

        m1 = TestDataModel()
        m2 = TestDataModel()

        m1.age = 12
        m1.name = 'Aiur'
        m2.age = 18

        self.assertEqual(m1.age, 12)
        self.assertEqual(m2.age, 18)

    def test_initial(self):
        """Add mapper to initial field.
        """
        mapper = {
            'age': 17,
            'name': 'Ada',
        }

        m = MockModel(**mapper)

        assert m.age is 17

    def test_property_same_pure_data(self):
        """The same value have different pure data."""
        m1 = MockModel()
        m2 = MockModel()

        # same value
        assert m1.pure_data == m2.pure_data
        # different reference
        assert m1.pure_data is not m2.pure_data
        assert id(m1.pure_data) != id(m2.pure_data)

    def test_property_pure_data(self):
        """The common property: pure-data to get data as key-value"""
        m = MockModel()
        m.age = 16
        m.name = 'mm'

        assert m.pure_data == {'age': 16, 'name': 'mm'}

    def test_method_get_name(self):
        """The method get_name: get the class name"""
        assert MockModel.get_name() == 'MockModel'

    def test_field_default_value(self):
        """The default field value could be set in field of dataclass"""

        class DefaultTestModel(Model):
            name: str = field(default='no_name')
            segment: Any = field(default='seg')

        m = DefaultTestModel()

        assert m.pure_data == {'name': 'no_name', 'segment': 'seg'}

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

    def test_sample(self):
        """Sample to set different type of data"""
        m = MockModel()
        m.age = 20
        print(m.pure_data)
        assert m.pure_data == {'name': '', 'age': 20}
        m.age = '20'
        assert m.pure_data == {'name': '', 'age': '20'}

    def test_field_default(self):
        """Default value in field."""

        class DefaultModel(Model):
            name = field(default='John')

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
