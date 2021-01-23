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

# import subprocess
# import os
# import cmd2
#
# current_folders = list(os.walk(os.getcwd()))[0][1]
#
# for i in range(len(current_folders)):
#     print(f'index: {i} - {current_folders[i]}')
#
# select = input('select folder:')
#
# target_folder = os.path.join(os.getcwd(), current_folders[select])
#
# # trans
#
# files = list(os.walk(target_folder))[0][2]
#
# pdf_files = [os.path.join(target_folder, x) for x in files if x.endswith('.pdf')]
#
# for pdf_file in pdf_files:
#     html_file = pdf_file.replace(".pdf", ".html")
#     subprocess.run(["pdf2htmlEX", pdf_files, html_file])
#
# # outputFilename = outputDir + filename.replace(".pdf", ".html")
# def demo():
#     import subprocess
#     import os
#     import cmd2
#
#     current_folders = list(os.walk(os.getcwd()))[0][1]
#
#     for i in range(len(current_folders)):
#         print(f'index: {i} - {current_folders[i]}')
#
#     select = input('select folder:')
#
#     target_folder = os.path.join(os.getcwd(), current_folders[int(select)])
#
#     # trans
#
#     files = list(os.walk(target_folder))[0][2]
#
#     pdf_files = [os.path.join(target_folder, x) for x in files if x.endswith('.pdf')]
#
#     for pdf_file in pdf_files:
#         html_file = pdf_file.replace(".pdf", ".html")
#         subprocess.run(["pdf2htmlEX", pdf_files, html_file])

import numpy as np
import pandas as pd
import jieba
from jieba import analyse

# df_news = pd.read_table(r'D:\RTW\python\ScrapyUtils\val.txt',names=['category','theme','URL','content'],encoding='utf-8')
# df_news = df_news.dropna()
#
# #
# content = df_news.content.values.tolist()
#
# content_S = []
# for line in content:
#     current_segment = jieba.lcut(line)
#     if len(current_segment) > 1 and current_segment != "\r\n":
#         content_S.append(current_segment)
# print(content_S[2])
#
# index = 1000
# print(df_news["content"][index])
# content_S_str = "".join(content_S[index])
# print(content_S_str)
# print(" ".join(analyse.extract_tags(content_S_str,topK=5)))

# with open(r'D:\RTW\python\ScrapyUtils\val.txt') as f:
#     content = f.read()

content = """
Qualcomm teased the Snapdragon 888, its latest 5G-equipped flagship smartphone processor, on the first day of its Snapdragon Tech Summit. But at the day two keynote, the company provided all of the details on the new chipset, which will be the brains powering almost every major 2021 Android flagship.

First off, the basic specs: the new processor will feature Qualcomm’s new Kryo 680 CPU, which will be one of the first devices to feature Arm’s latest customized Cortex-X1 core and promises up to 25 percent higher performance than last year’s chip with a maximum clock speed of 2.84GHz. And the company’s new Adreno 660 GPU promises a 35 percent jump on graphics rendering, in what it says is the biggest performance leap for its GPUs yet. The new CPU and GPU are also more power-efficient compared to those on the Snapdragon 875, with a 25 percent improvement for the Kyro 680 and a 20 percent improvement on the Adreno 660.

Another key difference between the Snapdragon 888 and last year’s 865 is that Qualcomm has finally integrated its 5G modem directly into the SoC. That means manufacturers won’t have to deal with finding the space (and power) for a second external modem. Specifically, the Snapdragon 888 will feature Qualcomm’s 5nm X60 modem, which the company announced back in February, and it will enable better carrier aggregation and download speeds up to 7.5 Gbps on new devices. The Snapdragon 888 will also support Wi-Fi 6 as well as the new 6GHz Wi-Fi 6E standard, which should boost that rollout by making it the default on most Android flagships.

As is tradition for a Snapdragon update, Qualcomm is also putting a big emphasis on its camera improvements. The new Spectra 580 ISP is the first from Qualcomm to feature a triple ISP, allowing it to do things like capture three simultaneous 4K HDR video streams or three 28-megapixel photos at once at up to 2.7 gigapixels per second (35 percent faster than last year).

It also offers improved burst capabilities and is capable of capturing up to 120 photos in a single second at a 10-megapixel resolution. Lastly, the upgraded ISP adds computational HDR to 4K videos, an improved low-light capture architecture, and the option to shoot photos in 10-bit color in HEIF. That said, it’ll be up to phone manufacturers to build cameras that can take advantage of the new features.

The final major changes come in AI performance, thanks to Qualcomm’s new Hexagon 780 AI processor. The Snapdragon 888 features Qualcomm’s sixth-generation AI Engine, which it promises will help improve everything from computational photography to gaming to voice assistant performance. The Snapdragon 888 can perform 26 trillion operations per second (TOPS), compared to 15 TOPS on the Snapdragon 865, while delivering three times better power efficiency. Additionally, Qualcomm is promising big improvements in both scalar and tensor AI tasks as part of those upgrades.

The Snapdragon 888 also features the second-generation Qualcomm Sensing Hub, a dedicated low-power AI processor for smaller hardware-based tasks, like identifying when you raise your phone to light up the display. The new second-gen Sensing Hub is dramatically improved, which means the phone will be able to rely less on the main Hexagon processor for those tasks.

All of this adds up to a substantial boost in Qualcomm’s — and therefore, nearly every Android flagship’s — capabilities for what our smartphones will be able to do. The first Snapdragon 888 smartphones are expected to show up in early 2021, which means it won’t be long before we’ll be able to try out the next generation of Android flagships for ourselves.

"""

# jieba.analyse.set_stop_words(r'D:\RTW\python\ScrapyUtils\val.txt')
# text_tags = jieba.analyse.extract_tags(content, topK=30)
#
# print(text_tags)


from twocaptcha import TwoCaptcha

solver = TwoCaptcha('b7e7611a72e9c3362a1f95c1371e45a8')