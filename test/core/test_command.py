from unittest import TestCase, skip

from base.command import Command


class MockInitCommand(Command):

    def syntax(self):
        return 'MockInit'

    def run(self):
        self.log('some message')

    def build(self, **kw):
        self.log('get key ' + str(kw.get('key1')))


class TestCheckCommand(Command):
    assert_args = ['target']


    def syntax(self):
        return '[Check]'

    def build(self, **kw):
        self.log(msg='my target: ' + self.target, step='')
        import base.core as core
        setting = core.build_setting(self.target)
        # schemes = core.build_thread_schemes(setting.CurrentSchemeList, setting.Thread)

        schemes = [x.get_name() for x in setting.SchemeList]
        self.log(msg='Scheme:' + ' '.join(schemes))

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

    def test_check_command(self):
        check = TestCheckCommand()

        with self.assertRaises(AssertionError) as e:
            check.check_args()
        self.assertIn("doesn't have arguments", str(e.exception))

        check.check_args(target='TestMock')

        check.build()

        check.run()
        check.exit()
        pass

    @skip
    def test_execute(self):
        cmd = self.demo_execute

        cmd.build(key1=114514)

        cmd.check_args()
        cmd.run()
        cmd.exit()

        # TODO core.cmd_exit(cmd.exitcode)
