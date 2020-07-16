import unittest
import time

from queue import Queue

import base.command.commands
from base.libs import threads, ItemPool, Proxy, Model


def proxy_generate(number):
    """
    Args:
        number:
    """
    print('adding proxy,')
    time.sleep(0.5)
    print('done.')
    for i in range(number):
        yield Proxy()


class MyTestCase(unittest.TestCase):
    def test_demo(self):
        pool = ItemPool(proxy_generate)
        pool.start()
        # pool.join(1)

        pool.stop()

    @unittest.skip
    def test_proxy_get(self):
        # TODO: proxy
        from base.libs import RequestScraper

        r = RequestScraper()
        r.scraper_activate()

        url = 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=2'

        from urllib import parse
        def _get_proxy_generation(url):
            res = parse.urlparse(url)

            query = parse.parse_qs(res.query)

            r = RequestScraper()
            r.scraper_activate()

            def proxy_generation(number):
                query['qty'] = number
                query_str = parse.urlencode(query, doseq=True)
                current_res = res._replace(query=query_str)

                current_url = current_res.geturl()

                content = r.get(current_url)

                proxy_list = content.split('\r\n')

                for proxy_info in proxy_list:
                    ip, port = proxy_info.split(':')
                    proxy = Proxy(ip=ip, port=port)

                    assert ip
                    assert port

                    yield proxy

            return proxy_generation

        pool = ItemPool(_get_proxy_generation(url), limit=3)
        pool.start()
        pool.join(60)

    def test_pool_generation(self):
        pool = ItemPool(proxy_generate)

        assert pool.size() is 0
        pool.start()
        time.sleep(0.6)
        assert pool.size() is 10

        [pool.get() for x in range(6)]

        assert pool.size() is 4
        time.sleep(0.7)
        assert pool.size() is 14

    # ----------------------------------------------------------------------
    # test_thread_property

    def test_thread_daemon(self):
        pool = ItemPool(proxy_generate)

        assert pool.isDaemon() is True

    def test_thread_event(self):
        pool = ItemPool(proxy_generate)

        assert pool.event.is_set() is False

        pool.start()
        assert pool.event.is_set() is True

        pool.stop()
        assert pool.event.is_set() is False

    # ----------------------------------------------------------------------
    # test pool property

    def test_pool_generate(self):
        pool = ItemPool(proxy_generate)

        assert callable(base.command.commands.generate)
        assert base.command.commands.generate is proxy_generate

        # generate model

        assert pool.size() is 0
        models = pool.generation()
        assert pool.size() is 10

    def test_pool_limit(self):
        pool = ItemPool(proxy_generate)

        assert pool.limit is 5

    def test_pool_queue(self):
        queue = Queue()
        pool = ItemPool(proxy_generate, queue=queue)

        assert id(queue) == id(pool.queue)


if __name__ == '__main__':
    # unittest.main()
    pass
