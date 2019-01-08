from base.Conserve import Conserve, allow
from base.Model import Model
from .model import *
import json

# temp
import threading
lock = threading.Lock()


class HopeConserve(Conserve):
    name = "hope"

    def start_conserve(self):
        self.data = []
        pass

    def end_conserve(self):
        print(len(self.data))
        # with open(r"D:\cloudWF\Python\ScrapyUtils\assets\data\data.json", "w") as f:
        #     json.dump(self.data, f)

    @allow(ProjectModel)
    def feed_print(self, model: ProjectModel):
        self.data.append(model.pure_data())

        if len(self.data) % 20 == 0:
            print(model.title)


class QueryConserve(Conserve):
    name = "nope"



    def start_conserve(self):
        self.count = 0
        self.dataList = []

    def end_conserve(self):
        pass



    @allow(ProjectInfoModel)
    def feed_project(self,model: ProjectInfoModel):
        lock.acquire()
        if model.id in self.dataList:
            pass
        else:
            self.dataList.append(model.id)
        print(len(self.dataList))
        lock.release()
