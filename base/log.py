import logging

# ScrapyUtils status log
# TODO 日志请求等级
StatusLog = logging.getLogger('main')
StatusLog.setLevel(logging.DEBUG)

StatusLog.propagate = 0

status_formatter = r"%(asctime)s - (%(threadName)s) - %(funcName)s [%(levelname)s] %(message)s"
status_formatter = r"%(asctime)s - (%(threadName)s) - [%(levelname)s] %(message)s"
status_f = logging.Formatter(status_formatter)

chHandler = logging.StreamHandler()
chHandler.setFormatter(status_f)
chHandler.setLevel(logging.DEBUG)
StatusLog.addHandler(chHandler)

# StatusLog.info("status logger startup")

# scraping log
ActLog = logging.getLogger('brief')
ActLog.setLevel(logging.DEBUG)
ActLog.propagate = 0

act_formatter = r"(%(levelname)s) %(message)s"
act_f = logging.Formatter(act_formatter)
chHandler = logging.StreamHandler()
chHandler.setFormatter(act_f)
chHandler.setLevel(logging.DEBUG)
ActLog.addHandler(chHandler)

# ActLog.info("act logger startup")


logging.debug('add default handler')
logging.debug('add brief handler')


status = StatusLog
act = ActLog



class theLog(object):
    defaultLog: logging.Logger = StatusLog

    # def __init__(self):
    #     defaultLog: logging.Logger = log

    @classmethod
    def msg(self, message=None):
        StatusLog.info(msg=message)


if __name__ == '__main__':
    print('logger test!')
    StatusLog.info('info')
    StatusLog.warning('warning')
    StatusLog.debug('debug')
    StatusLog.error("error")

    ActLog.error("[Scheme] TestAction failed")
