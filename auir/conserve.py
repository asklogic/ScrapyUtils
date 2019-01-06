import json
from base.lib import Model, Conserve, allow
from auir.model import ipModel, testModel, proxyModel, ProjectModel


class IPConserve(Conserve):

    @allow(ipModel)
    def _feed(self, model: Model):
        model: ipModel
        print(model.ip)

    @allow(ipModel)
    def feed_IP(self, model: Model):
        model: ipModel
        print("this is ip model")
        print(model.ip)

    @allow(testModel)
    def feed_test(self, model: Model):
        model: testModel
        print("this is test model")
        print(model.age)

    @allow(ProjectModel)
    def feed_project(self, model: Model):
        model: ProjectModel
        print("this is a project info")
        print(model.url)
        print(model.title)


class printConserve(Conserve):

    def start(self):
        self.projectList = []
        pass

    def finish(self):
        import json

        with open('E:\\cloudWF\\python\\ScrapyUtils\\auir\\data\\base_projects.json', "w") as f:
            json.dump(self.projectList, f)

    @allow(proxyModel)
    def feed_proxy(self, model):
        model: proxyModel
        print("proxy - ip: {0} port {1}".format(model.ip, model.port))

    @allow(ProjectModel)
    def feed_project(self, model: Model):
        model: ProjectModel
        print("this is a project info")
        print(model.url)
        print(model.title)
        print(model.location)

        self.projectList.append({
            "url": model.url,
            "title": model.title,
            "location": model.location,
        })


if __name__ == '__main__':
    m1 = ipModel()
    m1.ip = "wtf ip!"

    m2 = testModel()
    m2.age = "wtf test age"

    conserve = IPConserve()
    conserve.model(m1)
    conserve.model(m2)
