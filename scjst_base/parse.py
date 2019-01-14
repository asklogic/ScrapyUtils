from typing import Generator

from base.Model import ModelManager, Model
from base.Parse import Parse

from base.tool import xpathParse


from scjst_base.peewee_connect import ProjectBase

class ProjectBaseParse(Parse):
    def parsing(cls, content: str, manager: ModelManager) -> Model or Generator[Model]:
        urls = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a/@href')
        titles = xpathParse(content, '//*[@class="page-content"]/table/tr/td[3]/a')
        locations = xpathParse(content, '//*[@class="page-content"]/table/tr/td[2]')
        codes = xpathParse(content, '//*[@class="page-content"]/table/tr/td[4]')
        dates = xpathParse(content, r'//*[@class="page-content"]/table/tr/td[5]')
        page = xpathParse(content, r'//*[@class="cpb"]')

        data = []
        for i in range(len(urls)):
            p = manager.model("ProjectBaseModel")
            p.url = urls[i]
            p.title = titles[i]
            p.location = locations[i]
            p.code = codes[i]
            p.date = dates[i]
            # p.page = page

            # if ProjectBase.select().where(ProjectBase.url == p.url):
            #     continue

            data.append(p)
        if len(data) != 20:
            raise Exception('wat?')
        return data


class QueryParse(Parse):
    def parsing(cls, content: str, manager: ModelManager) -> Model or Generator[Model]:
        import json
        data = json.loads(content)["Data"]
        # print(json.loads(content)["Count"])

        for item in data:
            m = manager.model("ProjectIDModel")
            m.id = item["XMBH"]
            yield m