from .model import Model, Field


class ProxyModel(Model):
    ip = Field(convert=str)
    port = Field(convert=str)


class Proxy(object):
    ip: str
    port: str

    def __new__(cls, *args, **kwargs):
        return ProxyModel()
