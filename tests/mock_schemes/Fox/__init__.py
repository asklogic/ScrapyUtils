from base.core.collect import collect_steps, collect_processors, collect_profile

from . import action, parse, processor, profile

steps_class = collect_steps(action, parse)
processors_class = collect_processors(processor)
config, tasks_callable, scraper_callable = collect_profile(profile)
