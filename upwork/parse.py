from typing import Generator

from base.Model import ModelManager, Model
from base.Parse import Parse
from .model import *

from base.tool import xpathParse, xpathParseList


class DetailParse(Parse):
    def parsing(cls, content: str, manager: ModelManager) -> Model or Generator[Model]:
        price = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[1]/li[1]/span/strong')[0]
        area = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[1]/li[2]/span/strong')[0]
        room = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[1]/li[3]/span/strong')[0]
        floor = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[1]/li[4]/span/text()')[0]

        rent_additionally = \
            xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[1]/text()')[0]
        deposit = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[2]/text()')[0]
        construction_type = \
            xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[3]/text()')[0]
        building_material = \
            xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[4]/text()')[0]
        window = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[5]/text()')[0]
        heating = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[6]/text()')[0]
        finishing_state = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[7]/text()')[
            0]
        available_from = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[1]/ul[2]/li[8]/text()')[0]

        equipment = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[2]/ul/li')
        security = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[3]/ul/li')
        media = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[4]/ul/li')
        additional_information = xpathParse(content, r'/html/body/div[1]/section[6]/div/div/div/ul/li[5]/ul/li')

        equipmentData = ""
        for i in equipment:
            equipmentData = equipmentData + i + "|"

        securityData = ""
        for i in security:
            securityData = securityData + i + "|"

        mediaData = ""
        for i in media:
            mediaData = mediaData + i + "|"

        additional_information_Data = ""
        for i in additional_information:
            additional_information_Data = additional_information_Data + i + "|"

        description = xpathParse(content, r'/html/body/div[1]/section[7]/div/div/div/div/div/div[1]/p/text()')

        descriptionData = ""
        for i in description:
            descriptionData = descriptionData + str(i) + "|"

        m: Detail = manager.model("Detail")
        m.price = price
        m.area = area
        m.room = room
        m.floor = floor

        m.rent_additionally = rent_additionally
        m.deposit = deposit
        m.construction_type = construction_type
        m.building_material = building_material
        m.window = window
        m.heating = heating
        m.finishing_state = finishing_state
        m.available_from = available_from

        m.equipment = equipmentData
        m.security = securityData
        m.media = mediaData
        m.additional_information = additional_information_Data

        m.description = descriptionData

        yield m
