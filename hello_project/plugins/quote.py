#!/usr/bin/env python3
"""
Quote plugin for Hello Project
"""
import random
from typing import Any, Dict

import requests

from .base import BasePlugin, PluginResult


class QuotePlugin(BasePlugin):
    """Plugin to get inspirational quotes"""

    name = "quote"
    description = "Get inspirational quotes"
    version = "1.0.0"

    # Built-in quotes for offline usage
    BUILTIN_QUOTES = [
        {
            "text": ("The way to get started is to quit talking and begin doing."),
            "author": "Walt Disney",
        },
        {
            "text": (
                "Life is what happens to you while you're " "busy making other plans."
            ),
            "author": "John Lennon",
        },
        {
            "text": (
                "The future belongs to those who believe "
                "in the beauty of their dreams."
            ),
            "author": "Eleanor Roosevelt",
        },
        {
            "text": (
                "It is during our darkest moments that we "
                "must focus to see the light."
            ),
            "author": "Aristotle",
        },
        {
            "text": (
                "Success is not final, failure is not fatal: "
                "it is the courage to continue that counts."
            ),
            "author": "Winston Churchill",
        },
        {
            "text": "プログラミングとは思考を整理する技術である。",
            "author": "Programming Wisdom",
        },
        {
            "text": "コードは詩のように美しく、散文のように明確であるべきだ。",
            "author": "Code Philosophy",
        },
    ]

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize quote plugin

        Args:
            config: Plugin configuration
        """
        super().__init__(config)
        self.use_api = self.config.get("use_api", False)
        self.category = self.config.get("category", "inspirational")
        self.language = self.config.get("language", "en")

    def execute(self, context: Dict[str, Any]) -> PluginResult:
        """Get a quote

        Args:
            context: Execution context

        Returns:
            Quote result
        """
        if self.use_api:
            return self._get_api_quote()
        else:
            return self._get_builtin_quote()

    def _get_builtin_quote(self) -> PluginResult:
        """Get a random built-in quote

        Returns:
            Quote result with built-in quote
        """
        quote = random.choice(self.BUILTIN_QUOTES)

        return PluginResult(
            success=True,
            data={
                "text": quote["text"],
                "author": quote["author"],
                "source": "built-in",
            },
            plugin_name=self.name,
        )

    def _get_api_quote(self) -> PluginResult:
        """Get quote from external API

        Returns:
            Quote result from API
        """
        try:
            # Using a free quote API
            response = requests.get(
                "https://api.quotable.io/random",
                params={"tags": self.category},
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()

            return PluginResult(
                success=True,
                data={
                    "text": data["content"],
                    "author": data["author"],
                    "source": "api",
                },
                plugin_name=self.name,
            )

        except Exception as e:
            self.logger.warning(
                f"API request failed, falling back to built-in quotes: {e}"
            )
            return self._get_builtin_quote()

    def validate_config(self) -> bool:
        """Validate plugin configuration

        Returns:
            True if configuration is valid
        """
        # Basic validation
        if self.category not in [
            "inspirational",
            "motivational",
            "wisdom",
            "success",
        ]:
            self.logger.warning(f"Unknown category: {self.category}, using default")

        return True

    def get_help(self) -> str:
        """Get help text for quote plugin

        Returns:
            Help text
        """
        return f"""Quote Plugin ({self.version})
Description: {self.description}

Usage: --plugin quote

Configuration:
  - use_api: Use external API for quotes (default: false)
  - category: Quote category (inspirational, motivational, wisdom, success)
  - language: Language preference (default: en)

Features:
  - Built-in quotes (no internet required)
  - External API integration (quotable.io)
  - Multiple categories
  - Fallback to built-in quotes if API fails

Example config.yaml:
  plugins:
    - name: quote
      config:
        use_api: true
        category: "motivational"
        language: "en" """
