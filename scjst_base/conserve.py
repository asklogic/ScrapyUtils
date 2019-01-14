from base.Conserve import Conserve, allow
from base.Model import Model
from .model import *
import json
from scjst_base.peewee_connect import ProjectBase

import scrapy_config

import threading

lock = threading.Lock()


class ProjectBaseConserve(Conserve):
    name = "save_project_base"

    def start_conserve(self):
        self.count = 0
        self.insert = 0
        self.urls = []
        for i in range(6):
            print("url get: ", i)
            self.urls.extend(list(map(lambda x: x.url, ProjectBase.select().where(
                (ProjectBase.UID > 10000 * i * 2) & (ProjectBase.UID < 10000 * i * 2 + 10000)).execute())))
        # self.urls = list(map(lambda x: x.url, ProjectBase.select().execute()))
        self.data = []

        pass

    def end_conserve(self):
        if self.data:
            ProjectBase.insert_many(self.data).execute()
        print(self.count)
        print(self.insert)

    @allow(ProjectBaseModel)
    def feed_function(self, model: ProjectBaseModel):
        self.count += 1

        lock.acquire()
        try:
            if not model.url in self.urls:
                self.data.append(model.pure_data())
                self.insert += 1

            if len(self.data) > 100:
                ProjectBase.insert_many(self.data).execute()

                self.data.clear()
        except Exception as e:
            print("shit!")
        finally:
            lock.release()


class ReProjectBaseConserve(Conserve):
    name = "re_save_project_base"

    def start_conserve(self):
        self.url = []
        self.data = []
        self.count = 0
        self.insert = 0
        pass

    def end_conserve(self):
        # with open(scrapy_config.Assets_Path + r"/3000-4000.json", "w") as f:
        #     json.dump(self.data, f)
        print(self.count)
        print(self.insert)

    @allow(ProjectBaseModel)
    def feed_function(self, model: ProjectBaseModel):
        self.count += 1
        if not model.url in self.url:
            self.url.append(model.url)
            self.data.append(model.pure_data())
            self.insert += 1


class QueryConserve(Conserve):
    name = "QueryConserve"

    def start_conserve(self):
        self.count = 0
        self.insert = 0
        self.ids = []


        # with open(scrapy_config.Assets_Path + r"/id0-5000.json") as f:
        #     self.ids.extend(json.load(f))

        pass

    def end_conserve(self):
        print(self.count)
        print(self.insert)

        # with open(scrapy_config.Assets_Path + r"/id0-10000.json", "w") as f:
        #     json.dump(self.ids, f)
        pass

    @allow(ProjectIDModel)
    def feed_function(self, model: ProjectIDModel):
        self.count += 1
        if not model.id in self.ids:
            self.ids.append(model.pure_data())
            self.insert += 1
