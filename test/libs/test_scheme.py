import unittest
from typing import *

from base import core
from base.libs.task import Task
from base.components.prepare import Prepare

from base.components.scheme import Scheme


class TestScheme(unittest.TestCase):

    def setUp(self) -> None:
        self.normal_setting = core.build_setting('TestMock')

        self.prepare: Prepare = self.normal_setting.CurrentPrepare
        self.schemes: List[Scheme] = self.normal_setting.CurrentSchemeList

        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_init(self):
        pass

    def test_build_scheme(self):
        [self.assertTrue(issubclass(x, Scheme)) for x in self.schemes]
        schemes = core.build_schemes(self.schemes)

        [self.assertIsInstance(x, Scheme) for x in schemes]

        id_list = [id(x) for x in schemes]
        self.assertEqual(len(id_list), len(set(id_list)))

        context_id = id(schemes[0].context)

        [self.assertEqual(id(x.context), context_id) for x in schemes]

    def test_load_context(self):
        task = Task()

        task.param = {
            'uid': '10'
        }

        schemes = core.build_schemes(self.schemes)

        core.load_context(task, schemes)

        context_list = [x.context for x in schemes]

        self.assertEqual(len(set([id(x) for x in context_list])),1)

        for context in context_list:

            self.assertTrue(context.get('uid'), '10')
