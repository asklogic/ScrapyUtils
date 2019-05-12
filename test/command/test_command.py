from unittest import TestCase, skip

from base.command.Command import Command
from logging import INFO
import logging

from base import core
import time
import threading
from base.command import get_command, trigger, sys_exit


class TestMockEmptyCommand(Command):

    def syntax(self):
        return '[MockEmpty]'

    def run(self, **kw):
        pass


class MockInitCommand(Command):

    def syntax(self):
        return '[MockCMD]'

    def options(self, **kw):
        pass

    def run(self, **kw):
        count = 0
        while count > 0:
            count = count - 1
            time.sleep(1)
            self.log('loop')

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

    def tearDown(self) -> None:
        pass



    @classmethod
    def tearDownClass(cls) -> None:
        print('delete target TestGenerateTarget')
        cls.remove('TestGenerateTarget')

    @classmethod
    def remove(cls, target):
        import os
        if os.path.exists(os.path.join(os.getcwd(), target)):

            for file in list(os.walk(target))[0][2]:
                file_path = os.path.join(os.getcwd(), target, file)
                os.remove(file_path)

            for folder in list(os.walk(target))[0][1]:
                folder_path = os.path.join(os.getcwd(), target, folder)
                os.rmdir(folder_path)

            os.rmdir(os.path.join(os.getcwd(), target))

    def test_init(self):
        cmd = TestMockEmptyCommand()

        # property
        # setting:
        self.assertEqual(cmd.setting, None)

        # exit code
        self.assertEqual(cmd.exitcode, 0)

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
        cmd.build_setting()
        self.assertTrue(cmd.setting is None)

        # require_target = true
        thread = TestMockThreadCommand()

        # build. init setting
        # no kw, arise assert error
        with self.assertRaises(AssertionError) as ae:
            thread.build_setting()
        self.assertIn('no target', str(ae.exception))

        # target=TestMock in kw
        thread.build_setting(target='TestMock')
        # init setting property
        from base.libs.setting import Setting
        self.assertIsInstance(thread.setting, Setting)

        # TODO no target folder / components
        todo


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
        import signal
        signal.signal(signal.SIGINT, thread.signal_callback)

        # build command
        thread.build_setting(kw.get('target'))
        try:
            thread.options(**kw)
        except AssertionError as ae:
            import logging
            thread.log(level=logging.ERROR, msg='' + str(ae))

        # run
        try:
            thread.run()
        # exception from signal callback
        except Exception as e:
            thread.failed()
            pass

        finally:
            # cmd exit

            thread.exit()

        # import sys
        # sys.exit(1)

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
