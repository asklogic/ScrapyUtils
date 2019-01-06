from base.Action import Action
from base.Model import ModelManager
from base.Scraper import Scraper, RequestScraper
from base.lib import Task
import time

from urllib import parse


class newAction(Action):
    name = "ActionName"

    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: type) -> str:
        return scraper.get(url=task.url)


class NextPageAction(Action):
    name = "next"

    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: ModelManager) -> str:
        scraper: RequestScraper
        v = manager.get("view")[0]
        data = {
            '__VIEWSTATE': v.viewstate,
            '__VIEWSTATEGENERATOR': v.generator,
            '__EVENTTARGET': "ctl00$mainContent$gvBiddingResultPager",
            '__EVENTARGUMENT': str(task.param),
            '__EVENTVALIDATION': v.validation,
            'ctl00$mainContent$txt_entename': '',
            'ctl00$mainContent$cxtj': '',
            'UBottom1:dg1': '',
            'UBottom1:dg2': '',
            'UBottom1:dg3': '',
            'UBottom1:dg4': '',
            'UBottom1:dg5': '',
            'UBottom1:dg6': '',
        }
        return scraper.post(url=task.url, data=data)


class QueryNameAction(Action):
    name = "queryname"
    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: ModelManager) -> str:


        url = task.url
        scraper: RequestScraper = scraper
        scraper._headers["Referer"] = "http://xxgx.scjst.gov.cn/Project/pList.aspx"
        trueQuery = {
            "lb": "",
            "bh": "",
            "mc": task.param.split(":")[0],
            "dw": "",
            "dq": "",
            "validate": "",
        }

        trueQuery = str(trueQuery).replace("'", '"')

        params = {
            "id": parse.quote_plus(trueQuery)
        }
        # fixme 自带解析出错
        url = url + "?id=" + parse.quote_plus(trueQuery)
        return scraper.get(url=url)


class QueryCodeAction(Action):
    name = "querycode"
    @classmethod
    def scraping(cls, task: Task, scraper: Scraper, manager: ModelManager) -> str:
        time.sleep(0.1)


        url = task.url
        scraper: RequestScraper = scraper
        scraper._headers["Referer"] = "http://xxgx.scjst.gov.cn/Project/pList.aspx"
        trueQuery = {
            "lb": "",
            "bh": task.param.split(":")[1],
            "mc": "",
            "dw": "",
            "dq": "",
            "validate": "",
        }

        trueQuery = str(trueQuery).replace("'", '"')

        params = {
            "id": parse.quote_plus(trueQuery)
        }
        # fixme 自带解析出错
        url = url + "?id=" + parse.quote_plus(trueQuery)
        return scraper.get(url=url)
