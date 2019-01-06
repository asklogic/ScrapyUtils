import logging

log = logging.getLogger('main')
log.setLevel(logging.DEBUG)

log.info("logger startup")
log.propagate = 0

formatter = r"%(asctime)s - (%(threadName)s) - %(funcName)s [%(levelname)s] %(message)s"
f = logging.Formatter(formatter)

chHandler = logging.StreamHandler()
chHandler.setFormatter(f)
chHandler.setLevel(logging.DEBUG)
log.addHandler(chHandler)

####


briefLog = logging.getLogger('brief')
briefLog.setLevel(logging.DEBUG)
formatter = r"[%(levelname)s] %(message)s"
f = logging.Formatter(formatter)

briefLog.propagate = 0

chHandler = logging.StreamHandler()
chHandler.setFormatter(f)
chHandler.setLevel(logging.DEBUG)
briefLog.addHandler(chHandler)

logging.debug('add default handler')
logging.debug('add brief handler')



def getLog():
    return log

def getbriefLog():
    return briefLog

if __name__ == '__main__':
    print('logger test!')
    log.info('info')
    log.warning('warning')
    log.debug('debug')
    log.error("error")

