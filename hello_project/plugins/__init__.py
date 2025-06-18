"""Plugin system for Hello Project"""

from .base import BasePlugin, PluginManager
from .weather import WeatherPlugin
from .quote import QuotePlugin

__all__ = ["BasePlugin", "PluginManager", "WeatherPlugin", "QuotePlugin"]