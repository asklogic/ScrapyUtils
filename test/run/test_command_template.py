from unittest import TestCase, skip

from base.components.model import Model
from base.components.scheme import Scheme
from base.libs.scraper import Scraper

from base import core


class TestCommand(TestCase):

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_init(self):
        command = TestMockCommand()

        self.assertTrue(issubclass(command.__class__, Command))


        command.build()
        command.finish()
        command.stop()
        pass
