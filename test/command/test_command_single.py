from unittest import TestCase, skip

from base import core
from base import command

from base.command import single


class TestCommandSingle(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.kw = {
            'target': 'TestSingle'
        }
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()

    def test_command_init(self):
        cmd = command.get_command('single')

        pass

    def test_single_build(self):
        cmd = command.get_command('single')

        cmd.build_setting('TestSingle')

        # TODO property

    def test_single(self):
        cmd = command.get_command('single')
        cmd.build_setting('TestSingle')

        # import click
        #
        # @click.command()
        # @click.option('--count', default=1, prompt='first prompt')
        # def first_step(count):
        #     print(count)
        #
        # first_step()
        pass

    @skip
    def test_single_run(self):
        command.trigger('single', **self.kw)
        pass
