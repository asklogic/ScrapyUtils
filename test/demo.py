from selenium import webdriver
import requests

import os
import json
import scrapy_config
from scjst_base.peewee_connect import ProjectBase


def init():
    urls = []
    for i in range(10):
        print("url get: ", i)
        urls.extend(list(map(lambda x: x.url, ProjectBase.select().where(
            (ProjectBase.UID > 10000 * i) & (ProjectBase.UID < 10000 * (i + 1))).execute())))

    with open(scrapy_config.Assets_Path + "/urls.json", "w") as f:
        json.dump(urls, f)

    print(len(urls))


def inti_code_name():
    code_name = []
    for i in range(10):
        print("url get: ", i)
        code_name.extend(list(
            map(lambda x: (x.code if x.code else "") + "-:-" + (x.title if x.title else ""), ProjectBase.select().where(
                (ProjectBase.UID > 10000 * i) & (ProjectBase.UID < 10000 * (i + 1))).execute())))

    with open(scrapy_config.Assets_Path + "/code_name.json", "w") as f:
        json.dump(code_name, f)

    print(len(code_name))


def detect():
    data = []
    with open(scrapy_config.Assets_Path + "/3000-4000.json") as f:
        data.extend(json.load(f))

    with open(scrapy_config.Assets_Path + "/4000+.json") as f:
        data.extend(json.load(f))

    with open(scrapy_config.Assets_Path + "/urls.json") as f:
        urls = json.load(f)

    newdata = []

    # for item in data:
    #     if len(ProjectBase.select().where(ProjectBase.url == item.get("url"))) == 0:
    #         newdata.append(item)
    #         print("new!")
    #     else:
    #         print("nope!")

    for item in data:
        if not item.get('url') in urls:
            newdata.append(item)
            # print("new!")
        else:
            pass
            print("nope!")
    print("new: ", len(newdata))
    for i in range(int(len(newdata) / 1000) + 2):
        start = i * 1000
        end = i * 1000 + 1000
        split_data = newdata[start:end]
        print(start, end)
        # print(len(split_data))
        if split_data:
            ProjectBase.insert_many(split_data).execute()
    print(len(newdata))


# init()
inti_code_name()
# detect()
