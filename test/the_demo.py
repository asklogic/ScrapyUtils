import celery
import queue
import time
from multiprocessing import Pipe, Process, Queue
import multiprocessing

condition = multiprocessing.Condition()


from base import core, Scraper

f = Scraper.FireFoxScraper(headless=False)


f.activate()


