#!/usr/bin/env python3
"""
Configuration management using Pydantic
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError


class PluginConfig(BaseModel):
    """Configuration for individual plugins"""

    name: str
    enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)


class Settings(BaseModel):
    """Main application settings"""

    # Basic settings
    default_name: str = Field(default="GitHub CLI", description="Default greeting name")
    verbose: bool = Field(default=False, description="Enable verbose logging")

    # Output settings
    output_format: str = Field(default="text", description="Output format (text, json)")
    show_timestamp: bool = Field(default=False, description="Show timestamp in output")

    # Plugin settings
    plugins: List[PluginConfig] = Field(
        default_factory=list, description="Plugin configurations"
    )
    plugin_directory: str = Field(
        default="plugins", description="Plugin directory path"
    )

    # API settings (for plugins)
    api_timeout: int = Field(default=10, description="API request timeout in seconds")

    class Config:
        """Pydantic configuration"""

        extra = "forbid"  # Forbid extra fields
        validate_assignment = True


class ConfigManager:
    """Manages application configuration with multiple sources"""

    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".config" / "hello_project" / "config.yaml",
        Path.cwd() / "config.yaml",
        Path.cwd() / "hello_config.yaml",
    ]

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager

        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = Path(config_path) if config_path else None
        self._settings: Optional[Settings] = None

    def load_config(self) -> Settings:
        """Load configuration from various sources

        Returns:
            Settings: Loaded configuration

        Raises:
            ValidationError: If configuration validation fails
        """
        config_data = {}

        # Load from file
        if config_file := self._find_config_file():
            config_data.update(self._load_config_file(config_file))

        # Override with environment variables
        config_data.update(self._load_from_env())

        try:
            self._settings = Settings(**config_data)
            return self._settings
        except ValidationError as e:
            raise ValidationError(f"Configuration validation failed: {e}")

    def _find_config_file(self) -> Optional[Path]:
        """Find configuration file

        Returns:
            Path to configuration file or None if not found
        """
        # Use explicitly provided path
        if self.config_path and self.config_path.exists():
            return self.config_path

        # Search default paths
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                return path

        return None

    def _load_config_file(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from file

        Args:
            config_path: Path to configuration file

        Returns:
            Configuration dictionary

        Raises:
            ValueError: If file format is not supported
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                if config_path.suffix.lower() in [".yaml", ".yml"]:
                    return yaml.safe_load(f) or {}
                elif config_path.suffix.lower() == ".json":
                    return json.load(f) or {}
                else:
                    raise ValueError(
                        f"Unsupported config file format: {config_path.suffix}"
                    )
        except Exception as e:
            raise ValueError(f"Failed to load config file {config_path}: {e}")

    def _load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables

        Returns:
            Configuration dictionary from environment variables
        """
        env_config = {}

        # Map environment variables to config fields
        env_mappings = {
            "HELLO_DEFAULT_NAME": "default_name",
            "HELLO_VERBOSE": "verbose",
            "HELLO_OUTPUT_FORMAT": "output_format",
            "HELLO_SHOW_TIMESTAMP": "show_timestamp",
            "HELLO_API_TIMEOUT": "api_timeout",
        }

        for env_var, config_key in env_mappings.items():
            if env_value := os.getenv(env_var):
                # Convert string values to appropriate types
                if config_key in ["verbose", "show_timestamp"]:
                    env_config[config_key] = env_value.lower() in [
                        "true",
                        "1",
                        "yes",
                    ]
                elif config_key == "api_timeout":
                    env_config[config_key] = int(env_value)
                else:
                    env_config[config_key] = env_value

        return env_config

    def save_config(
        self,
        settings: Settings,
        config_path: Optional[str] = None,
    ) -> None:
        """Save configuration to file

        Args:
            settings: Settings to save
            config_path: Optional path to save configuration
        """
        save_path = Path(config_path) if config_path else self._get_default_save_path()

        # Ensure directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dictionary and save as YAML
        config_dict = settings.model_dump()
        with open(save_path, "w", encoding="utf-8") as f:
            yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)

    def _get_default_save_path(self) -> Path:
        """Get default save path for configuration

        Returns:
            Default configuration save path
        """
        config_dir = Path.home() / ".config" / "hello_project"
        return config_dir / "config.yaml"

    @property
    def settings(self) -> Settings:
        """Get current settings, loading if necessary

        Returns:
            Current settings
        """
        if self._settings is None:
            self._settings = self.load_config()
        return self._settings
