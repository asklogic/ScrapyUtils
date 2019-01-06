from selenium import webdriver
import requests

import os

with open("E:\\cloudWF\\python\\ScrapyUtils\\custom\\actions.py", "a") as f:
    theStr = """ 

class NextPageAction(Action):
    def scraping(self, task: Task, scraper: baseScraper):
        scraper: firefoxScraper

        scripts = "__doPostBack('ctl00$mainContent$gvBiddingResultPager','{0}')".format(str(task.param))

        driver = scraper.getDriver()
        from selenium.webdriver import Firefox
        driver: Firefox
        driver.execute_script(scripts)
        import time
        time.sleep(5)

        return driver.page_source
"""

    f.writelines(theStr)
    pass