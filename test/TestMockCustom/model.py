from base.components.model import Field, Model


class TestMockCustomModel(Model):
    _active = True
    
    filed = Field()



class OtherTestModel(Model):

    name = Field()