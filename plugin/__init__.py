# import all listeners and commands
from .listener import FollowLnkViewEventListener

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: listeners
    "FollowLnkViewEventListener",
)


def plugin_loaded() -> None:
    """Executed when this plugin is loaded."""


def plugin_unloaded() -> None:
    """Executed when this plugin is unloaded."""
