from base.Model import Model, Field, ModelManager


class ViewstateModel(Model):
    viewstate = Field(xpath=r'//*[@id="__VIEWSTATE"]//@value')
    generator = Field(xpath=r'//*[@id="__VIEWSTATEGENERATOR"]//@value')
    validation = Field(xpath=r'//*[@id="__EVENTVALIDATION"]//@value')


class ProjectBaseModel(Model):
    # title = Field(xpath=r'//*[@class="page-content"]/table/tr/td[3]/a')
    # location = Field(xpath=r'//*[@class="page-content"]/table/tr/td[2]')
    # url = Field(xpath=r'//*[@class="page-content"]/table/tr/td[3]/a/@href')
    # code = Field(xpath=r'//*[@class="page-content"]/table/tr/td[4]')
    # date = Field(xpath=r'//*[@class="page-content"]/table/tr/td[5]')

    title = Field()
    location = Field()
    url = Field()
    code = Field()
    date = Field()
    # page = Field()

class ProjectIDModel(Model):
    id = Field()