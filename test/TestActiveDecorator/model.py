from base.components import Field, Model, active


@active
class TestactivedecoratorModel(Model):
    filed = Field()
