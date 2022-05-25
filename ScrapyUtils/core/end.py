# -*- coding: utf-8 -*-
"""退出.



Todo:
    * 异常处理:

"""

from ScrapyUtils import configure


def _suit_exit():
    # scrapers:
    for scraper in configure.scrapers:
        scraper.scraper_detach()

    # suits:
    # actions
    [suit.suit_exit() for suit in configure.action_suits]
    # processor
    configure.processor_suit.suit_exit()


def end():
    _suit_exit()
