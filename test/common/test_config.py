from unittest import TestCase

import sys

sys.path.insert(0, r"E:\cloudWF\python\ScrapyUtils")

import scrapy_config
from base.lib import Config


class TestConfig(TestCase):

    def test_init(self):
        config_file = scrapy_config
        config_name = "test_core"

        target_config: dict = getattr(config_file, config_name)
        # default
        if not target_config.get("job"):
            target_config["job"] = config_name

        config = Config(config_file, config_name)

        print("\n")
        print(config.job)
        print(config.prepare)
        print(config.schemes)
        print(config.models)
        print(config.process)
        print(config.project)

