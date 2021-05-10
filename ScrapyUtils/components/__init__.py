from logging import getLogger, Logger

component_log: Logger = getLogger('component_log')

# submodules

from .component import Component, ComponentSuit, active, set_active
from .pipeline import Pipeline, ProcessorSuit
from .proceesor import Processor
from .step import Step, Action, Parse, StepSuit
