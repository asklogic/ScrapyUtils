from base.Model import Model, Field


class TestMockSingleModel(Model):
    _active = True

    _mapper = {
        'ip': '//*[@id="list"]/table/tbody/tr/td[1]',
    }

    ip = Field(xpath='//*[@id="list"]/table/tbody/tr/td[1]')
    port = Field(xpath='//*[@id="list"]/table/tbody/tr/td[2]')
