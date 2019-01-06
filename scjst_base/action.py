from base.lib import Action, Task
from old.base.tools import requestScraper


class Scjst_baseAction(Action):
    def scraping(self, task: Task, scraper):
        scraper: requestScraper
        v = self.manager.get("ViewStateModel")[0]
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
