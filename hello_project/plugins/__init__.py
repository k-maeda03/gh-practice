"""Plugin system for Hello Project"""

from .base import BasePlugin, PluginManager, PluginResult
from .weather import WeatherPlugin
from .quote import QuotePlugin

__all__ = ["BasePlugin", "PluginManager", "PluginResult", "WeatherPlugin", "QuotePlugin"]