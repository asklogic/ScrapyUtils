import json
import scrapy_config
from base.components.model import Model
# from scjst_base.peewee_connect import ProjectBase
from base.hub.pipeline import Pipeline
from base.components.proceesor import Processor
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

    class PrintProcessor(Processor):

        def process_item(self, model: Model):
            # print(model.get('location'))
            return model

    class InsertProcessor(Processor):
        def start_process(self):
            self.data = []
            pass

        def process_item(self, model: Model):
            self.data.append(model)
            return model

        def end_process(self):
            ProjectTest.insert_many(self.data).execute()

    p.add_process(PrintProcessor())
    p.add_process(InsertProcessor())

    p.process_all(data[:])


def finish(obj1, obj2):
    print(obj1)
    print(obj2)
    print("finish!")


def exception_callback(obj1: threadpool.WorkRequest, obj2):
    print(obj1.args[0])
    print(obj2)
    print("get !")


def add_threadpool(pool: threadpool.ThreadPool, target, args):
    """
    压入单个req
    :param pool:
    :param target:
    :param args:
    :return:
    """
    pool.putRequest(threadpool.makeRequests(target, [(args, None)], finish, exception_callback)[0])


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

        def args_test(self, data: [] = (), msg: str = "mock"):
            print(data)
            print(msg)

    tt = testThread()
    # add_threadpool(pool, tt.args_test, [(([1, 3, 4], "theseq"), None)])
    add_threadpool(pool, tt.args_test, ([1, 3, 4], "theseq"))
    add_threadpool(pool, tt.args_test, ([1, 3, 4], "theseq"))
    add_threadpool(pool, tt.args_test, ([1, 3, 4], "theseq"))

    pool.wait()
    print("end")


# init()
# inti_code_name()
# detect()

# insert_test()

# threadpool_test()

from multiprocessing import dummy


def multiprocess_test():
    def sel(seq, **kwargs):
        # raise Exception("if raise")

        time.sleep(1)
        print(seq)
        # print(args)
        print(kwargs)
        return "sel_return"

    def callback(obj1):
        print(type(obj1))
        print(obj1)
        pass

    # pool: multiprocessing.Pool = multiprocessing.Pool(processes=1)
    pool: dummy.Pool = dummy.Pool(processes=1)

    pool.apply_async(sel, args=("test",), kwds={"some": [1, 2, 3]}, callback=callback, error_callback=callback)
    pool.apply_async(sel, args=("test",), kwds={"some": [1, 2, 3]}, callback=callback, error_callback=callback)
    pool.apply_async(sel, args=("test",), kwds={"some": [1, 2, 3]}, callback=callback, error_callback=callback)
    pool.apply_async(sel, args=("test",), kwds={"some": [1, 2, 3]}, callback=callback, error_callback=callback)
    pool.apply_async(sel, args=("test",), kwds={"some": [1, 2, 3]}, callback=callback, error_callback=callback)

    pool.close()
    pool.join()
    # pool.join()

    pass


# multiprocess_test()

import concurrent.futures


def concurrent_test():
    def sel(seq, **kwargs):

        time.sleep(1)
        raise Exception("if raise")

        print(seq)
        # print(args)
        # print(kwargs)
        return "sel_return"

    def callback(future: concurrent.futures.Future):
        try:
            print(future.result())
        except Exception as e:
            pass
        future.result()

    print("conccurrent!")
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    t1 = pool.submit(sel, ("ToT"))
    t1 = pool.submit(sel, ("ToT"))
    t1 = pool.submit(sel, ("ToT"))
    # t1 = pool.submit(sel, ("ToT")).add_done_callback(callback)
    # t1 = pool.submit(sel, ("ToT")).add_done_callback(callback)
    # t1 = pool.submit(sel, ("ToT")).add_done_callback(callback)

    pool.shutdown(wait=True)
    # concurrent.futures.wait()


concurrent_test()

