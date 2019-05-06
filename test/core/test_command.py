from unittest import TestCase, skip

from base.command import Command


class MockInitCommand(Command):

    def syntax(self):
        return '[MockInit]'

    def run(self):
        self.log('some message')



class TestCheckCommand(Command):
    assert_args = ['target']

    def syntax(self):
        return '[Check]'




class TestThreadCommand(Command):

    def syntax(self):
        return '[Thread]'

    def check_args(self, **kw):
        # must have target and build setting
        pass


class TestCommand(TestCase):

    def setUp(self) -> None:
        cmd = MockInitCommand()

        self.demo_execute = cmd

    def test_init(self):
        cmd = MockInitCommand()

    def test_trigger(self):
        # TODO
        # cmd_name = 'MockTest'

        # cmd = core.get_command(cmd_name)

        # temp
        cmd = MockInitCommand()
        cmd.build()

        cmd.run()
        self.assertTrue(cmd.setting is None)




