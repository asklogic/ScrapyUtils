import unittest
from urllib import parse
from queue import Queue

from base.libs import Producer, MultiProducer
from base.core import collect
from base.libs import RequestScraper, Proxy

from tests.telescreen import tests_path


# function
# collect._get_proxy_generation
url = 'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=100&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=2'


def rebuild_url(url: str, query_dict: dict):
    # TODO: assert
    """
    Args:
        url (str):
        query_dict (dict):
    """
    assert type(url) is str, 'type'
    assert type(query_dict) is dict, 'type'

    res = parse.urlparse(url)

    ori_query_dict = parse.parse_qs(res.query)

    ori_query_dict.update(query_dict)

    query_str = parse.urlencode(ori_query_dict, doseq=True)

    # res._replace(query=ori_query_dict)

    return res._replace(query=query_str).geturl()


def proxy_generation(url):
    """url from profile.

    Args:
        url:
    """

    r = RequestScraper()
    r.scraper_activate()

    def proxy_generation():
        content = r.get(url)

        proxy_list = content.split('\r\n')

        for proxy_info in proxy_list:
            ip, port = proxy_info.split(':')
            proxy = Proxy(ip=ip, port=port)

            assert ip
            assert port

            yield proxy

    return proxy_generation


class TestProxyProducer(unittest.TestCase):
    def test_init(self):
        pass

    def test_function_rebuild_url(self):
        test_url = 'https://www.baidu.com/s?ie=UTF-8&wd=ip'

        d = {'name': 'nameless'}

        new_url = rebuild_url(test_url, d)
        assert '&name=nameless' in new_url

    def test_function_default_req(self):
        res = proxy_generation(url)

        assert callable(res)
        # assert type(list(res(3))) is list

    def test_multi_proxy_producer(self):
        limit = 6

        gen = proxy_generation(rebuild_url(url, {'qty': '6'}))

        class ProxyProducer(MultiProducer):

            def producing(self, increment):
                return gen()

        producer = ProxyProducer(queue=Queue(5), increment=limit)

    def test_function_in_collect(self):
        collect.collect_scheme('proxy_test')
        from base.core import get_proxy

        collect.proxy.start()

        # [collect.proxy.queue.get() for x in range(8)]
        assert collect.proxy is get_proxy()
        assert collect.proxy == get_proxy()






if __name__ == '__main__':
    unittest.main()
