import sys
from base.command import build_run

if __name__ == '__main__':
    try:
        # import scrapy_config
        pass
    except Exception as e:
        print(e)
        print("import error")
    build_run(None, sys.argv)
