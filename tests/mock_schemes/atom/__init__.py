from base.core.collect import collect_steps, collect_processors, collect_settings

from . import action, parse, processor, settings

steps_class = collect_steps(action, parse)
processors_class = collect_processors(processor)
config, tasks_callable, scraper_callable = collect_settings(settings)
