import os


def my_name():
    print('mianmian')


def my_second():
    pass


if __name__ == '__main__':
    pass

    list()

# # import signal
# #
# # # Define signal handler function
# # def myHandler(signum, frame):
# #     """
# #     Args:
# #         signum:
# #         frame:
# #     """
# #     print("Now, it's the time")
# #     exit()
# #
# # # register signal.SIGALRM's handler
# # signal.signal(signal.SIGALRM, myHandler)
# # signal.alarm(5)
# # while True:
# #     print('not yet')
# from ScrapyUtils.libs.scraper import FirefoxScraper
#
# import asyncio
#
# import time
#
#
# async def async_print(n, t=5):
#     # for i in range(t):
#     #     await asyncio.sleep(1)
#     #     time.sleep(1)
#     # print(n,i)
#     await asyncio.sleep(1)
#
#     print(n, 'do something')
#     f = FirefoxScraper()
#     f.scraper_activate()
#
#     print(n, 'something done.')
#     f.scraper_quit()
#
#
# async def await_coroutine(*args):
#     await async_print(5)
#     # await asyncio.sleep(2)
#
#

# def run(coroutine):
#     print('start')
#     try:
#         coroutine().send(None)
#
#     except StopIteration as e:
#         return e.value
#     finally:
#         print('end')
#
#
# # run(async_print)
#
# # with await_coroutine():
# #     pass
#
# # await_coroutine().send(None)
#
#
# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)
#
#
# # async def main():
# #     print(f"started at {time.strftime('%X')}")
# #
# #     await say_after(1, 'hello')
# #     await say_after(2, 'world')
# #
# #     print(f"finished at {time.strftime('%X')}")
#
# # async def main():
# #     task1 = asyncio.create_task(
# #         say_after(1, 'hello'))
# #
# #     task2 = asyncio.create_task(
# #         say_after(2, 'world'))
# #
# #     print(f"started at {time.strftime('%X')}")
# #
# #     # Wait until both tasks are completed (should take
# #     # around 2 seconds.)
# #     await task1
# #     await task2
# #
# #     print(f"finished at {time.strftime('%X')}")
#
#
# async def factorial(name, number):
#     f = 1
#     for i in range(2, number + 1):
#         print(f"Task {name}: Compute factorial({i})...")
#         await asyncio.sleep(1)
#         f *= i
#     print(f"Task {name}: factorial({number}) = {f}")
#
#
# async def main():
#     # Schedule three calls *concurrently*:
#     await asyncio.gather(
#         # factorial("A", 2),
#         # factorial("B", 3),
#         # factorial("C", 4),
#         async_print(n='A'),
#         async_print(n='B'),
#         async_print(n='C'),
#     )
#
#
# asyncio.run(main())
#
# from concurrent.futures.thread import ThreadPoolExecutor
#
# executor = ThreadPoolExecutor(10)
# loop = asyncio.get_event_loop()
#
# loop.run_in_executor()

# import time
#
# from threading import Thread
#
#
# class Watcher(Thread):
#
#     def run(self):
#         char_list = ['-', '\\', '|', '/']
#         count = 0
#
#         while self.exit_flag:
#             time.sleep(self.delay)
#
#             print('\r' + self.start_content + ' ' + char_list[count % 4], end='', flush=True)
#
#             count += 1
#             if count * self.delay > self.timeout:
#                 break
#
#         print(f'\r{self.start_content} - {self.end_content}')
#
#     def __init__(self, timeout=20, start_content="Loading", end_content="Done!", delay=0.5,
#                  daemon=True) -> None:
#         super().__init__(daemon=daemon)
#
#         self.exit_flag = True
#         self.timeout = timeout
#         self.start_content = start_content
#         self.end_content = end_content
#         self.delay = delay
#
#         self.start()
#         self.current_time = time.time()
#
#     def exit_watch(self, spend=False):
#         self.exit_flag = False
#         spend_time = time.time() - self.current_time
#
#         self.join()
#         if spend:
#             print('spend time:', spend_time)
#
#
# print('Start here.')
#
# # w = Watcher(start_content='initialing')
# w = Watcher()
#
# time.sleep(3)
#
# w.exit_watch(True)
#
# print('End here.')

import subprocess
import os
import cmd2

current_folders = list(os.walk(os.getcwd()))[0][1]

for i in range(len(current_folders)):
    print(f'index: {i} - {current_folders[i]}')

select = input('select folder:')

target_folder = os.path.join(os.getcwd(), current_folders[select])

# trans

files = list(os.walk(target_folder))[0][2]

pdf_files = [os.path.join(target_folder, x) for x in files if x.endswith('.pdf')]

for pdf_file in pdf_files:
    html_file = pdf_file.replace(".pdf", ".html")
    subprocess.run(["pdf2htmlEX", pdf_files, html_file])

# outputFilename = outputDir + filename.replace(".pdf", ".html")
def demo():
    import subprocess
    import os
    import cmd2

    current_folders = list(os.walk(os.getcwd()))[0][1]

    for i in range(len(current_folders)):
        print(f'index: {i} - {current_folders[i]}')

    select = input('select folder:')

    target_folder = os.path.join(os.getcwd(), current_folders[int(select)])

    # trans

    files = list(os.walk(target_folder))[0][2]

    pdf_files = [os.path.join(target_folder, x) for x in files if x.endswith('.pdf')]

    for pdf_file in pdf_files:
        html_file = pdf_file.replace(".pdf", ".html")
        subprocess.run(["pdf2htmlEX", pdf_files, html_file])