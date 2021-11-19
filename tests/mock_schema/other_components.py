# -*- coding: utf-8 -*-
"""The module to test collect other components.

"""

from ScrapyUtils.components import Action, Parse, set_active, active, Processor


@active
class FirstParse(Parse):
    pass


@active
class SecondParse(Parse):
    pass


class ThirdParse(Parse):
    pass


@active
class TestProcessor(Processor):
    pass
