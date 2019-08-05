import unittest

from base.libs import Model, Field


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()

    def test_init(self):
        # must be inheritance
        with self.assertRaises(Exception) as e:
            m = Model()

        class TestModel(Model):
            pass

        m = TestModel()

        self.assertEqual(m.name(), 'TestModel')

    def test_component_active(self):
        """
        test_component_active : TODO
        :return:
        """
        pass

    def test_set_value(self):
        class TestDataModel(Model):
            age = Field()
            name = Field()

        m1 = TestDataModel()
        m2 = TestDataModel()

        m1.age = 12
        m1.name = 'Auir'
        m2.age = 18

        self.assertNotEqual(id(m1.pure_data), id(m2.pure_data))

        self.assertEqual(m1.age, 12)
        self.assertEqual(m2.age, 18)

        self.assertEqual(m1.pure_data, {'age': 12, 'name': 'Auir'})

    def test_field_default(self):
        """
        default and set/get
        """
        f = Field()

        class TestDefaultModel(Model):
            atk = Field(default=22)
            defence = Field()

        class TestOtherModel(Model):
            heal = Field(default=100)

        m1 = TestDefaultModel()
        m2 = TestDefaultModel()
        m3 = TestOtherModel()
        m4 = TestOtherModel()

        self.assertEqual(m1.atk, 22)
        self.assertEqual(m2.atk, 22)
        self.assertEqual(m3.heal, 100)
        self.assertEqual(m4.heal, 100)

        self.assertNotEqual(id(m1.pure_data), id(m2.pure_data))

        m1.atk = 50
        self.assertEqual(m1.atk, 50)

        self.assertEqual(m1.defence, None)

    def test_field_type(self):
        # """
        # force convert
        # """

        class TestTypeModel(Model):
            attr_int = Field(default='12', convert=int)
            age = Field()

        m1 = TestTypeModel()
        # self.assertEqual(m1.attr_int, 12)

        m1.attr_int = '30'

        # convert to the first value's type
        m1.age = 20
        m1.age = '50'
        self.assertEqual(m1.attr_int, 30)
        self.assertEqual(m1.age, '50')

    # def test_field_xpath(self):
    #     self.fail('TODO')

    # def test_init_func(self):
    #     self.fail('TODO')

    def test_task_model(self):
        from base.libs import Task

        def mock_test_task():
            for i in range(2, 20):
                t = Task()
                t.url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
                yield t

        # [print(t.url) for t in mock_test_task()]
        [self.assertIn('https://www.kuaidaili.com/free/inha', t.url) for t in mock_test_task()]

    def test_proxy_model(self):
        from base.libs import Proxy

        def mock_test_proxy():
            for i in range(2, 20):
                p = Proxy()
                p.ip = '127.0.0.1'
                p.port = '8090'
                yield p

        [self.assertEqual('8090', t.port) for t in mock_test_proxy()]
        [self.assertEqual('127.0.0.1', t.ip) for t in mock_test_proxy()]


