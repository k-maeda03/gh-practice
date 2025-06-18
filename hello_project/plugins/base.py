#!/usr/bin/env python3
"""
Base plugin system
"""
import importlib
import importlib.util
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass


@dataclass
class PluginResult:
    """Result from plugin execution"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    plugin_name: str = ""


class BasePlugin(ABC):
    """Base class for all plugins"""
    
    name: str = "base"
    description: str = "Base plugin"
    version: str = "1.0.0"
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize plugin with configuration
        
        Args:
            config: Plugin configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"plugin.{self.name}")
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> PluginResult:
        """Execute plugin functionality
        
        Args:
            context: Execution context with user input and settings
            
        Returns:
            PluginResult with execution result
        """
        pass
    
    def validate_config(self) -> bool:
        """Validate plugin configuration
        
        Returns:
            True if configuration is valid
        """
        return True
    
    def get_help(self) -> str:
        """Get help text for the plugin
        
        Returns:
            Help text describing plugin usage
        """
        return f"{self.name}: {self.description}"


class PluginManager:
    """Manages plugin loading and execution"""
    
    def __init__(self, plugin_directory: str = "plugins"):
        """Initialize plugin manager
        
        Args:
            plugin_directory: Directory containing plugins
        """
        self.plugin_directory = Path(plugin_directory)
        self.plugins: Dict[str, BasePlugin] = {}
        self.logger = logging.getLogger("plugin_manager")
        
        # Load built-in plugins
        self._load_builtin_plugins()
    
    def _load_builtin_plugins(self) -> None:
        """Load built-in plugins"""
        try:
            from .weather import WeatherPlugin
            from .quote import QuotePlugin
            
            self.register_plugin(WeatherPlugin())
            self.register_plugin(QuotePlugin())
            
        except ImportError as e:
            self.logger.warning(f"Failed to load built-in plugins: {e}")
    
    def register_plugin(self, plugin: BasePlugin) -> None:
        """Register a plugin
        
        Args:
            plugin: Plugin instance to register
        """
        if not isinstance(plugin, BasePlugin):
            raise ValueError(f"Plugin must inherit from BasePlugin")
        
        if not plugin.validate_config():
            raise ValueError(f"Plugin {plugin.name} has invalid configuration")
        
        self.plugins[plugin.name] = plugin
        self.logger.info(f"Registered plugin: {plugin.name}")
    
    def load_external_plugins(self) -> None:
        """Load plugins from external directory"""
        if not self.plugin_directory.exists():
            self.logger.info(f"Plugin directory {self.plugin_directory} does not exist")
            return
        
        for plugin_file in self.plugin_directory.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
                
            try:
                self._load_plugin_from_file(plugin_file)
            except Exception as e:
                self.logger.error(f"Failed to load plugin from {plugin_file}: {e}")
    
    def _load_plugin_from_file(self, plugin_file: Path) -> None:
        """Load a plugin from a Python file
        
        Args:
            plugin_file: Path to plugin file
        """
        module_name = f"external_plugin_{plugin_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load plugin from {plugin_file}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find plugin classes in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, BasePlugin) and 
                attr != BasePlugin):
                
                plugin_instance = attr()
                self.register_plugin(plugin_instance)
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get plugin by name
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin instance or None if not found
        """
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[str]:
        """Get list of available plugin names
        
        Returns:
            List of plugin names
        """
        return list(self.plugins.keys())
    
    def execute_plugin(self, name: str, context: Dict[str, Any]) -> PluginResult:
        """Execute a plugin
        
        Args:
            name: Plugin name
            context: Execution context
            
        Returns:
            Plugin execution result
        """
        plugin = self.get_plugin(name)
        if not plugin:
            return PluginResult(
                success=False,
                error=f"Plugin '{name}' not found",
                plugin_name=name
            )
        
        try:
            result = plugin.execute(context)
            result.plugin_name = name
            return result
        except Exception as e:
            self.logger.error(f"Plugin {name} execution failed: {e}")
            return PluginResult(
                success=False,
                error=str(e),
                plugin_name=name
            )
    
    def get_plugin_help(self, name: Optional[str] = None) -> str:
        """Get help for plugins
        
        Args:
            name: Optional plugin name for specific help
            
        Returns:
            Help text
        """
        if name:
            plugin = self.get_plugin(name)
            if plugin:
                return plugin.get_help()
            else:
                return f"Plugin '{name}' not found"
        else:
            # Return help for all plugins
            help_text = "Available plugins:\n"
            for plugin_name, plugin in self.plugins.items():
                help_text += f"  {plugin_name}: {plugin.description}\n"
            return help_text