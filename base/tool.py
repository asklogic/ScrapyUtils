from lxml import etree
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import requests
from base.Model import ProxyModel
import time

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


def xpathParseList(htmlContent: str, xpathContent: str, separator: str = "") -> str:
    data = xpathParse(htmlContent, xpathContent)

    return separator.join(data)


# TODO
def jinglin(number):
    status_code = 1000
    r = None
    while status_code > 300:
        time.sleep(1)
        print("wait for get proxy. number: ", number)

        r = requests.get(
            r"http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=" + str(
                number) + "&time=100&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=", timeout=15,
            headers=headers)

        print("finish. status: {}".format(r.status_code))
        status_code = r.status_code

    proxyList = r.content.decode("utf-8").split("\r\n")

    return proxyList


def get_proxy_model(number: int) -> List[ProxyModel]:
    proxy_list = jinglin(number)
    for p in proxy_list:
        m = ProxyModel()
        m.ip = p.split(":")[0]
        m.port = p.split(":")[1]
        yield m
