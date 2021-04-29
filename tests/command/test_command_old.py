import unittest
import signal
import os

from tests.telescreen import tests_path
from base.core.collect import collect_scheme

schemes_path = os.path.join(tests_path, 'mock_schemes')

from base.command.commands import trigger, thread
from base.command.entity import Command

from base.command.process import sys_exit
from base.command.entity.thread_ import Thread

from base.log import Wrapper as log
from click.testing import CliRunner


# mock
def mock_trigger(command, **kwargs):
    # get command class
    """
    Args:
        command:
        **kwargs:
    """
    command: Command = command

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGINT, command.signal_callback)
    signal.signal(signal.SIGTERM, command.signal_callback)

    # collect
    if command.do_collect:
        collect_scheme(kwargs.get('scheme'))

    try:
        command.options(**kwargs)

        command.run()

    except Exception as e:
        command.failed()
        log.exception('Command', e)

    finally:
        command.stop()

    sys_exit(command.exitcode)


class TestCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass
        # shutil.rmtree(os.path.join(schemes_path, 'generate'))

    def test_generate(self):
        params = {
            # 'scheme': 'lianjia',
            # 'scheme': 'JewDetail',
            # 'scheme': 'UdemyDetail',
            # 'scheme': 'atom',
            # 'scheme': 'diretta',
            'scheme': 'diretta_detail',
        }

        trigger('thread', **params)

    def test_download(self):
        params = {
            # 'scheme': 'lianjia',
            'scheme': 'diretta',
            # 'scheme': 'diretta_detail',
            # 'scheme': 'uspto_detail',
            # 'scheme': 'JewDetail',
            # 'scheme': 'UdemyDetail',
            # 'scheme': 'atom',
        }

        trigger('download', **params)

    def test_parsing(self):
        params = {
            'scheme': 'diretta_match',
            # 'scheme': 'uspto_detail',
            # 'index': 1,
            # 'download': '1590088871'
            # 'scheme': 'lianjia',
            # 'scheme': 'JewDetail',
            # 'scheme': 'UdemyDetail',
            # 'scheme': 'atom',
        }

        trigger('parsing', **params)

    def test_atom(self):
        params = {
            'scheme': 'atom',
            'path': schemes_path
        }

        command = Thread()
        mock_trigger(command, **params)

        # block here

        from base.core.collect import models_pipeline as pipeline
        assert pipeline.suit.schemes[0].name == 'Duplication'
        assert pipeline.suit.schemes[1].name == 'Count'

        count = pipeline.suit.schemes[1].mock_count
        failed = len(pipeline.failed)

        assert count + failed > 5 * 10

    def test_atom_runner(self):
        runner = CliRunner()
        result = runner.invoke(thread, ['atom', '--path', r'E:\cloudWF\RFW\ScrapyUtils\tests\mock_schemes'])

        print(result.output)

    def test_proxy(self):
        params = {
            'scheme': 'proxy_test',
            'path': schemes_path
        }

        command = Thread()
        mock_trigger(command, **params)

    @unittest.skip
    def test_proxy_test_runner(self):
        runner = CliRunner()
        from base.command import thread
        result = runner.invoke(thread, ['proxy_test', '--path', r'E:\cloudWF\RFW\ScrapyUtils\tests\mock_schemes'])

        print(result.output)

    def test_instable(self):
        runner = CliRunner()
        from base.command import thread
        result = runner.invoke(thread, ['test_instable', '--line', '0'])

        print(result.output)

        from base.core.collect import models_pipeline

        print(models_pipeline.suit.schemes[0].mock_count)
        assert models_pipeline.suit.schemes[0].mock_count > 0

    def test_log(self):
        command = Thread()

        command.log.info('wtf!', 'Pipeline', 'Count')
        command.log.info('wtf!', 'Scrapy')
        command.log.info('wtf!', 'Core')
        command.log.info('wtf!', )


if __name__ == '__main__':
    unittest.main()
