# -*- coding: utf-8 -*-
import unittest
import os
# from appium import webdriver

# from ScrapyUtils.libs import Scraper, AppiumScraper

desired_caps = {}
desired_caps["platformName"] = "Android"
desired_caps["platformVersion"] = "7.1.2"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["newCommandTimeout"] = "3000"
desired_caps["noReset"] = "True"
desired_caps["appPackage"] = r"com.homelink.android"
desired_caps["appActivity"] = r"com.homelink.android.SplashScreenActivity"


def get_devices():
    with os.popen('adb devices') as p:
        content = p.read()
    addresses = [x.split('\t')[0] for x in content.split('\n') if x][1:]

    port = [x.split(':')[1] for x in addresses]

    return addresses, port


class TestAppiumCase(unittest.TestCase):
    def test_function_get_devices(self):
        # TODO: test it.
        # get_devices()
        pass


if __name__ == "__main__":
    unittest.main()
