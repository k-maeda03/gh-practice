.PHONY: help install install-dev test lint format type-check clean run install-hooks

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies with uv
	uv pip install -e .

install-dev: ## Install development dependencies with uv
	uv pip install -e ".[dev]"

test: ## Run tests with pytest
	uv run pytest

test-cov: ## Run tests with coverage report
	uv run pytest --cov=. --cov-report=term-missing --cov-report=html

lint: ## Run linting with flake8
	uv run flake8 .

format: ## Format code with black and isort
	uv run black .
	uv run isort .

format-check: ## Check if code is formatted correctly
	uv run black --check .
	uv run isort --check-only .

type-check: ## Run type checking with mypy
	uv run mypy hello.py

run: ## Run the hello script
	uv run python hello.py

run-help: ## Show hello script help
	uv run python hello.py --help

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

ci: format-check lint type-check test ## Run all CI checks

docs: ## Build documentation with Sphinx
	uv run sphinx-build -b html docs/source docs/build

docs-live: ## Build documentation and watch for changes
	uv run sphinx-autobuild docs/source docs/build

docs-clean: ## Clean documentation build
	rm -rf docs/build

setup-dev: ## Setup development environment
	@echo "Setting up development environment with uv..."
	@echo "Make sure uv is installed: curl -LsSf https://astral.sh/uv/install.sh | sh"
	uv venv
	@echo "Activate venv with: source .venv/bin/activate"
	uv pip install -e ".[dev,docs]"
	@echo "Development environment ready!"

install-hooks: ## Install git hooks for pre-push checks
	@echo "Installing git hooks..."
	./scripts/install-hooks.sh
	@echo "Git hooks installed! Tests will run before each push."