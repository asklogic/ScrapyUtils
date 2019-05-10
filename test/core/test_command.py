from unittest import TestCase, skip

from base.command.Command import Command
from logging import INFO
import logging

from base import core
import time
from base.command import get_command, trigger, sys_exit


class TestMockEmptyCommand(Command):

    def syntax(self):
        return '[MockEmpty]'

    def run(self, **kw):
        pass


class MockInitCommand(Command):

    def syntax(self):
        return '[MockCMD]'

    def run(self, **kw):
        self.log('some message')


class TestCheckCommand(Command):
    require_target = True

    def syntax(self):
        return '[Check]'

    def run(self, **kw):
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


class TestMockThreadCommand(Command):
    require_target = True

    def syntax(self):
        return '[MockTestThread]'

    def run(self, **kw):
        # log out
        pass

        setting = self.setting
        # build
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)
        schemes = core.build_schemes(setting.CurrentSchemeList)

        sys_hub, dump_hub = core.build_hub(setting=setting)

        sys_hub.activate()
        dump_hub.activate()

        return
        thread_List = []
        for i in range(setting.Thread):
            t = core.ScrapyThread(sys_hub, dump_hub, schemes, scrapers[i], setting)
            thread_List.append(t)
            t.setDaemon(True)
            t.start()

        [t.join() for t in thread_List]
        sys_hub.stop(True)
        dump_hub.stop(True)


class TestCommand(TestCase):

    def setUp(self) -> None:
        cmd = MockInitCommand()

        self.demo_execute = cmd

    def test_init(self):
        cmd = TestMockEmptyCommand()

        # property
        # setting:
        self.assertEqual(cmd.setting, None)

        # exit code
        self.assertEqual(cmd.exitcode, -1)

        # default require_target
        self.assertEqual(cmd.require_target, False)

    # log in command
    def test_log(self):
        # TODO
        cmd = MockInitCommand()

        cmd.log('mock cmd - log test')
        cmd.log('log test DEBUG', level=logging.DEBUG)
        cmd.log('log test INFO', level=logging.INFO)
        cmd.log('log test WARN', level=logging.WARN)

    # step build
    # according to require_target property. to init Setting property
    def test_build(self):
        # require_target = false
        cmd = MockInitCommand()
        cmd.build()
        self.assertTrue(cmd.setting is None)

        # require_target = true
        thread = TestMockThreadCommand()

        # build. init setting
        # no kw, arise assert error
        with self.assertRaises(AssertionError) as ae:
            thread.build()
        self.assertIn('no target', str(ae.exception))

        # target=TestMock in kw
        thread.build(target='TestMock')
        # init setting property
        from base.libs.setting import Setting
        self.assertIsInstance(thread.setting, Setting)

    def test_trigger(self):
        # TODO
        # cmd_name = 'MockTest'

        # cmd = core.get_command(cmd_name)

        # mock command
        thread = MockInitCommand()

        kw = {
            'target': 'TestMockThread',
        }

        # sys register signal function

        # cmd build
        thread.build(**kw)

        try:
            thread.run(**kw)
        # exception from signal callback
        except Exception as e:
            pass

        finally:
            # cmd exit
            thread.exit()

        # sys exit

    @skip
    def test_command_check(self):
        trigger('check', target='TestMockThread')

    @skip
    def test_command_thread(self):
        trigger('thread', target='TestMockThread')

    def test_command_generate(self):
        trigger('generate')

    def test_core_get_command(self):
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
