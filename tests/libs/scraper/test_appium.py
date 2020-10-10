import unittest
import os
from appium import webdriver
from ScrapyUtils.libs import Scraper, AppiumScraper

desired_caps = {}
desired_caps["platformName"] = "Android"
desired_caps["platformVersion"] = "5.1.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["newCommandTimeout"] = "3000"
desired_caps["noReset"] = "True"
desired_caps["appPackage"] = r"com.homelink.android"
desired_caps["appActivity"] = r"com.homelink.android.SplashScreenActivity"


# desired_caps = {"platformName": "Android",
#                 "platformVersion": "5.1.1",
#                 "deviceName": "127.0.0.1:62001",
#                 "newCommandTimeout": "3000",
# 'noReset': "True",
#                 "appPackage": "com.youpin.comic",
#                 "appActivity": "com.youpin.comic.welcomepage.WelcomeActivity",
#                 }

# driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)


# class AppiumScraper(Scraper):
#
#     def __init__(self, desired, ):
#         super(AppiumScraper, self).__init__()
#
#
#
#         pass
#
#     def _activate(self):
#         pass
#
#     def _clear(self):
#         pass
#
#     def _quit(self):
#         pass

def get_devices():
    with os.popen('adb devices') as p:
        content = p.read()
    addresses = [x.split('\t')[0] for x in content.split('\n') if x][1:]

    port = [x.split(':')[1] for x in addresses]

    return addresses, port


class TestAppiumCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)

    def test_function_get_devices(self):
        # TODO: test it.
        get_devices()


if __name__ == "__main__":
    unittest.main()
