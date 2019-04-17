from unittest import TestCase

import sys

sys.path.insert(0, r"E:\cloudWF\python\ScrapyUtils")

from base.libs.scraper import FireFoxScraper


class TestFireFoxScraper(TestCase):

    def test_init(self):
        # return
        # f: FireFoxScraper = FireFoxScraper(headless=False)
        #
        # f.quit()
        pass

    def test_get(self):
        # return

        f: FireFoxScraper = FireFoxScraper(headless=True)

        f.start_tab()


        # driver = f.getDriver()
        #
        #
        # f.get("https://ip.cn/")
        #
        # print(driver.find_element_by_xpath('//*[@id="result"]/div/p[1]/code').text)
        #
        # f.set_proxy(['125.120.9.174', '26716'])
        # f.get("https://ip.cn/")
        #
        # print(driver.find_element_by_xpath('//*[@id="result"]/div/p[1]/code').text)
        f.quit()

