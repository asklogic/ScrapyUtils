from typing import List
from base.Prepare import Prepare
from base.Scraper import Scraper, RequestScraper
from base.lib import Task

import scrapy_config
import json

class ProjectBasePrepare(Prepare):
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

class QueryProjectPrepare(Prepare):
    @classmethod
    def scraper_prepared(cls) -> Scraper:
        r = RequestScraper()
        r.set_timeout(5)
        return r

    @classmethod
    def task_prepared(cls) -> List[Task]:
        data = []
        with open(scrapy_config.Assets_Path + "/code_name.json") as f:
            data.extend(json.load(f))
        print(len(data))


        for i in data[0:10000]:
            t = Task()
            t.url = "http://xxgx.scjst.gov.cn/api/getdata/GetPerjectList"
            t.param = i
            yield t
        pass