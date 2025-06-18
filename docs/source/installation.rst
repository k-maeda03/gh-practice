Installation
============

This guide covers the installation of Hello Project and its dependencies.

Prerequisites
-------------

* **Python 3.8+** is required
* **uv** (recommended package manager) or **pip**

Installing uv
--------------

We recommend using uv for fast package management:

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh

For other installation methods, see the `uv documentation <https://docs.astral.sh/uv/>`_.

Installation Methods
--------------------

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~~

For development and contributing:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/k-maeda03/gh-practice.git
   cd gh-practice

   # Setup development environment
   make setup-dev

   # Or manually:
   uv venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   uv pip install -e ".[dev,docs]"

Production Installation
~~~~~~~~~~~~~~~~~~~~~~~

For production use (once published to PyPI):

.. code-block:: bash

   # With uv
   uv pip install gh-practice

   # With pip
   pip install gh-practice

Verification
------------

Verify your installation:

.. code-block:: bash

   # Test basic functionality
   python hello.py --help

   # Test enhanced version
   python hello_v2.py --help

   # Run tests (development installation)
   make test

   # Check installed version
   python -c "import hello_project; print(hello_project.__version__)"

Dependencies
------------

Core Dependencies
~~~~~~~~~~~~~~~~~

* **pydantic>=2.0.0**: Configuration management
* **pyyaml>=6.0.0**: YAML configuration files
* **requests>=2.28.0**: HTTP requests for plugins

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

* **pytest>=7.0.0**: Testing framework
* **pytest-cov>=4.0.0**: Test coverage
* **black>=22.0.0**: Code formatting
* **flake8>=6.0.0**: Linting
* **mypy>=1.0.0**: Type checking
* **isort>=5.0.0**: Import sorting

Documentation Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **sphinx>=7.0.0**: Documentation generation
* **sphinx-rtd-theme>=1.3.0**: ReadTheDocs theme
* **sphinx-autodoc-typehints>=1.24.0**: Type hints in docs
* **myst-parser>=2.0.0**: Markdown support

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import errors after installation**

Make sure you're in the correct virtual environment:

.. code-block:: bash

   which python
   python -c "import hello_project"

**uv not found**

Install uv or use pip as a fallback:

.. code-block:: bash

   pip install -e ".[dev,docs]"

**Permission errors**

Use virtual environments to avoid system-wide installations:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the `GitHub Issues <https://github.com/k-maeda03/gh-practice/issues>`_
2. Review the :doc:`development/troubleshooting` guide
3. Create a new issue with detailed information