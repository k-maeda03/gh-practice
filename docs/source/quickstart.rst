Quick Start Guide
=================

This guide will get you up and running with Hello Project in just a few minutes.

Basic Usage
-----------

Hello Project provides two main scripts:

1. **hello.py**: Basic script with command-line arguments
2. **hello_v2.py**: Enhanced version with configuration and plugins

Basic Script
~~~~~~~~~~~~

.. code-block:: bash

   # Simple greeting
   python hello.py

   # Custom name
   python hello.py --name "World"

   # Verbose mode
   python hello.py --verbose

Enhanced Script
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Basic usage
   python hello_v2.py

   # With configuration file
   python hello_v2.py --config config.yaml

   # Using plugins
   python hello_v2.py --plugin weather --plugin quote

   # Interactive mode
   python hello_v2.py --interactive

   # JSON output
   python hello_v2.py --output-format json

Configuration
-------------

Hello Project supports flexible configuration through multiple sources:

Configuration File
~~~~~~~~~~~~~~~~~~

Create a ``config.yaml`` file:

.. code-block:: yaml

   # Basic settings
   default_name: "GitHub CLI User"
   verbose: false
   output_format: "text"
   show_timestamp: false

   # Plugin configurations
   plugins:
     - name: "weather"
       enabled: true
       config:
         use_mock: true
         default_city: "Tokyo"
     
     - name: "quote"
       enabled: true
       config:
         use_api: false
         category: "inspirational"

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Override settings with environment variables:

.. code-block:: bash

   export HELLO_DEFAULT_NAME="Environment User"
   export HELLO_VERBOSE=true
   export HELLO_OUTPUT_FORMAT=json

   python hello_v2.py

Plugins
-------

Hello Project includes a powerful plugin system:

Built-in Plugins
~~~~~~~~~~~~~~~~

**Weather Plugin**
  Get weather information for any city.

  .. code-block:: bash

     python hello_v2.py --plugin weather

**Quote Plugin**
  Display inspirational quotes.

  .. code-block:: bash

     python hello_v2.py --plugin quote

Plugin Help
~~~~~~~~~~~

Get information about available plugins:

.. code-block:: bash

   # List all plugins
   python hello_v2.py --plugins-help

   # In interactive mode
   python hello_v2.py --interactive
   > plugins

Interactive Mode
----------------

The interactive mode provides a command-line interface:

.. code-block:: bash

   python hello_v2.py --interactive

Available commands:

.. code-block:: text

   > greet World           # Greet someone
   > weather Tokyo         # Get weather
   > quote                 # Get a quote
   > plugins               # List plugins
   > config                # Show configuration
   > help                  # Show help
   > quit                  # Exit

Output Formats
--------------

Text Format (Default)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Hello, GitHub CLI!
   This is an enhanced practice repository with plugin support.

   Plugin Results:

   Weather:
     City: Tokyo
     Temperature: 22°C
     Description: Partly cloudy

   Quote:
     "The way to get started is to quit talking and begin doing." - Walt Disney

JSON Format
~~~~~~~~~~~

.. code-block:: json

   {
     "greeting": "Hello, GitHub CLI!",
     "message": "This is an enhanced practice repository with plugin support.",
     "plugins": {
       "weather": {
         "success": true,
         "data": {
           "city": "Tokyo",
           "temperature": "22°C",
           "description": "Partly cloudy"
         }
       }
     }
   }

Development Commands
--------------------

If you're contributing or modifying the code:

.. code-block:: bash

   # Run tests
   make test

   # Code formatting
   make format

   # Linting
   make lint

   # Type checking
   make type-check

   # All checks
   make ci

Next Steps
----------

* Read the :doc:`tutorials/index` for detailed examples
* Check the :doc:`api/index` for technical details
* See :doc:`development/index` for contributing guidelines