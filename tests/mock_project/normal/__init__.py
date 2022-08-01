from ScrapyUtils.core.preload import collect_action, collect_processors, initial_configure

from . import web_action, parse_action, process, settings

collect_action(web_action, parse_action)
collect_processors(process)
initial_configure(settings)