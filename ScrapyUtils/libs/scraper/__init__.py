# -*- coding: utf-8 -*-
"""The scraper module for scrapy data.

爬取核心类，负责与网页或者其他数据来源交互，获得数据。

其中设定了爬取基本类Scraper，规定了所有爬取类的通用方法，具体的其他方法需要通过子类的Mixin导入。



样例:
    启动自带的Scraper或者自定义Scraper::

        scraper = RequestScraper()

    必须先attach之后再进行使用::

        scraper.scraper_attach()

    通用方法包括'重启'、'清理'和'返回爬取实例'，都需要子类自定义::

        scraper.scraper_clear()
        scraper.scraper_restart()
        scraper.get_driver()

    对于基于Selenium之类的Scraper，最好执行退出::

        scraper.scraper_detach()



Todo:
    * Appium Scraper
    * Chrome Scraper
"""
from importlib import import_module

from ._base_scraper import Scraper

# dynamic import
module_mapper = {
    # 'appium_scraper': [],
    'chrome_scraper': ['selenium'],
    'firefox_scraper': ['selenium'],
    'request_scraper': ['requests'],
}

for sub_module, libs in module_mapper.items():
    try:

        for _ in libs:
            import_module(_)

    except ModuleNotFoundError as mnfe:
        pass
    else:
        __import__('ScrapyUtils.libs.scraper.'+sub_module)
