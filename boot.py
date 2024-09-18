import sublime

from .plugin.constants import PLUGIN_NAME


def reload_plugin() -> None:
    import sys

    # remove all previously loaded plugin modules
    prefix = f"{__package__}."
    for module_name in tuple(filter(lambda m: m.startswith(prefix) and m != __name__, sys.modules)):
        del sys.modules[module_name]


if sublime.platform() == "windows":
    reload_plugin()

    from .plugin import *  # noqa: F401, F403
else:
    print(f"[{PLUGIN_NAME}][INFO] This plugin is only supported on Windows.")
