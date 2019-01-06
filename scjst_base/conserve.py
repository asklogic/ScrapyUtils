from base.lib import Conserve, allow, Model
from scjst_base.model import *


class AgentConserve(Conserve):
    @allow(Scjst_baseModel)
    def feed_func(self, model: Scjst_baseModel):
        print(model.url)
        print(model.title)
