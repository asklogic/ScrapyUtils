import unittest

from ScrapyUtils.core import *
from ScrapyUtils.core.collect import scheme_start, scheme_initial, scheme_preload


class SchemeStartTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        scheme_preload('atom')
        scheme_initial({})

    def test_something(self):
        scheme_start()


if __name__ == '__main__':
    unittest.main()
