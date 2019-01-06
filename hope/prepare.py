from typing import List

from base.Prepare import Prepare

# temp
from base.Scraper import Scraper, RequestScraper
from base.lib import Task

class XmgkPrepare(Prepare):
    name = "xmgk"

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(5)
        return r

    @classmethod
    def task_prepared(cls) -> List[Task]:
        for i in range(1, 201):
            t = Task()
            t.url = "http://xmgk.scjst.gov.cn/QueryInfo/Project/ProjectList.aspx"
            t.param = i
            yield t


class QueryPrepare(Prepare):
    name = "query"

    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(5)
        return r

    @classmethod
    def task_prepared(cls) -> List[Task]:
        import json
        d = None
        with open(r"D:\cloudWF\Python\ScrapyUtils\assets\data\data.json") as f:
            d = json.load(f)

        titles = list(map(lambda x: x["title"], d))
        codes = list(map(lambda x: x["code"], d))


        for index in range(len(codes)):
            t = Task()
            t.param = titles[index] + ":" + codes[index]
            t.url = "http://xxgx.scjst.gov.cn/api/getdata/GetPerjectList"

            yield t

        pass
