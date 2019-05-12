import unittest
from unittest import TestCase, skip

from base.command import trigger, get_command, Command


class TestCommandGenerate(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        print('delete target TestGenerateTarget')
        cls.remove('TestGenerateTarget')

    @classmethod
    def remove(cls, target):
        import os

        for file in list(os.walk(target))[0][2]:
            file_path = os.path.join(os.getcwd(), target, file)
            os.remove(file_path)

        for folder in list(os.walk(target))[0][1]:
            folder_path = os.path.join(os.getcwd(), target, folder)
            os.rmdir(folder_path)

        os.rmdir(os.path.join(os.getcwd(), target))

    def test_command_generate(self):
        trigger('generate', target='TestGenerateTarget')

    def test_command_generate_option(self):
        # empty
        cmd: Command = get_command('generate')
        kw = {}

        # assert kw: target
        # must have target
        with self.assertRaises(AssertionError) as ae:
            cmd.options(**kw)
        self.assertIn('no target', str(ae.exception))

        # default
        from base.command.generate import Generate
        import os

        kw = {
            'target': 'TestTargetName'
        }

        cmd: Generate = get_command('generate')
        cmd.options(**kw)

        self.assertEqual(cmd.target_name, 'TestTargetName')
        self.assertEqual(cmd.path, os.getcwd())
        self.assertEqual(cmd.data, True)
