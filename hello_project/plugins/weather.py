#!/usr/bin/env python3
"""
Weather plugin for Hello Project
"""
import requests
from typing import Dict, Any
from .base import BasePlugin, PluginResult


class WeatherPlugin(BasePlugin):
    """Plugin to get weather information"""

    name = "weather"
    description = "Get current weather information"
    version = "1.0.0"

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize weather plugin

        Args:
            config: Plugin configuration with API key and default city
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.default_city = self.config.get("default_city", "Tokyo")
        self.use_mock = self.config.get("use_mock", True)  # For demo purposes

    def execute(self, context: Dict[str, Any]) -> PluginResult:
        """Get weather information

        Args:
            context: Execution context

        Returns:
            Weather information result
        """
        city = context.get("city", self.default_city)

        if self.use_mock:
            return self._get_mock_weather(city)

        if not self.api_key:
            return PluginResult(
                success=False,
                error="Weather API key not configured. Set 'api_key' in plugin config.",
                plugin_name=self.name,
            )

        try:
            weather_data = self._get_real_weather(city)
            return PluginResult(success=True, data=weather_data, plugin_name=self.name)
        except Exception as e:
            return PluginResult(
                success=False,
                error=f"Failed to get weather data: {e}",
                plugin_name=self.name,
            )

    def _get_mock_weather(self, city: str) -> PluginResult:
        """Get mock weather data for demo

        Args:
            city: City name

        Returns:
            Mock weather result
        """
        mock_data = {
            "city": city,
            "temperature": "22°C",
            "description": "Partly cloudy",
            "humidity": "65%",
            "wind": "5 km/h",
            "note": "This is mock data for demonstration purposes",
        }

        return PluginResult(success=True, data=mock_data, plugin_name=self.name)

    def _get_real_weather(self, city: str) -> Dict[str, Any]:
        """Get real weather data from API

        Args:
            city: City name

        Returns:
            Weather data dictionary
        """
        # Example using OpenWeatherMap API
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self.api_key, "units": "metric"}

        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "city": data["name"],
            "temperature": f"{data['main']['temp']:.1f}°C",
            "description": data["weather"][0]["description"].title(),
            "humidity": f"{data['main']['humidity']}%",
            "wind": f"{data['wind']['speed']} m/s",
        }

    def validate_config(self) -> bool:
        """Validate plugin configuration

        Returns:
            True if configuration is valid
        """
        # For mock mode, no validation needed
        if self.use_mock:
            return True

        # For real API, require API key
        return bool(self.api_key)

    def get_help(self) -> str:
        """Get help text for weather plugin

        Returns:
            Help text
        """
        return f"""Weather Plugin ({self.version})
Description: {self.description}

Usage: --plugin weather

Configuration:
  - api_key: OpenWeatherMap API key (required for real data)
  - default_city: Default city name (default: Tokyo)
  - use_mock: Use mock data for demo (default: true)

Context parameters:
  - city: City name to get weather for

Example config.yaml:
  plugins:
    - name: weather
      config:
        api_key: "your_api_key_here"
        default_city: "New York"
        use_mock: false"""
