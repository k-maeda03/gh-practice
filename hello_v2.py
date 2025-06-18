#!/usr/bin/env python3
"""
Enhanced hello world script with configuration and plugin support
"""
import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from hello_project.config import ConfigManager, Settings
from hello_project.plugins import PluginManager


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration

    Args:
        verbose: Enable verbose logging
    """
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def format_output(
    data: Dict[str, Any], output_format: str, show_timestamp: bool = False
) -> str:
    """Format output according to specified format

    Args:
        data: Data to format
        output_format: Output format (text, json)
        show_timestamp: Whether to include timestamp

    Returns:
        Formatted output string
    """
    if show_timestamp:
        data["timestamp"] = datetime.now().isoformat()

    if output_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    else:
        # Text format
        lines = []
        if show_timestamp:
            lines.append(f"Time: {data.get('timestamp', '')}")

        lines.append(data.get("greeting", ""))

        if plugins_data := data.get("plugins"):
            lines.append("\nPlugin Results:")
            for plugin_name, plugin_result in plugins_data.items():
                if plugin_result.get("success"):
                    lines.append(f"\n{plugin_name.title()}:")
                    plugin_data = plugin_result.get("data", {})
                    if isinstance(plugin_data, dict):
                        for key, value in plugin_data.items():
                            if key != "note":
                                lines.append(f"  {key.title()}: {value}")
                        if note := plugin_data.get("note"):
                            lines.append(f"  Note: {note}")
                    else:
                        lines.append(f"  {plugin_data}")
                else:
                    lines.append(
                        f"\n{plugin_name.title()}: Error - {plugin_result.get('error')}"
                    )

        return "\n".join(lines)


def interactive_mode(
    config_manager: ConfigManager, plugin_manager: PluginManager
) -> None:
    """Run in interactive mode

    Args:
        config_manager: Configuration manager
        plugin_manager: Plugin manager
    """
    settings = config_manager.settings
    print("🤖 Hello Project Interactive Mode")
    print("Type 'help' for commands, 'quit' to exit")

    while True:
        try:
            user_input = input("\n> ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye! 👋")
                break
            elif user_input.lower() == "help":
                print(
                    """
Available commands:
  greet <name>     - Greet someone
  weather <city>   - Get weather for city  
  quote            - Get an inspirational quote
  plugins          - List available plugins
  config           - Show current configuration
  quit             - Exit interactive mode
                """
                )
            elif user_input.lower() == "plugins":
                print(plugin_manager.get_plugin_help())
            elif user_input.lower() == "config":
                print(f"Configuration:\n{settings.model_dump_json(indent=2)}")
            elif user_input.startswith("greet "):
                name = user_input[6:].strip()
                print(f"Hello, {name}!")
            elif user_input.startswith("weather "):
                city = user_input[8:].strip() or "Tokyo"
                result = plugin_manager.execute_plugin("weather", {"city": city})
                if result.success:
                    data = result.data
                    print(
                        f"Weather in {data['city']}: {data['temperature']}, {data['description']}"
                    )
                else:
                    print(f"Weather error: {result.error}")
            elif user_input.lower() == "quote":
                result = plugin_manager.execute_plugin("quote", {})
                if result.success:
                    data = result.data
                    print(f'"{data["text"]}" - {data["author"]}')
                else:
                    print(f"Quote error: {result.error}")
            else:
                print(
                    f"Unknown command: {user_input}. Type 'help' for available commands."
                )

        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except EOFError:
            print("\nGoodbye! 👋")
            break


def main() -> None:
    """Main function with enhanced features"""
    parser = argparse.ArgumentParser(
        description="Enhanced GitHub CLI practice script with plugins",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --name "World"
  %(prog)s --config config.yaml --plugin weather --plugin quote
  %(prog)s --interactive
  %(prog)s --plugins-help
        """,
    )

    parser.add_argument("--name", default=None, help="Name to greet")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument(
        "--plugin",
        action="append",
        dest="plugins",
        help="Enable plugin (can be used multiple times)",
    )
    parser.add_argument(
        "--plugins-help", action="store_true", help="Show help for all plugins"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument(
        "--output-format", choices=["text", "json"], help="Output format"
    )

    args = parser.parse_args()

    try:
        # Load configuration
        config_manager = ConfigManager(args.config)
        settings = config_manager.load_config()

        # Override settings with command line arguments
        if args.name is not None:
            settings.default_name = args.name
        if args.verbose:
            settings.verbose = True
        if args.output_format:
            settings.output_format = args.output_format

        # Setup logging
        setup_logging(settings.verbose)
        logger = logging.getLogger(__name__)

        if settings.verbose:
            logger.info("Starting enhanced hello script")

        # Initialize plugin manager
        plugin_manager = PluginManager()
        plugin_manager.load_external_plugins()

        # Show plugins help
        if args.plugins_help:
            print(plugin_manager.get_plugin_help())
            return

        # Run interactive mode
        if args.interactive:
            interactive_mode(config_manager, plugin_manager)
            return

        # Prepare output data
        output_data = {
            "greeting": f"Hello, {settings.default_name}!",
            "message": "This is an enhanced practice repository with plugin support.",
        }

        # Execute plugins
        plugins_to_run = args.plugins or []
        if plugins_to_run:
            plugins_data = {}
            for plugin_name in plugins_to_run:
                result = plugin_manager.execute_plugin(
                    plugin_name, {"name": settings.default_name}
                )
                plugins_data[plugin_name] = {
                    "success": result.success,
                    "data": result.data,
                    "error": result.error,
                }

            output_data["plugins"] = plugins_data

        # Output results
        formatted_output = format_output(
            output_data, settings.output_format, settings.show_timestamp
        )
        print(formatted_output)

        if settings.verbose:
            logger.info("Script completed successfully")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
