import unittest

from base.core import collect
from base.core import *

from tests.telescreen import schemes_path
from importlib import import_module

from base.components import *
from base.libs import *
from queue import Queue


class TestCollect(unittest.TestCase):

    # @unittest.skip
    # def test_init_collect(self):
    #     """
    #     test_mock_scheme
    #     """
    #
    #     # /tests/mock_schemes in sys.path
    #     with self.assertRaises(ModuleNotFoundError) as mnfe:
    #         import_module('not_exist')
    #
    #     # case: test_collect_active (step)
    #     module = import_module('test_collect_active')
    #
    #     assert len(module.steps) is 1
    #     assert module.steps[0].name == 'Actived'
    #
    #     # case: test_collect_priority
    #     priority = import_module('test_collect_priority')
    #
    #     assert len(priority.processors) == 3
    #     assert priority.processors[0].name == 'Duplication'
    #     assert priority.processors[1].name == 'Count'
    #     assert priority.processors[2].name == 'MysqlSave'
    #
    #     # case: test_profile
    #
    #     profile = import_module('test_profile')
    #
    #     assert profile.config['thread'] is 2
    #     assert profile.config['timeout'] == 1.5
    #     assert callable(profile.scraper_callable)
    #     assert callable(profile.tasks_callable)
    #
    #     tasks = profile.tasks_callable()
    #     assert len(list(tasks)) == 10
    #
    #     # final case: atom
    #
    #     atom = import_module('atom')
    #
    #     # step
    #     assert len(atom.steps) is 4
    #     for step in atom.steps:
    #         assert issubclass(step, Step)

    def test_case_collect_scheme_switch(self):
        # assert get_steps() is None

        collect.collect_scheme('atom')
        assert len(get_steps()) == 4

        collect.collect_scheme('Fox')
        assert len(get_steps()) == 2

    def test_collect_global_variable(self):
        """
        replace by get_XXX function.
        """
        pass

    def test_function_get_scheme(self):
        collect.collect_scheme('atom')

        steps = get_steps()
        assert len(steps) == 4

    def test_function_get_pipeline(self):
        collect.collect_scheme('atom')

        assert get_pipeline()
        assert isinstance(get_pipeline(), Pipeline)

    def test_function_get_config(self):
        collect.collect_scheme('atom')

        conf = get_config()
        assert conf
        assert isinstance(conf, dict)

        # config attr
        assert conf.get('thread') == 2

    def test_function_get_task_queue(self):
        collect.collect_scheme('atom')

        queue = get_tasks()
        assert queue
        assert queue.qsize() == 10

    def test_function_get_scraper_gen(self):
        collect.collect_scheme('atom')

        gen = get_scraper_generate()
        assert gen
        assert callable(gen)

        scraper = gen()
        assert isinstance(scraper, Scraper)
        assert scraper.activated is True

    @unittest.skip
    def test_function_get_proxy_info(self):
        collect.collect_scheme('proxy_test')

        config = get_config()

        assert config.get('proxy') is True
        assert config.get('proxy_url')

        url = 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=2'

        gen = collect._get_proxy_generation(url)

        class ProxyProducer(MultiProducer):
            def producing(self, increment):
                for proxy_model in gen(increment):
                    yield proxy_model

        proxy_producer = ProxyProducer(10, queue=Queue(5), delay=1.1)

        proxy_producer.start()

        proxy_producer.stop()

    @unittest.skip
    def test_function_get_proxy_producer(self):
        proxy_url = 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=2'

        res = collect._get_proxy_generation(proxy_url)

        proxies = list(res(5))

        for p in proxies:
            print(p)

        assert proxies

    def test_deep(self):
        import copy

        class Demo(object):
            def __init__(self, attr=2):
                self.attr = attr
                pass

            def __copy__(self):
                print('copy')
                return '2'

        d = Demo(3)
        d.a = 1
        assert copy.copy(d) == '2'

        # assert False


if __name__ == '__main__':
    unittest.main()
