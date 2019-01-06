import unittest
from unittest import TestCase

import sys

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base import Scraper


class scraper_Test(TestCase):
    def test_project(self):
        pass
        self.assertEqual(1, 1)

    def Requests_scraper(self):
        r = Scraper.RequestScraper()

        # Done
        # self.assertIsInstance(r, Scraper.RequestScraper)
        # current
        # self.assertIn("ip", r.get(r"https://ip.cn/"))
        # self.assertIn("118.113.128.40", r.get(r"https://ip.cn/"))
        # proxy get
        # r.set_proxy("121.61.82.166:26534")
        # self.assertIn("121.61.82.166", r.get(r"https://ip.cn/"))

        pass

if __name__ == '__main__':
    unittest.main()
