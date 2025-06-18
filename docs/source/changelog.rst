Changelog
=========

All notable changes to Hello Project are documented here.

v1.3.0 (2025-06-18)
-------------------

**Major Features**

* **Configuration System**: Pydantic-based configuration with YAML/JSON support
* **Plugin System**: Extensible architecture with built-in plugins
* **Interactive Mode**: Real-time command execution interface
* **Multiple Output Formats**: Text and JSON output support

**Built-in Plugins**

* **Weather Plugin**: Get weather information (mock/API modes)
* **Quote Plugin**: Display inspirational quotes (built-in/API modes)

**Technical Improvements**

* Type-safe configuration management
* Environment variable override support
* Comprehensive error handling
* Plugin validation and fallback mechanisms

v1.2.0 (2025-06-18)
-------------------

**Testing & CI/CD**

* **pytest**: Comprehensive test suite
* **GitHub Actions**: Multi-Python version CI pipeline
* **Code Quality**: black, flake8, mypy, isort integration
* **uv Support**: Modern Python package management

**Development Experience**

* Makefile for common development tasks
* Test coverage reporting
* Type hints throughout codebase
* Automated code formatting

v1.1.0 (2025-06-18)
-------------------

**Documentation**

* Enhanced README with detailed setup instructions
* Usage examples and command references
* Project structure documentation
* Contribution guidelines

v1.0.0 (2025-06-18)
-------------------

**Initial Release**

* Basic hello world script with CLI arguments
* Command-line argument parsing
* Logging functionality
* Error handling

**Features**

* Name customization via ``--name`` argument
* Verbose logging with ``--verbose`` flag
* Help system
* Basic Python packaging structure