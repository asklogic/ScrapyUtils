from selenium import webdriver
import requests

import os
import json
import scrapy_config
from base.Model import Model
from scjst_base.peewee_connect import ProjectBase
from base.Process import Process, Pipeline
from faker import Faker
import threadpool


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


def insert_test():
    import peewee

    db = peewee.MySQLDatabase('scjst', user='root', password='87886700', host='logic-ol.me', port=3306,
                              charset='utf8mb4')

    class ProjectTest(peewee.Model):
        UID = peewee.PrimaryKeyField()
        location = peewee.CharField(null=True)
        url = peewee.CharField(null=False)
        code = peewee.CharField(null=True)

        class Meta:
            table_name = "Project_Test"

    ProjectTest.bind(db)
    ProjectTest.drop_table()
    ProjectTest.create_table()

    f = Faker(locale='zh_CN')
    data = []

    for i in range(5000):
        data.append({
            "location": f.address(),
            "url": f.image_url() + f.image_url(),
            "code": f.random_int(),
        })

    data.extend(data)
    data.extend(data)
    data.extend(data)
    data.extend(data)
    print(len(data))

    # ProjectTest.insert_many(data).execute()
    print("prepared!")
    p = Pipeline()

    class PrintProcess(Process):

        def process_item(self, model: Model):
            # print(model.get('location'))
            return model

    class InsertProcess(Process):
        def start_process(self):
            self.data = []
            pass

        def process_item(self, model: Model):
            self.data.append(model)
            return model

        def end_process(self):
            ProjectTest.insert_many(self.data).execute()

    p.add_process(PrintProcess())
    p.add_process(InsertProcess())

    p.process_all(data[:])


def finish(obj1, obj2):
    print(obj1)
    print(obj2)
    print("finish!")

def exception_callback(obj1:threadpool.WorkRequest, obj2):
    print(obj1.args[0])
    print(obj2)
    print("get !")

def add_threadpool(pool: threadpool.ThreadPool, target, args):
    pool.putRequest(threadpool.makeRequests(target, args, finish,exception_callback)[0])


import time
import threading


def threadpool_test():
    pool = threadpool.ThreadPool(3)

    def sel(seq):
        raise Exception("if raise")

        time.sleep(5)
        print(seq)
        return "sel_return"

    class testThread(threading.Thread):
        def run(self):
            raise Exception("if raise")

            time.sleep(5)
            print(self)
            return "sel_return"


    add_threadpool(pool, testThread, ("theseq"))
    add_threadpool(pool, testThread, ("theseq"))
    add_threadpool(pool, testThread, ("theseq"))
    add_threadpool(pool, testThread, ("theseq"))
    add_threadpool(pool, testThread, ("theseq"))
    pool.wait()
    print("end")


# init()
# inti_code_name()
# detect()

# insert_test()

threadpool_test()
