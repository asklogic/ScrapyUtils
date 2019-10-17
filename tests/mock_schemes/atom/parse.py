from base.components.step import ParseStep
from base.components import active

from base.tool import xpathParse

from .model import Person


@active
class MockPersonParse(ParseStep):

    def parsing(self):
        names = xpathParse(self.content, r'//*[@class="person"]')

        for name in names:
            m = Person()
            m.name = name
            yield m


@active
class CountParse(ParseStep):
    count = 0

    priority = 200

    def parsing(self):
        self.count += 1
