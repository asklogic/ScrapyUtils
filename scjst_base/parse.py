from base.lib import Parse, ModelManager

from old.base.tools import xpathParse
from scjst_base.model import *

class Scjst_baseParse(Parse):
    def parsing(self, content: str, manager: ModelManager):
        urls = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a/@href')
        titles = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a')
        locations = xpathParse(content, '//*[@class="page-content"]/table/tr/td[2]')
        xpathParse(content, '//*[@class="page-content"]//tr/td[2]')
        for i in range(len(urls)):
            p = Scjst_baseModel()
            p.url = urls[i]
            p.title = titles[i]
            p.location = locations[i]

            yield p


class ViewStateParse(Parse):

    def parsing(self, content: str, manager: ModelManager):
        v = ViewStateModel()
        v.viewstate = xpathParse(content, '//*[@id="__VIEWSTATE"]//@value')[0]
        v.generator = xpathParse(content, '//*[@id="__VIEWSTATEGENERATOR"]//@value')[0]
        v.validation = xpathParse(content, '//*[@id="__EVENTVALIDATION"]//@value')[0]
        yield v
