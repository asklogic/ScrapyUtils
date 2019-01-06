from typing import Generator

from base.Model import ModelManager, Model
from base.Parse import Parse
from base.tool import xpathParse
from .model import ProxyModel


class NewParse(Parse):
    name = "xpathParse"

    def parsing(self, content: str, manager: ModelManager) -> Model or Generator[Model]:
        urls = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a/@href')
        titles = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a')
        locations = xpathParse(content, '//*[@class="page-content"]/table/tr/td[2]')
        codes = xpathParse(content, '//*[@class="page-content"]/table/tr/td[4]')
        xpathParse(content, '//*[@class="page-content"]//tr/td[2]')

        data = []
        for i in range(len(urls)):
            p = manager.model("ProjectModel")
            p.url = urls[i]
            p.title = titles[i]
            p.location = locations[i]
            p.code = codes[i]

            data.append(p)
        if len(data) != 20:
            raise Exception('wat?')
        return data
            # yield p


class QueryParse(Parse):

    def parsing(cls, content: str, manager: ModelManager) -> Model or Generator[Model]:
        import json
        data = json.loads(content)["Data"]
        # print(json.loads(content)["Count"])

        for item in data:
            m = manager.model("ProjectInfoModel")
            m.id = item["XMBH"]
            yield m

        # manager.get("CountModel")
        # m = manager.model("CountModel")
        # m.count = data
        # yield m
        # pass
