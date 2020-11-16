import unittest

from ScrapyUtils.core import *

from tests.telescreen import schemes_path
from importlib import import_module

from ScrapyUtils.components import *
from ScrapyUtils.libs import *
from queue import Queue

from ScrapyUtils.core.collect import *


class TestCollect(unittest.TestCase):
    def test_main_process(self):
        # scheme_preload('TestFirefox')
        scheme_preload('atom')

        # global command instance
        # scheme_command_alter()

        scheme_initial({})

        # confirm here.
        # scraper active here.
        # log out.
        scheme_start()

        scheme_exit()



if __name__ == '__main__':
    unittest.main()

    # scheme_preload('atom')
    pass
