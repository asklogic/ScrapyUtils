from unittest import TestCase

from base.command.Command import Command
from logging import INFO
import logging

from base import core
import time


class MockInitCommand(Command):

    def syntax(self):
        return '[MockCMD]'

    def run(self):
        self.log('some message')


class TestCheckCommand(Command):
    require_target = True

    def syntax(self):
        return '[Check]'

    def run(self):
        setting = self.setting

        schemes = [str(x) for x in setting.SchemeList]

        current_schemes = [str(x) for x in setting.CurrentSchemeList]

        self.log(msg='setting schemes: \n ' + '\t\n'.join(schemes), level=INFO)

        self.log(msg='current schemes: \n ' + '\t\n'.join(current_schemes), level=INFO)

        current_models = [str(x) for x in setting.CurrentModels]

        self.log(msg='current models: \n ' + '\t\n'.join(current_models), level=INFO)

        processors = [str(x) for x in setting.ProcessorList]

        current_processors = [str(x) for x in setting.CurrentProcessorsList]

        self.log(msg='setting processor: \n ' + '\t\n'.join(processors), level=INFO)

        self.log(msg='current processor: \n ' + '\t\n'.join(current_processors), level=INFO)

        start = time.time()
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

        # comment this
        time.sleep(1)
        end = time.time()

        self.log('spend %.2f second(s) in' % float(end - start))


class MockTestThreadCommand(Command):
    require_target = True

    def syntax(self):
        return '[MockTestThread]'


class TestCommand(TestCase):

    def setUp(self) -> None:
        cmd = MockInitCommand()

        self.demo_execute = cmd

    def test_init(self):
        cmd = MockInitCommand()

        # property
        # setting:
        self.assertEqual(cmd.setting, None)

        # exit code
        self.assertEqual(cmd.exitcode, -1)

        # default require_target
        self.assertEqual(cmd.require_target, False)

    def test_log(self):
        # TODO
        cmd = MockInitCommand()

        cmd.log('mock cmd - log test')
        cmd.log('log test DEBUG', level=logging.DEBUG)
        cmd.log('log test INFO', level=logging.INFO)
        cmd.log('log test WARN', level=logging.WARN)

    def test_build(self):
        # require_target = false
        cmd = MockInitCommand()
        cmd.build()
        self.assertTrue(cmd.setting is None)

        # require_target = true
        thread = MockTestThreadCommand()
        # build
        # no kw, arise assert error
        with self.assertRaises(AssertionError) as ae:
            thread.build()
        self.assertIn('no target', str(ae.exception))

        thread.build(target='TestMock')
        from base.libs.setting import Setting
        self.assertIsInstance(thread.setting, Setting)

    def test_trigger(self):
        # TODO
        # cmd_name = 'MockTest'

        # cmd = core.get_command(cmd_name)

        # mock thread
        thread = MockTestThreadCommand()

        kw = {
            'target': 'TestMock',

        }
        thread.build(**kw)

    def test_command_check(self):
        # todo to trigger
        check = TestCheckCommand()
        kw = {
            'target': 'TestMockCustom'
        }
        check.build(**kw)

        # check.run()

    def test_core_get_command(self):
        from base.command import get_command

        # command_name = 'check'
        #
        # try:
        #     module = __import__('base.command.' + command_name, fromlist=['base', 'command'])
        #
        #     command_class = getattr(module, command_name.capitalize())
        #
        #     command = command_class()
        # except ModuleNotFoundError as error:
        #     raise ModuleNotFoundError('can not found Command %s' % command_name)

        command = get_command('check')

        self.assertTrue(issubclass(command.__class__, Command))

        with self.assertRaises(ModuleNotFoundError) as error:
            command = get_command('not_exist')
        self.assertIn('can not found Command not_exist', str(error.exception))
