import celery
import queue
import time
from multiprocessing import Pipe, Process, Queue
import multiprocessing

condition = multiprocessing.Condition()


def queueFeed(q: Queue):
    if q.qsize() < 51:
        print("feed")
        for i in range(50):
            q.put(i)


def queuePersistenceFeed(q: Queue):
    while True and q.qsize() < 51:
        print("feed")
        for i in range(50):
            q.put(i)
            print("put ", i)


def queueDump(q: Queue):
    for i in range(20):
        q.get(timeout=10)
    print("dump finish")


def feed(q: Queue):
    while True:
        if condition.acquire():
            if q.qsize() < 20:
                print("feed")
                for i in range(50):
                    q.put(i)

        condition.release()
        time.sleep(0.5)
        # print("loop")

f = feed
q = Queue()
pf = Process(target=f, args=(q,))
# pf.start()



def test():
    q = Queue()
    pf = Process(target=queueFeed, args=(q,))
    # pd = Process(target=queueDump, args=(q,))
    pf.start()
    # pd.start()
    # pd.join()

    for i in range(20):
        q.get(timeout=10)
    pf.join()
    pf.terminate()
    # pd.terminate()
    # print(q.qsize())


def pipeTest():
    pipe = Pipe(duplex=True)
    pipe[0].send(1)

    res = pipe[1].recv()
    print(res)


if __name__ == '__main__':
    pf = Process(target=feed, args=(q,))
    pf.start()
    # pipeTest()
    # test()
