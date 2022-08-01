import os
import sys


# 外网测试
from os.path import dirname, abspath

http_switch = True

# scraper
firefox_scraper_switch = False
requests_scraper_switch = False

mock_project_home = os.path.join(dirname(abspath(__file__)), 'mock_project')
sys.path.insert(0, mock_project_home)
