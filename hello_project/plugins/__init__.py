"""Plugin system for Hello Project"""

from .base import BasePlugin, PluginManager, PluginResult
from .quote import QuotePlugin
from .weather import WeatherPlugin

__all__ = [
    "BasePlugin",
    "PluginManager",
    "PluginResult",
    "WeatherPlugin",
    "QuotePlugin",
]
