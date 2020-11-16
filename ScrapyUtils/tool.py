from lxml import etree
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import requests
import time
# import peewee
import redis

headers = {
    'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    "Content-Type": "application/x-www-form-urlencoded",
    'Connection': 'close',
    'Cache-Control': 'max-age=0',
}


def xpathParse(htmlContent: str, xpathContent: str) -> List[str]:
    """
    Args:
        htmlContent (str):
        xpathContent (str):
    """
    assert bool(htmlContent), "empty content"
    assert bool(xpathContent), "empty xpath"

    html = etree.HTML(htmlContent)
    result = html.xpath(xpathContent)

    pure_data = []
    for el in result:
        if isinstance(el, etree._ElementUnicodeResult):
            el = str(el)
            pure_data.append(el)
        elif isinstance(el, etree._Element):
            el = str(el.text)
            pure_data.append(el)
        else:
            pure_data.append(el)

    return pure_data


class XpathParser(object):
    etree: etree.HTML
    single: bool = False

    def __init__(self, html):
        """
        Args:
            html:
        """
        assert html, "empty content."
        assert type(html) == str, "html content must be str."

        self.etree = etree.HTML(html)

    def xpath(self, xpath, child_text=False):
        """
        Args:
            xpath:
        """
        assert xpath, "empty xpath."
        assert type(xpath) == str, "xpath content must be str."

        result = self.etree.xpath(xpath)

        pure_data = []
        for el in result:
            if isinstance(el, etree._ElementUnicodeResult):
                el = str(el)
                pure_data.append(el)
            elif isinstance(el, etree._Element):
                if child_text:
                    el = str(list(filter(None, el.xpath('text()')))[-1])
                    pure_data.append(el)
                else:
                    el = str(el.text)
                    pure_data.append(el)
            else:
                pure_data.append(el)

        return pure_data

    def origin_xpath(self, xpath):
        """
        Args:
            xpath:
        """
        return self.etree.xpath(xpath)


def xpathParseList(htmlContent: str, xpathContent: str, separator: str = "") -> str:
    """
    Args:
        htmlContent (str):
        xpathContent (str):
        separator (str):
    """
    data = xpathParse(htmlContent, xpathContent)

    return separator.join(data)


# TODO
def jinglin(number):
    """
    Args:
        number:
    """
    status_code = 1000
    r = None
    while status_code > 300:
        time.sleep(1)
        print("wait for get proxy. number: ", number)

        r = requests.get(
            r"http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=" + str(
                number) + "&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=", timeout=15,
            headers=headers)

        print("finish. status: {}".format(r.status_code))
        status_code = r.status_code

    proxyList = r.content.decode("utf-8").split("\r\n")

    return proxyList

# def rebuild_duplication_info(rdb: redis.Redis, table: peewee.Model, primary_key: str, duplicated: list, key):
#     all_key = []
#     all_key.extend(duplicated)
#     all_key.append("*")
#     for k in rdb.keys(":".join(all_key)):
#         rdb.delete(k)
#     print("delete exist keys")
#
#     count = table.select().count()
#     for i in range(1000, count + 1000, 1000):
#         end = i
#         start = end - 1000
#
#         for item in table.select().where(
#                 (getattr(table, primary_key) > start) & (getattr(table, primary_key) < end)):
#             # print(item)
#             rdb.set("".join([":".join(duplicated), ":", getattr(item, key)]), 1)
#         print("done start: {0}. end: {1}".format(start, end))
