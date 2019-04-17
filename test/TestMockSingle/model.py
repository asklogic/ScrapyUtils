from base.Model import Field
from base.components.model import Model


class TestMockSingleModel(Model):
    _active = True
    
    filed = Field()


