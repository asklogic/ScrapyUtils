import sys

if __name__ == '__main__':
    try:
        import scrapy_config
        from base.command import build_run

    except Exception as e:
        print(e)
        print("import error")
    build_run(scrapy_config, sys.argv)
