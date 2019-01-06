from base.lib import Action, Task
from old.base.tools import baseScraper, firefoxScraper,requestScraper
from selenium.webdriver import Firefox


class testAction(Action):
    def scraping(self, task: Task, scraper: baseScraper):
        return scraper.getPage(url="https://ip.cn/")


class ProxyAction(Action):
    def scraping(self, task: Task, scraper: baseScraper):
        return scraper.getPage(url=task.url)


class HomeAction(Action):
    def scraping(self, task: Task, scraper: baseScraper):
        return scraper.getPage(url=task.url)


class NextPageAction(Action):
    def scraping(self, task: Task, scraper: baseScraper):
        scraper: firefoxScraper
        driver: Firefox = scraper.getDriver()

        pagination = str(task.param)
        scripts = "__doPostBack('ctl00$mainContent$gvBiddingResultPager','{0}')".format(pagination)
        import time
        driver.execute_script(scripts)
        time.sleep(5)
        return driver.page_source

class ReqNextPageAction(Action):
    def scraping(self, task: Task, scraper: baseScraper):
        scraper : requestScraper
        v = self.manager.get("ViewstateModel")[0]
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


# class otherTestAction(Action):
#     def scraping(self, task: Task, scraper: baseScraper):
#         pass