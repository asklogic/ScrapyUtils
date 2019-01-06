from base.lib import Model


class testModel(Model):
    age = 22


class ipModel(Model):
    ip: str


class proxyModel(Model):
    ip: str
    port: str
    type: str
    anonymous: str


class ViewstateModel(Model):
    viewstate: str
    generator: str
    validation: str


class ProjectModel(Model):
    title: str
    location: str
    url: str


if __name__ == '__main__':
    print(ipModel().__class__.__name__)
