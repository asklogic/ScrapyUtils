from ScrapyUtils.core.preload import collect_action, collect_processors, initial_configure

from . import action, processor, settings

steps_class = collect_action(action)
processors_class = collect_processors(processor)
initial_configure(settings)
