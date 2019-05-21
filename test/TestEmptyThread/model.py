from base.components import Field, Model, active


@active
class TestemptythreadModel(Model):
    filed = Field()


@active
class OtherModel(Model):
    name = Field()
