import unittest
import cProfile
import time
import os

from ScrapyUtils.core.collect import *


class TestCollectInitialTestCase(unittest.TestCase):
    def test_something(self):
        print(configure.FILE_FOLDER_PATH)
        print(configure.DOWNLOAD_FOLDER_PATH)
        print(configure.SCHEME_PATH)

        scheme_preload('atom')

        print(configure.FILE_FOLDER_PATH)
        print(configure.DOWNLOAD_FOLDER_PATH)
        print(configure.SCHEME_PATH)

        time.sleep(0.1)

        collect_scheme_initial()

        scheme_exit()


if __name__ == '__main__':
    unittest.main()
