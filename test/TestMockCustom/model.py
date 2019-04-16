from base.Model import Model, Field


class TestMockCustomModel(Model):
    _active = True
    
    filed = Field()



class OtherTestModel(Model):

    name = Field()