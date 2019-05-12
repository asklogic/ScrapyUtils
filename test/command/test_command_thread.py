from unittest import TestCase, skip
from base.command import Command, get_command


class Thread(Command):
    require_target = True

    def syntax(self):
        return '[Thread]'

    def __init__(self):
        super().__init__()

    def signal_callback(signum, frame, self):
        super().signal_callback(frame, self)

    def options(self, **kw):
        pass

    def run(self, **kw):
        pass

    def failed(self):
        pass

    def exit(self):
        pass


class TestCommandThread(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    @classmethod
    def setUpClass(cls) -> None:
        cls.cmd = Thread()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_init(self):
        cmd: Thread = self.cmd
        kw = {
            'target': 'TestEmptyThread'
        }
        cmd.build_setting(**kw)

    def test_option(self):
        pass
