import signal
import threading
import time

i = 5


def test_thread(asd):
    global i
    remain = i

    while i > 0:
        i = i - 1
        time.sleep(1)
        print('loop')


def signal_test(signum, frame):
    print('stop')


# if __name__ == '__main__':
#     signal.signal(signal.SIGINT, signal_test)
#
#     t = threading.Thread(target=test_thread)
#     t.start()
#     # t.join()
#     t.join()


# import signal
#
def signal_handler(signum, stack):
    print('Received:', signum)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':

    t = threading.Thread(target=test_thread, args=(1,))
    # t.setDaemon(True)

    t.start()
    # t.join()

    print('end?')
    # remain = 5
    # while remain:
    #     remain = remain - 1
    #     print('Waiting...try kill using signal 2(SIGINT)')
    #     time.sleep(0.5)
