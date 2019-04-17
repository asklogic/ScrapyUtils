import multiprocessing

condition = multiprocessing.Condition()

from base.libs import scraper

f = scraper.FireFoxScraper(headless=False)


f.activate()


