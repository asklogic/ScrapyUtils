from base.Model import Model,Field

class Detail(Model):
    price = Field()
    area = Field()
    room = Field()
    floor = Field()

    rent_additionally = Field()
    deposit = Field()
    construction_type = Field()
    building_material = Field()
    window = Field()
    heating = Field()
    finishing_state = Field()
    available_from = Field()

    equipment = Field()
    security = Field()
    media = Field()
    additional_information = Field()
    description = Field()
