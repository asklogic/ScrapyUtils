from base.Model import Model, Field


class TestMockThreadModel(Model):
    _active = True

    ip = Field(xpath='//*[@id="list"]/table/tbody/tr[1]/td[1]')
    port = Field(xpath='//*[@id="list"]/table/tbody/tr[1]/td[2]')
