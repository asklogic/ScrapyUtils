# -*- coding: utf-8 -*-
"""The module to test collect other components.

"""

from ScrapyUtils.components import Action, set_active, active, Processor


@active
class TestProcessor(Processor):
    pass
