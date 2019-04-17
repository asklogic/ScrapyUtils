from base.components.model import Field, Model


class TestMockFailedModel(Model):
    _active = True
    
    filed = Field()


