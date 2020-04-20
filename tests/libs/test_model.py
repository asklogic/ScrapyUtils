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

    # def test_field_default(self):
    #     """
    #     default and set/get
    #     """
    #     f = Field()
    #
    #     class TestDefaultModel(Model):
    #         atk = Field(default=22)
    #         defence = Field()
    #
    #     class TestOtherModel(Model):
    #         heal = Field(default=100)
    #
    #     m1 = TestDefaultModel()
    #     m2 = TestDefaultModel()
    #     m3 = TestOtherModel()
    #     m4 = TestOtherModel()
    #
    #     self.assertEqual(m1.atk, 22)
    #     self.assertEqual(m2.atk, 22)
    #     self.assertEqual(m3.heal, 100)
    #     self.assertEqual(m4.heal, 100)
    #
    #     self.assertNotEqual(id(m1.pure_data), id(m2.pure_data))
    #
    #     m1.atk = 50
    #     self.assertEqual(m1.atk, 50)
    #
    #     self.assertEqual(m1.defence, None)
    #
    # def test_field_type(self):
    #     """
    #     Field constructor
    #
    #     default - object : default value
    #     convert - function : a function that could convert value when set model's property
    #
    #     """
    #
    #     class TestTypeModel(Model):
    #         attr_int = Field(default='12', convert=int)
    #         age = Field()
    #
    #     m1 = TestTypeModel()
    #     # self.assertEqual(m1.attr_int, 12)
    #
    #     m1.attr_int = '30'
    #
    #     # convert to the first value's type
    #     m1.age = 20
    #     m1.age = '50'
    #     self.assertEqual(m1.attr_int, 30)
    #     self.assertEqual(m1.age, '50')
    #
    # # def test_field_xpath(self):
    # #     self.fail('TODO')
    #
    # # def test_init_func(self):
    # #     self.fail('TODO')
    #
    # def test_task_model(self):
    #     from base.libs import Task
    #
    #     def mock_test_task():
    #         for i in range(2, 20):
    #             t = Task()
    #             t.url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
    #             yield t
    #
    #     # [print(t.url) for t in mock_test_task()]
    #     [self.assertIn('https://www.kuaidaili.com/free/inha', t.url) for t in mock_test_task()]
    #
    # def test_proxy_model(self):
    #     from base.libs import Proxy
    #
    #     def mock_test_proxy():
    #         for i in range(2, 20):
    #             p = Proxy()
    #             p.ip = '127.0.0.1'
    #             p.port = '8090'
    #             yield p
    #
    #     [self.assertEqual('8090', t.port) for t in mock_test_proxy()]
    #     [self.assertEqual('127.0.0.1', t.ip) for t in mock_test_proxy()]
    #
    # def test_constructor(self):
    #     # Task model
    #     from base.libs import Task
    #
    #     t = Task(url='http://ip.cn')
    #
    #     assert t.url == 'http://ip.cn'
    #
    #     # custom model
    #
    #     class CustomModel(Model):
    #         name = Field()
    #
    #     cm = CustomModel(name='custom')
    #
    #     assert cm.name == 'custom'
    #
    #     # FIXME: property and data model
    #     m = CustomModel(notexist='nope')
    #
    # @unittest.skip
    # def test_nametuple(self):
    #     from collections import namedtuple
    #     # from typing import NamedTuple
    #     from recordtype import recordtype
    #     # from dataclasses import dataclass
    #
    #     class TestModelMeta(type):
    #
    #         def __new__(mcs, name, bases, attrs) -> Any:
    #
    #             fields = {}
    #
    #             for key, value in list(attrs.items()):
    #                 if isinstance(value, Field):
    #                     fields[key] = value.default if value.default else ''
    #
    #             attrs['_base_tuple'] = recordtype(name, fields)
    #
    #             return super().__new__(mcs, name, bases, attrs)
    #
    #     class BaseModel(object, metaclass=TestModelMeta):
    #
    #         def __new__(cls) -> Any:
    #             return cls._base_tuple()
    #
    #         # @property
    #         # @classmethod
    #         # def base(cls):
    #         #     return cls._base_tuple
    #
    #     class TestModel(BaseModel):
    #         name = Field('Lou')
    #         age = Field()
    #
    #     assert TestModel().name == 'Lou'
    #     assert TestModel().age == ''
    #
    #     m = TestModel()
    #     m.age = 1
    #     assert m.age == 1
    #
    #     model = namedtuple('model', ['age', 'number'], defaults=['10', '20'])
    #
    # def test_dataclass(self):
    #     from dataclasses import dataclass
    #
    #     @dataclass
    #     class BaseDataModel(object):
    #         name: str = 'name'
    #         age: int = 2
    #
    #     m = BaseDataModel()
    #     assert m.name == 'name'
    #     assert m.age == 2
    #
    #     @dataclass()
    #     class DataModel(object):
    #
    #         @property
    #         def name(self):
    #             return self.__class__.__name__
    #
    #         @classmethod
    #         def get_name(cls):
    #             return cls.__class__.__name__
    #
    #         def pure_data(self):
    #             return self.__dict__
    #
    #     class TestModel(DataModel):
    #         number: str = '1'
    #
    #     m1 = TestModel()
    #     m2 = TestModel()
    #     m1.number = 'name1'
    #     m2.number = 'name2'
    #     assert m1.number == 'name1'
    #     assert m2.number == 'name2'
    #
    #     assert m1.name == 'TestModel'