# head = {
#     "0": ["ZSLXNAME", "ZCZY"],
#     "1": "ZCZY",
#     "5": "ZSLXNAME",
#     "9": ['ZW', "ZCZY"],
# }
# label = {
#     "0": {
#         "证书级别": "ZSJSNAME",
#         "证书号": "ZCZSH",
#         "发证时间": "FZSJ",
#         "有效期": ["ZSYXQ", "ZSYXQ"],
#     },
#     "1": {
#         "等级": "ZSJSNAME",
#         "证书编号": "ZCZSH",
#         "注册证书号": "ZGZSH",
#         "执业印章号": "YZH",
#         "证书有效期": ["ZSYXQ", "ZSYXQ"],
#         "所在单位": ["QYMC", "QYBM"],
#     },
#     "2": {
#         "证书号": "ZCZSH",
#         "执业印章号": "YZH",
#         "资格印章号": "ZGZSH",
#         "注册证书号": "ZCZSBH",
#         "发证时间": "FZSJ",
#         "证书有效期": ["ZSYXQ", "ZSYXQ"],
#         "所在单位": ["QYMC", "QYBM"],
#
#     },
#     "3": {
#         "职务": "ZSJSNAME",
#         "证书号": "ZCZSH",
#         "发证时间": "FZSJ",
#         "证书有效期": ["ZSYXQ", "ZSYXQ"],
#         "所在单位": ["QYMC", "QYBM"],
#
#     },
#     "4": {
#         "证书级别": "ZSJSNAME",
#         "证书号": "ZCZSH",
#         "职称": "JSZC",
#         "发证时间": "FZSJ",
#         "证书有效期": ["ZSYXQ", "ZSYXQ"],
#         "所在单位": ["QYMC", "QYBM"],
#     },
#     "5": {
#         "专业": "Level",
#         "岗位": "ZCZY",
#         "证书号": "ZCZSH",
#         "证书有效期": ["ZSYXQ", "ZSYXQ"],
#         "发证时间": "FZSJ",
#     },
#     "6": {
#         "证书级别": "ZSJSNAME",
#         "证书号": "ZCZSH",
#         "注册专业": "ZCZY",
#         "执业印章号": "YZH",
#         "证书有效期": ["ZSYXQ", "ZSYXQ"],
#
#     },
#     "6.1": {
#         "证书级别": "ZSJSNAME",
#         "证书号": "ZCZSH",
#         "所在单位": ["QYMC", "QYBM"],
#     },
#     "7": {
#         "等级": "Level",
#         "注册证书号": "ZCZSH",
#         "证书编号": "ZCZSBH",
#         "初始注册": "FZSJ",
#         "证书有效期": ["ZSYXQ", "ZSYXQ"],
#         "所在单位": ["QYMC", "QYBM"],
#     },
#     "8": {
#         "证书级别": "ZSJSNAME",
#         "证书号": "ZCZSH",
#         "发证时间": "FZSJ",
#         "有效期": ["ZSYXQ", "ZSYXQ"],
#     },
# }

# head = {
#     "head": "ZSLXMC",
#     "subCount": "LXGS",
#     "得分": "Score",
#
# }
#
# sub = {
#     "0": {
#         "证书号": "ZSBH",
#         "有效期": ["YXJSRQ", "YXJSRQ"],
#         "发证机关": "BFBM",
#     },
#
#     "1": {
#         "证书号": "ZSBH",
#         "有效期": ["YXJSRQ", "YXJSRQ"],
#         "发证机关": "BFBM",
#         "企业名称": "QYMC",
#     },
#     "2": {
#         "证书号": "ZSBH",
#         "登记类别": "ZSDJMC",
#         "有效期": ["YXJSRQ", "YXJSRQ"],
#         "发证机关": "BFBM",
#         "企业名称": "QYMC",
#     },
#     "3": {
#         "证书号": "ZSBH",
#         "有效期": ["YXJSRQ", "YXJSRQ"],
#         "发证机关": "BFBM",
#     },
#     "3.1": {
#         "证书号": "ZSBH",
#         "有效期": ["YXJSRQ", "YXJSRQ"],
#         "发证机关": "BFBM",
#         "资质项": "ZZX",
#         "企业名称": "QYMC",
#     },
#     "4": {
#         "等级编号": "ZSBH",
#         "登记日期": "BFRQ",
#         "企业名称": "QYMC",
#     },
# }
#
# with open(r'C:\Users\logic\Desktop\EnterMapper.json', "w") as f:
#     json.dump({'head': head, "sub": sub}, f)
