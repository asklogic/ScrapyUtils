# -*- coding: utf-8 -*-
"""The module to test collect other components.

"""

from ScrapyUtils.components import Action, set_active, active
from ScrapyUtils.components.processor import Processor


@active
class TestProcessor(Processor):
    pass
