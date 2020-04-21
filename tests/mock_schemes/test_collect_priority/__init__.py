from base.core.collect import collect_steps, collect_processors

# from . import action, parse

# steps = collect_steps(action, parse)


from . import processor

processors_class = collect_processors(processor)
