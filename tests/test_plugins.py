#!/usr/bin/env python3
"""
Tests for plugin system
"""
import pytest
from unittest.mock import Mock, patch
from hello_project.plugins import BasePlugin, PluginManager, PluginResult
from hello_project.plugins.weather import WeatherPlugin
from hello_project.plugins.quote import QuotePlugin


class MockPlugin(BasePlugin):
    """Mock plugin for testing"""
    
    name = "mock"
    description = "Mock plugin for testing"
    version = "1.0.0"
    
    def __init__(self, config=None, should_fail=False):
        super().__init__(config)
        self.should_fail = should_fail
    
    def execute(self, context):
        if self.should_fail:
            raise Exception("Mock plugin failure")
        
        return PluginResult(
            success=True,
            data={"message": "Mock plugin executed", "context": context},
            plugin_name=self.name
        )


class TestPluginResult:
    """Test cases for PluginResult"""

    def test_plugin_result_success(self):
        """Test successful plugin result"""
        result = PluginResult(
            success=True,
            data={"test": "value"},
            plugin_name="test"
        )
        
        assert result.success is True
        assert result.data == {"test": "value"}
        assert result.error is None
        assert result.plugin_name == "test"

    def test_plugin_result_failure(self):
        """Test failed plugin result"""
        result = PluginResult(
            success=False,
            error="Test error",
            plugin_name="test"
        )
        
        assert result.success is False
        assert result.data is None
        assert result.error == "Test error"
        assert result.plugin_name == "test"


class TestBasePlugin:
    """Test cases for BasePlugin"""

    def test_mock_plugin_execution(self):
        """Test mock plugin execution"""
        plugin = MockPlugin()
        context = {"test": "context"}
        
        result = plugin.execute(context)
        
        assert result.success is True
        assert result.data["message"] == "Mock plugin executed"
        assert result.data["context"] == context

    def test_mock_plugin_failure(self):
        """Test mock plugin failure handling"""
        plugin = MockPlugin(should_fail=True)
        context = {}
        
        with pytest.raises(Exception, match="Mock plugin failure"):
            plugin.execute(context)

    def test_plugin_validation(self):
        """Test plugin configuration validation"""
        plugin = MockPlugin()
        assert plugin.validate_config() is True

    def test_plugin_help(self):
        """Test plugin help text"""
        plugin = MockPlugin()
        help_text = plugin.get_help()
        
        assert "mock" in help_text
        assert "Mock plugin for testing" in help_text


class TestPluginManager:
    """Test cases for PluginManager"""

    def test_plugin_manager_initialization(self):
        """Test plugin manager initialization"""
        manager = PluginManager()
        
        # Should have built-in plugins loaded
        assert len(manager.plugins) >= 2
        assert "weather" in manager.plugins
        assert "quote" in manager.plugins

    def test_register_plugin(self):
        """Test plugin registration"""
        manager = PluginManager()
        mock_plugin = MockPlugin()
        
        initial_count = len(manager.plugins)
        manager.register_plugin(mock_plugin)
        
        assert len(manager.plugins) == initial_count + 1
        assert "mock" in manager.plugins
        assert manager.get_plugin("mock") is mock_plugin

    def test_register_invalid_plugin(self):
        """Test registration of invalid plugin"""
        manager = PluginManager()
        
        with pytest.raises(ValueError, match="Plugin must inherit from BasePlugin"):
            manager.register_plugin("not a plugin")

    def test_get_plugin(self):
        """Test getting plugin by name"""
        manager = PluginManager()
        
        weather_plugin = manager.get_plugin("weather")
        assert weather_plugin is not None
        assert isinstance(weather_plugin, WeatherPlugin)
        
        non_existent = manager.get_plugin("non_existent")
        assert non_existent is None

    def test_list_plugins(self):
        """Test listing available plugins"""
        manager = PluginManager()
        plugins = manager.list_plugins()
        
        assert isinstance(plugins, list)
        assert "weather" in plugins
        assert "quote" in plugins

    def test_execute_plugin_success(self):
        """Test successful plugin execution"""
        manager = PluginManager()
        mock_plugin = MockPlugin()
        manager.register_plugin(mock_plugin)
        
        context = {"test": "data"}
        result = manager.execute_plugin("mock", context)
        
        assert result.success is True
        assert result.plugin_name == "mock"
        assert result.data["context"] == context

    def test_execute_plugin_failure(self):
        """Test plugin execution failure"""
        manager = PluginManager()
        mock_plugin = MockPlugin(should_fail=True)
        manager.register_plugin(mock_plugin)
        
        result = manager.execute_plugin("mock", {})
        
        assert result.success is False
        assert result.plugin_name == "mock"
        assert "Mock plugin failure" in result.error

    def test_execute_nonexistent_plugin(self):
        """Test execution of non-existent plugin"""
        manager = PluginManager()
        
        result = manager.execute_plugin("nonexistent", {})
        
        assert result.success is False
        assert "Plugin 'nonexistent' not found" in result.error
        assert result.plugin_name == "nonexistent"

    def test_get_plugin_help(self):
        """Test getting plugin help"""
        manager = PluginManager()
        
        # Test help for all plugins
        all_help = manager.get_plugin_help()
        assert "Available plugins:" in all_help
        assert "weather:" in all_help
        assert "quote:" in all_help
        
        # Test help for specific plugin
        weather_help = manager.get_plugin_help("weather")
        assert "Weather Plugin" in weather_help
        
        # Test help for non-existent plugin
        no_help = manager.get_plugin_help("nonexistent")
        assert "Plugin 'nonexistent' not found" in no_help


