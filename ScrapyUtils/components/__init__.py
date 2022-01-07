from logging import getLogger, Logger

component_log: Logger = getLogger('component_log')

# submodules

from .component import Component, ComponentSuit, active, set_active
from .processor import Processor, ProcessorSuit
from .action import Action, ActionSuit
