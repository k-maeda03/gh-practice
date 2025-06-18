Hello Project Documentation
============================

Welcome to the Hello Project documentation! This project is a comprehensive example of modern Python development practices, including configuration management, plugin systems, and interactive command-line interfaces.

.. note::
   This project was created as a GitHub CLI practice repository and has evolved into a full-featured demonstration of Python best practices.

Quick Start
-----------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/k-maeda03/gh-practice.git
   cd gh-practice

   # Setup development environment (with uv)
   make setup-dev

   # Run basic script
   python hello.py

   # Run enhanced version
   python hello_v2.py --help

Features
--------

* **Configuration Management**: Type-safe configuration with Pydantic
* **Plugin System**: Extensible architecture with built-in plugins
* **Interactive Mode**: Real-time command execution
* **Multiple Output Formats**: Text and JSON support
* **Comprehensive Testing**: pytest-based test suite
* **CI/CD Pipeline**: GitHub Actions integration

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   tutorials/index
   api/index
   development/index
   changelog

.. toctree::
   :maxdepth: 1
   :caption: API Reference:

   api/hello_project
   api/config
   api/plugins

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`