class TestWeatherPlugin:
    """Test cases for WeatherPlugin"""

    def test_weather_plugin_initialization(self):
        """Test weather plugin initialization"""
        plugin = WeatherPlugin()
        
        assert plugin.name == "weather"
        assert plugin.use_mock is True
        assert plugin.default_city == "Tokyo"

    def test_weather_plugin_mock_execution(self):
        """Test weather plugin with mock data"""
        plugin = WeatherPlugin({"use_mock": True})
        context = {"city": "Tokyo"}
        
        result = plugin.execute(context)
        
        assert result.success is True
        assert result.data["city"] == "Tokyo"
        assert "temperature" in result.data
        assert "description" in result.data
        assert result.data["note"] == "This is mock data for demonstration purposes"

    def test_weather_plugin_without_api_key(self):
        """Test weather plugin without API key"""
        plugin = WeatherPlugin({"use_mock": False})
        context = {}
        
        result = plugin.execute(context)
        
        assert result.success is False
        assert "API key not configured" in result.error

    def test_weather_plugin_validation(self):
        """Test weather plugin configuration validation"""
        # Mock mode should validate successfully
        plugin = WeatherPlugin({"use_mock": True})
        assert plugin.validate_config() is True
        
        # Real API mode without key should fail validation
        plugin = WeatherPlugin({"use_mock": False})
        assert plugin.validate_config() is False
        
        # Real API mode with key should pass validation
        plugin = WeatherPlugin({"use_mock": False, "api_key": "test123"})
        assert plugin.validate_config() is True

    def test_weather_plugin_help(self):
        """Test weather plugin help"""
        plugin = WeatherPlugin()
        help_text = plugin.get_help()
        
        assert "Weather Plugin" in help_text
        assert "api_key" in help_text
        assert "default_city" in help_text


class TestQuotePlugin:
    """Test cases for QuotePlugin"""

    def test_quote_plugin_initialization(self):
        """Test quote plugin initialization"""
        plugin = QuotePlugin()
        
        assert plugin.name == "quote"
        assert plugin.use_api is False
        assert plugin.category == "inspirational"

    def test_quote_plugin_builtin_execution(self):
        """Test quote plugin with built-in quotes"""
        plugin = QuotePlugin({"use_api": False})
        context = {}
        
        result = plugin.execute(context)
        
        assert result.success is True
        assert "text" in result.data
        assert "author" in result.data
        assert result.data["source"] == "built-in"

    @patch('requests.get')
    def test_quote_plugin_api_execution(self, mock_get):
        """Test quote plugin with API"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "content": "Test quote",
            "author": "Test Author"
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        plugin = QuotePlugin({"use_api": True})
        context = {}
        
        result = plugin.execute(context)
        
        assert result.success is True
        assert result.data["text"] == "Test quote"
        assert result.data["author"] == "Test Author"
        assert result.data["source"] == "api"

    @patch('requests.get')
    def test_quote_plugin_api_fallback(self, mock_get):
        """Test quote plugin API fallback to built-in"""
        mock_get.side_effect = Exception("API error")
        
        plugin = QuotePlugin({"use_api": True})
        context = {}
        
        result = plugin.execute(context)
        
        # Should fallback to built-in quotes
        assert result.success is True
        assert result.data["source"] == "built-in"

    def test_quote_plugin_validation(self):
        """Test quote plugin configuration validation"""
        plugin = QuotePlugin({"category": "inspirational"})
        assert plugin.validate_config() is True
        
        # Unknown category should still validate but log warning
        plugin = QuotePlugin({"category": "unknown"})
        assert plugin.validate_config() is True

    def test_quote_plugin_help(self):
        """Test quote plugin help"""
        plugin = QuotePlugin()
        help_text = plugin.get_help()
        
        assert "Quote Plugin" in help_text
        assert "use_api" in help_text
        assert "category" in help_text


if __name__ == "__main__":
    pytest.main([__file__])