from .show_template import show as show_t
from .show_component import show as show_c


def show(config):
    if config["type"] == "template":
        return show_t(name=config["name"], language=config["language"], category=config["category"])
    elif config["type"] == "component":
        return show_c(name=config["name"], language=config["language"], category=config["category"])
