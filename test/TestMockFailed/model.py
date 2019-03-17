from base.Model import Model, Field


class TestMockFailedModel(Model):
    _active = True
    
    filed = Field()


