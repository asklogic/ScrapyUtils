from lxml import etree

headers = {
    'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    "Content-Type": "application/x-www-form-urlencoded",
    'Connection': 'close',
    'Cache-Control': 'max-age=0',
}


class XpathParser(object):
    etree: etree.HTML

    def __init__(self, html):
        assert type(html) == str, "html content must be str."

        self.etree = etree.HTML(html)

    def find_elements(self, xpath: str, child_text: bool = True):
        return self._get_result(xpath, child_text)

    def find_element(self, xpath: str, child_text: bool = True):
        if res := self._get_result(xpath, child_text):
            return res[0]

    def _get_result(self, xpath: str, child_text: bool):
        """根据xpath从etree解析结果中获取text结果

        child_text: 向下获取text不为空的结果
        """
        elements = self.etree.xpath(xpath)

        text_result = []
        for el in elements:
            if child_text:
                # 遍历子节点 直到找到有text的节点
                # next自动短路判断
                if (next := el.getchildren()) and (not el.text):
                    el = next[0]
                text_result.append(el.text)
            else:
                text_result.append(el.text)

        return text_result

    def origin_xpath(self, xpath):
        return self.etree.xpath(xpath)
