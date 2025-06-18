Configuration Management
=======================

Hello Project uses a sophisticated configuration system based on Pydantic for type safety and validation.

Configuration Sources
---------------------

Configuration is loaded from multiple sources in order of priority:

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration files**
4. **Default values** (lowest priority)

Configuration Files
-------------------

Supported Formats
~~~~~~~~~~~~~~~~~

Hello Project supports both YAML and JSON configuration files:

**YAML Format (Recommended)**

.. code-block:: yaml

   # config.yaml
   default_name: "GitHub CLI User"
   verbose: false
   output_format: "text"
   show_timestamp: false

   plugins:
     - name: "weather"
       enabled: true
       config:
         use_mock: true
         default_city: "Tokyo"

**JSON Format**

.. code-block:: json

   {
     "default_name": "GitHub CLI User",
     "verbose": false,
     "output_format": "text",
     "show_timestamp": false,
     "plugins": [
       {
         "name": "weather",
         "enabled": true,
         "config": {
           "use_mock": true,
           "default_city": "Tokyo"
         }
       }
     ]
   }

File Locations
~~~~~~~~~~~~~~

Configuration files are searched in this order:

1. Path specified with ``--config`` argument
2. ``~/.config/hello_project/config.yaml``
3. ``./config.yaml`` (current directory)
4. ``./hello_config.yaml`` (current directory)

Configuration Schema
--------------------

The configuration follows a strict schema defined by Pydantic models:

Basic Settings
~~~~~~~~~~~~~~

.. code-block:: yaml

   # Greeting configuration
   default_name: "GitHub CLI"        # Default name for greetings
   verbose: false                    # Enable verbose logging

   # Output configuration
   output_format: "text"             # "text" or "json"
   show_timestamp: false             # Include timestamp in output

   # API configuration
   api_timeout: 10                   # Timeout for API requests (seconds)

Plugin Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   plugins:
     - name: "weather"               # Plugin name
       enabled: true                 # Enable/disable plugin
       config:                       # Plugin-specific configuration
         use_mock: true
         default_city: "Tokyo"
         api_key: "your_api_key"     # Optional for real API

     - name: "quote"
       enabled: true
       config:
         use_api: false
         category: "inspirational"
         language: "en"

   plugin_directory: "plugins"       # Directory for external plugins

Environment Variables
---------------------

Override any configuration value using environment variables:

Variable Mapping
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Basic settings
   export HELLO_DEFAULT_NAME="Environment User"
   export HELLO_VERBOSE=true
   export HELLO_OUTPUT_FORMAT=json
   export HELLO_SHOW_TIMESTAMP=true
   export HELLO_API_TIMEOUT=20

Boolean Values
~~~~~~~~~~~~~~

For boolean settings, use these values:

- **True**: ``true``, ``1``, ``yes``
- **False**: ``false``, ``0``, ``no``

.. code-block:: bash

   # These all set verbose to true
   export HELLO_VERBOSE=true
   export HELLO_VERBOSE=1
   export HELLO_VERBOSE=yes

Usage Examples
--------------

Basic Configuration
~~~~~~~~~~~~~~~~~~~

Create a simple ``config.yaml``:

.. code-block:: yaml

   default_name: "My Project"
   verbose: true
   output_format: "json"

Use it:

.. code-block:: bash

   python hello_v2.py --config config.yaml

Development Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``dev-config.yaml`` for development:

.. code-block:: yaml

   default_name: "Developer"
   verbose: true
   show_timestamp: true
   
   plugins:
     - name: "weather"
       enabled: true
       config:
         use_mock: true          # Use mock data during development
         default_city: "Tokyo"

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Create ``prod-config.yaml`` for production:

.. code-block:: yaml

   default_name: "Production User"
   verbose: false
   output_format: "json"
   show_timestamp: true
   
   plugins:
     - name: "weather"
       enabled: true
       config:
         use_mock: false         # Use real API in production
         api_key: "${WEATHER_API_KEY}"  # Use environment variable
         default_city: "New York"

Plugin-Specific Configuration
-----------------------------

Weather Plugin
~~~~~~~~~~~~~~

.. code-block:: yaml

   plugins:
     - name: "weather"
       enabled: true
       config:
         # Mock mode (no API key required)
         use_mock: true
         default_city: "Tokyo"
         
         # Real API mode
         # use_mock: false
         # api_key: "your_openweathermap_api_key"
         # default_city: "London"

Quote Plugin
~~~~~~~~~~~~

.. code-block:: yaml

   plugins:
     - name: "quote"
       enabled: true
       config:
         # Use built-in quotes
         use_api: false
         category: "inspirational"
         language: "en"
         
         # Use external API
         # use_api: true
         # category: "motivational"

Configuration Validation
-------------------------

Hello Project validates all configuration values:

Type Validation
~~~~~~~~~~~~~~~

.. code-block:: bash

   # This will fail - api_timeout must be an integer
   python hello_v2.py --config invalid-config.yaml

   # Error: Configuration validation failed: 
   # api_timeout: Input should be a valid integer

Required Fields
~~~~~~~~~~~~~~~

All configuration fields have sensible defaults, so no fields are strictly required.

Value Constraints
~~~~~~~~~~~~~~~~~

- ``output_format``: Must be "text" or "json"
- ``api_timeout``: Must be a positive integer
- Plugin names must be valid Python identifiers

Advanced Usage
--------------

Multiple Configuration Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can't directly merge multiple configuration files, but you can use environment variables to override specific values:

.. code-block:: bash

   # Use base config with environment overrides
   export HELLO_VERBOSE=true
   python hello_v2.py --config base-config.yaml

Dynamic Configuration
~~~~~~~~~~~~~~~~~~~~~

Generate configuration programmatically:

.. code-block:: python

   from hello_project.config import Settings, ConfigManager

   # Create settings programmatically
   settings = Settings(
       default_name="Dynamic User",
       verbose=True,
       output_format="json"
   )

   # Save to file
   manager = ConfigManager()
   manager.save_config(settings, "dynamic-config.yaml")

Configuration Debugging
-----------------------

View Current Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

In interactive mode:

.. code-block:: bash

   python hello_v2.py --interactive
   > config

Or check with verbose logging:

.. code-block:: bash

   python hello_v2.py --verbose --config your-config.yaml

Validate Configuration
~~~~~~~~~~~~~~~~~~~~~

Test configuration file syntax:

.. code-block:: python

   import yaml
   from hello_project.config import Settings

   # Load and validate
   with open('config.yaml') as f:
       config_data = yaml.safe_load(f)
   
   settings = Settings(**config_data)
   print("Configuration is valid!")

Common Configuration Patterns
-----------------------------

User-Specific Settings
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # ~/.config/hello_project/config.yaml
   default_name: "Your Name"
   verbose: false
   
   plugins:
     - name: "weather"
       config:
         default_city: "Your City"

Project-Specific Settings
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # ./config.yaml (in project directory)
   default_name: "Project User"
   output_format: "json"
   show_timestamp: true

CI/CD Configuration
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # ci-config.yaml
   verbose: true
   output_format: "json"
   
   plugins: []  # Disable all plugins in CI

Next Steps
----------

* Learn about the :doc:`plugins` system
* Explore :doc:`interactive_mode` features
* See the :doc:`../api/config` reference