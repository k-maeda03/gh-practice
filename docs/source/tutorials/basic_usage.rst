Basic Usage Tutorial
====================

This tutorial covers the fundamental usage of Hello Project, from basic commands to advanced features.

Introduction
------------

Hello Project provides two main entry points:

1. **hello.py**: A simple greeting script with basic functionality
2. **hello_v2.py**: An enhanced version with configuration and plugin support

Let's explore both!

Basic Script (hello.py)
-----------------------

The basic script demonstrates fundamental Python CLI patterns.

Simple Greeting
~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ python hello.py
   Hello, GitHub CLI!
   This is an improved practice repository.

Custom Name
~~~~~~~~~~~

.. code-block:: bash

   $ python hello.py --name "World"
   Hello, World!
   This is an improved practice repository.

Verbose Mode
~~~~~~~~~~~~

.. code-block:: bash

   $ python hello.py --verbose
   2025-06-18 15:30:00,123 - __main__ - INFO - Starting hello script
   Hello, GitHub CLI!
   This is an improved practice repository.
   2025-06-18 15:30:00,124 - __main__ - INFO - Script completed successfully

Enhanced Script (hello_v2.py)
------------------------------

The enhanced script includes configuration management, plugins, and multiple output formats.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py
   Hello, GitHub CLI!
   This is an enhanced practice repository with plugin support.

Help Information
~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py --help
   usage: hello_v2.py [-h] [--name NAME] [--config CONFIG] [--plugin PLUGINS]
                      [--plugins-help] [--verbose] [--interactive]
                      [--output-format {text,json}]

   Enhanced GitHub CLI practice script with plugins

   optional arguments:
     -h, --help            show this help message and exit
     --name NAME           Name to greet
     --config CONFIG       Path to configuration file
     --plugin PLUGINS      Enable plugin (can be used multiple times)
     --plugins-help        Show help for all plugins
     --verbose             Enable verbose logging
     --interactive         Run in interactive mode
     --output-format {text,json}
                           Output format

Command-Line Arguments
----------------------

Name Customization
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py --name "Python Developer"
   Hello, Python Developer!
   This is an enhanced practice repository with plugin support.

Verbose Output
~~~~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py --verbose
   2025-06-18 15:30:00,123 - __main__ - INFO - Starting enhanced hello script
   Hello, GitHub CLI!
   This is an enhanced practice repository with plugin support.
   2025-06-18 15:30:00,124 - __main__ - INFO - Script completed successfully

JSON Output
~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py --output-format json
   {
     "greeting": "Hello, GitHub CLI!",
     "message": "This is an enhanced practice repository with plugin support."
   }

JSON with Timestamp
~~~~~~~~~~~~~~~~~~~

When using a configuration file with ``show_timestamp: true``:

.. code-block:: bash

   $ python hello_v2.py --output-format json --config config.yaml
   {
     "greeting": "Hello, GitHub CLI!",
     "message": "This is an enhanced practice repository with plugin support.",
     "timestamp": "2025-06-18T15:30:00.123456"
   }

Using Plugins
-------------

Plugin Help
~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py --plugins-help
   Available plugins:
     weather: Get current weather information
     quote: Get inspirational quotes

Single Plugin
~~~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py --plugin weather
   Hello, GitHub CLI!
   This is an enhanced practice repository with plugin support.

   Plugin Results:

   Weather:
     City: Tokyo
     Temperature: 22°C
     Description: Partly cloudy
     Humidity: 65%
     Wind: 5 km/h
     Note: This is mock data for demonstration purposes

Multiple Plugins
~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ python hello_v2.py --plugin weather --plugin quote
   Hello, GitHub CLI!
   This is an enhanced practice repository with plugin support.

   Plugin Results:

   Weather:
     City: Tokyo
     Temperature: 22°C
     Description: Partly cloudy
     Humidity: 65%
     Wind: 5 km/h
     Note: This is mock data for demonstration purposes

   Quote:
     "The way to get started is to quit talking and begin doing." - Walt Disney

Common Patterns
---------------

Development Workflow
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Test basic functionality
   python hello.py --name "Test"

   # Test enhanced features
   python hello_v2.py --verbose

   # Test with plugins
   python hello_v2.py --plugin weather --plugin quote

   # Test JSON output
   python hello_v2.py --output-format json

Production Usage
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Use with configuration file
   python hello_v2.py --config production.yaml

   # Generate JSON for API integration
   python hello_v2.py --output-format json --plugin weather > output.json

   # Interactive session for testing
   python hello_v2.py --interactive

Troubleshooting
---------------

Import Errors
~~~~~~~~~~~~~

If you get import errors:

.. code-block:: bash

   # Make sure you're in the project directory
   cd /path/to/gh-practice

   # Check Python path
   python -c "import sys; print(sys.path)"

   # Install dependencies
   uv pip install -e ".[dev]"

Plugin Errors
~~~~~~~~~~~~~

If plugins fail to load:

.. code-block:: bash

   # Check plugin help
   python hello_v2.py --plugins-help

   # Run with verbose mode
   python hello_v2.py --verbose --plugin weather

Configuration Issues
~~~~~~~~~~~~~~~~~~~~

If configuration loading fails:

.. code-block:: bash

   # Check configuration syntax
   python -c "import yaml; yaml.safe_load(open('config.yaml'))"

   # Use verbose mode to see loading process
   python hello_v2.py --verbose --config config.yaml

Next Steps
----------

* Learn about :doc:`configuration` management
* Explore the :doc:`plugins` system
* Try :doc:`interactive_mode` features
* Create :doc:`custom_plugins`