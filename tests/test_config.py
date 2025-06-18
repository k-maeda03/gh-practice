#!/usr/bin/env python3
"""
Tests for configuration management
"""
import tempfile
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from hello_project.config import ConfigManager, PluginConfig, Settings


class TestSettings:
    """Test cases for Settings model"""

    def test_default_settings(self):
        """Test default settings creation"""
        settings = Settings()

        assert settings.default_name == "GitHub CLI"
        assert settings.verbose is False
        assert settings.output_format == "text"
        assert settings.show_timestamp is False
        assert settings.plugins == []
        assert settings.api_timeout == 10

    def test_settings_with_plugins(self):
        """Test settings with plugin configuration"""
        plugin_config = PluginConfig(name="test", enabled=True, config={"key": "value"})
        settings = Settings(plugins=[plugin_config])

        assert len(settings.plugins) == 1
        assert settings.plugins[0].name == "test"
        assert settings.plugins[0].enabled is True
        assert settings.plugins[0].config == {"key": "value"}

    def test_settings_validation(self):
        """Test settings validation"""
        # Valid output format
        settings = Settings(output_format="json")
        assert settings.output_format == "json"

        # Invalid values should be caught by Pydantic
        with pytest.raises(ValidationError):
            Settings(api_timeout="invalid")


class TestPluginConfig:
    """Test cases for PluginConfig model"""

    def test_plugin_config_defaults(self):
        """Test plugin config with defaults"""
        config = PluginConfig(name="test")

        assert config.name == "test"
        assert config.enabled is True
        assert config.config == {}

    def test_plugin_config_with_data(self):
        """Test plugin config with custom data"""
        config = PluginConfig(
            name="weather",
            enabled=False,
            config={"api_key": "test123", "city": "Tokyo"},
        )

        assert config.name == "weather"
        assert config.enabled is False
        assert config.config["api_key"] == "test123"
        assert config.config["city"] == "Tokyo"


class TestConfigManager:
    """Test cases for ConfigManager"""

    def test_config_manager_initialization(self):
        """Test config manager initialization"""
        manager = ConfigManager()
        assert manager.config_path is None
        assert manager._settings is None

    def test_config_manager_with_path(self):
        """Test config manager with specific path"""
        test_path = "/test/config.yaml"
        manager = ConfigManager(test_path)
        assert str(manager.config_path) == test_path

    def test_load_default_config(self):
        """Test loading default configuration"""
        manager = ConfigManager()
        settings = manager.load_config()

        # Should return default settings when no config file exists
        assert isinstance(settings, Settings)
        assert settings.default_name == "GitHub CLI"

    def test_load_config_from_file(self):
        """Test loading configuration from YAML file"""
        config_data = {
            "default_name": "Test User",
            "verbose": True,
            "output_format": "json",
            "plugins": [
                {"name": "weather", "enabled": True, "config": {"api_key": "test123"}}
            ],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            manager = ConfigManager(temp_path)
            settings = manager.load_config()

            assert settings.default_name == "Test User"
            assert settings.verbose is True
            assert settings.output_format == "json"
            assert len(settings.plugins) == 1
            assert settings.plugins[0].name == "weather"
            assert settings.plugins[0].config["api_key"] == "test123"
        finally:
            Path(temp_path).unlink()

    def test_load_config_from_json(self):
        """Test loading configuration from JSON file"""
        config_data = {"default_name": "JSON User", "api_timeout": 20}

        import json

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            manager = ConfigManager(temp_path)
            settings = manager.load_config()

            assert settings.default_name == "JSON User"
            assert settings.api_timeout == 20
        finally:
            Path(temp_path).unlink()

    def test_environment_variable_override(self, monkeypatch):
        """Test environment variable configuration override"""
        # Set environment variables
        monkeypatch.setenv("HELLO_DEFAULT_NAME", "Env User")
        monkeypatch.setenv("HELLO_VERBOSE", "true")
        monkeypatch.setenv("HELLO_API_TIMEOUT", "30")

        manager = ConfigManager()
        settings = manager.load_config()

        assert settings.default_name == "Env User"
        assert settings.verbose is True
        assert settings.api_timeout == 30

    def test_save_config(self):
        """Test saving configuration to file"""
        settings = Settings(
            default_name="Save Test",
            verbose=True,
            plugins=[PluginConfig(name="test", enabled=False)],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"

            manager = ConfigManager()
            manager.save_config(settings, str(config_path))

            # Verify file was created and content is correct
            assert config_path.exists()

            with open(config_path, "r") as f:
                saved_data = yaml.safe_load(f)

            assert saved_data["default_name"] == "Save Test"
            assert saved_data["verbose"] is True
            assert len(saved_data["plugins"]) == 1
            assert saved_data["plugins"][0]["name"] == "test"

    def test_invalid_config_file(self):
        """Test handling of invalid configuration file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_path = f.name

        try:
            manager = ConfigManager(temp_path)
            with pytest.raises(ValueError):
                manager.load_config()
        finally:
            Path(temp_path).unlink()

    def test_unsupported_config_format(self):
        """Test handling of unsupported configuration file format"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("some content")
            temp_path = f.name

        try:
            manager = ConfigManager(temp_path)
            with pytest.raises(ValueError, match="Unsupported config file format"):
                manager.load_config()
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__])
