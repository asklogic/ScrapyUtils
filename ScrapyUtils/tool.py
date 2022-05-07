from lxml import etree
from typing import TypeVar, Generic, Tuple, List, Dict, Union, Generator
import requests
import time
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
