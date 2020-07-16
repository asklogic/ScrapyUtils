import unittest
import os

import importlib
from typing import List
from queue import Queue

from base.libs import Scraper, RequestScraper

from tests.telescreen import tests_path, schemes_path

os.path.join(schemes_path)


def _load_profile(scheme_path, profile_name: str = 'profile.py'):
    """
    Args:
        scheme_path:
        profile_name (str):
    """
    assert os.path.exists(scheme_path)
    assert os.path.isdir(scheme_path)

    profile: str = os.path.join(scheme_path, profile_name)

    scheme = os.path.basename(scheme_path)

    # TODO: imp
    module = importlib.import_module(scheme + '.' + profile_name.split('.')[0])
    return module


def _invoke_scraper():
    pass


def collect_profile(scheme_path, profile_name: str = 'profile.py'):
    """
    Args:
        scheme_path:
        profile_name (str):
    """
    module = _load_profile(scheme_path, profile_name)
    config = {}

    # common setting(
    config['thread'] = getattr(module, 'THREAD', 5)
    config['timeout'] = getattr(module, 'TIMEOUT', 1.5)

    # Task
    task = getattr(module, 'generate_tasks')

    task_queue = Queue()
    for t in list(task()):
        task_queue.put(t)
    config['task_queue'] = task_queue

    # TODO: step setting
    # TODO: processor setting

    # scraper
    scraper_callable = getattr(module, 'generate_scraper')

    scrapers: List[Scraper] = []

    # TODO: refact thread.
    for i in range(config['thread']):
        try:
            scraper = scraper_callable()
            assert isinstance(scraper, Scraper)
            scrapers.append(scraper)
        except Exception as e:
            scraper = RequestScraper()
            scraper.scraper_activate()
            scrapers.append(scraper)

    config['scrapers'] = scrapers

    return config


class TestProfile(unittest.TestCase):

    def test_load_file(self):
        error = os.path.join(schemes_path, 'test_collect_active')

        # with self.assertRaises(AssertionError) as ae:
        #     _load_profile(error)
        with self.assertRaises(ModuleNotFoundError) as me:
            _load_profile(error)

        atom = os.path.join(schemes_path, 'atom')
        _load_profile(atom)

    def test_collect_profile(self):
        atom = os.path.join(schemes_path, 'atom')
        config = collect_profile(atom)

        assert isinstance(config, dict)
        assert config.get('thread') == 5
        assert config.get('timeout') == 1.5

        assert isinstance(config.get('task_queue'), Queue)
        assert config.get('task_queue').qsize() == 10

        assert len(config.get('scrapers')) == 5 == config.get('thread')
        assert isinstance(config.get('scrapers'), list)

        for scraper in config.get('scrapers'):
            assert isinstance(scraper, Scraper)
            assert scraper.activated is True


if __name__ == '__main__':
    unittest.main()
