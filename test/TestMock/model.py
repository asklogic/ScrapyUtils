from base.components.model import Field, Model


class TestMockModel(Model):
    _active = True
    
    filed = Field()


