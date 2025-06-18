Development Guide
================

This section covers development practices, contributing guidelines, and advanced topics.

.. toctree::
   :maxdepth: 2

   contributing
   coding_style
   testing
   troubleshooting

Quick Start for Developers
--------------------------

.. code-block:: bash

   # Clone and setup
   git clone https://github.com/k-maeda03/gh-practice.git
   cd gh-practice
   make setup-dev

   # Run tests
   make test

   # Code quality checks
   make ci

Development Workflow
--------------------

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Run** tests and quality checks
5. **Submit** a pull request

Key Commands
------------

.. code-block:: bash

   make test          # Run tests
   make format        # Format code
   make lint          # Lint code
   make type-check    # Type checking
   make ci            # All quality checks