# -*- coding: utf-8 -*-
"""The module to test collect other components.

"""

from ScrapyUtils.components import Action, set_active, active
from ScrapyUtils.components.process import Process


@active
class TestProcessor(Process):
    pass
