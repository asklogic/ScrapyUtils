from base.lib import Parse, ModelManager
from .model import ipModel, proxyModel, ProjectModel, ViewstateModel

# temp
from old.base.tools import xpathParse


class testParse(Parse):

    def parsing(self, content: str, manager: ModelManager):
        items = xpathParse(htmlContent=content, xpathContent=r'//*[@id="result"]/div/p[1]/code')
        m = ipModel()
        m.ip = items[0]
        yield m


class JustForTestParse(Parse):
    def parsing(self, content: str, manager: ModelManager):
        items = xpathParse(htmlContent=content, xpathContent=r'//*[@id="result"]/div/p[1]/code')
        m = ipModel()
        m.ip = items[0]
        yield m


class IpProxyParse(Parse):
    def parsing(self, content: str, manager: ModelManager):
        ip = xpathParse(content, r'//*[@id="list"]/table/tbody/tr/td[1]')
        port = xpathParse(content, r'//*[@id="list"]/table/tbody/tr/td[2]')
        an = xpathParse(content, r'//*[@id="list"]/table/tbody/tr/td[3]')
        scheme = xpathParse(content, r'//*[@id="list"]/table/tbody/tr/td[4]')

        for i in range(15):
            m = proxyModel()
            m.ip = ip[i]
            m.port = port[i]
            m.anonymous = an[i]
            m.type = scheme[i]
            yield m


class ProjectParse(Parse):
    def parsing(self, content: str, manager: ModelManager):
        urls = xpathParse(content, '//*[@id="right_content"]/div[2]/table/tbody/tr/td[3]/a/@href')
        titles = xpathParse(content, '//*[@id="right_content"]/div[2]/table/tbody/tr/td[3]/a')
        locations = xpathParse(content, '//*[@id="right_content"]/div[2]/table/tbody/tr/td[2]')
        for i in range(len(urls)):
            p = ProjectModel()
            p.url = urls[i]
            p.title = titles[i]
            p.location = locations[i]

            yield p


class ReqProjectParse(Parse):
    def parsing(self, content: str, manager: ModelManager):
        urls = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a/@href')
        titles = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a')
        locations = xpathParse(content, '//*[@class="page-content"]/table/tr/td[2]')
        xpathParse(content, '//*[@class="page-content"]//tr/td[2]')
        for i in range(len(urls)):
            p = ProjectModel()
            p.url = urls[i]
            p.title = titles[i]
            p.location = locations[i]

            yield p


class viewStateParse(Parse):
    def parsing(self, content: str, manager: ModelManager):
        v = ViewstateModel()
        v.viewstate = xpathParse(content, '//*[@id="__VIEWSTATE"]//@value')[0]
        v.generator = xpathParse(content, '//*[@id="__VIEWSTATEGENERATOR"]//@value')[0]
        v.validation = xpathParse(content, '//*[@id="__EVENTVALIDATION"]//@value')[0]
        yield v
