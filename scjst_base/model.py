from base.lib import Model


class Scjst_baseModel(Model):
    title: str
    location: str
    url: str


class ViewStateModel(Model):
    viewstate: str
    generator: str
    validation: str

