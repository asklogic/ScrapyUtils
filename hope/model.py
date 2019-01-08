from base.Model import Model, Field, ModelManager


class ProxyInfoModel(Model):
    ip = Field(xpath=r'//*[@id="list"]/table/tbody/tr/td[1]')
    port = Field(xpath=r'//*[@id="list"]/table/tbody/tr/td[2]')
    scheme = Field(xpath=r'//*[@id="list"]/table/tbody/tr/td[4]')

    # xpath_length = 15




class ViewstateModel(Model):
    viewstate = Field(xpath=r'//*[@id="__VIEWSTATE"]//@value')
    generator = Field(xpath=r'//*[@id="__VIEWSTATEGENERATOR"]//@value')
    validation = Field(xpath=r'//*[@id="__EVENTVALIDATION"]//@value')


class ProjectModel(Model):
    title = Field()
    location = Field()
    url = Field()
    code = Field()


class CountModel(Model):
    count = Field()


class ProjectInfoModel(Model):
    id = Field()