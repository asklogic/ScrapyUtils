from base.Model import Model, Field, ModelManager


class ProxyModel(Model):
    ip = Field(xpath=r'//*[@id="list"]/table/tbody/tr/td[1]')
    port = Field(xpath=r'//*[@id="list"]/table/tbody/tr/td[2]')

    # xpath_length = 15

    def feed_back(self):
        pass


class ViewstateModel(Model):
    name = "view"
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