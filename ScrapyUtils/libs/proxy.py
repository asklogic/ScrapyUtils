from .model import Model, Field


class Proxy(Model):
    ip = Field(convert=str)
    port = Field(convert=str)


