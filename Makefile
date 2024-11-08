# Makefile

# ==============================================================================
# Variables
# ==============================================================================

# General
REPO_NAME ?= kom_python_core

# Python
PIPENV = pipenv run
PYTEST = $(PIPENV) pytest
RUFF = $(PIPENV) ruff

# ==============================================================================
# Phony Targets
# ==============================================================================
.PHONY: help lint lint-fix test test-cov install

# ==============================================================================
# Default Target
# ==============================================================================

help:
	@echo "Usage:"
	@echo "  make lint           Run ruff for linting"
	@echo "  make lint-fix       Fix linting issues using ruff"
	@echo "  make test           Run tests"
	@echo "  make test-cov       Run tests with coverage"
	@echo "  make install        Install dependencies"

# ==============================================================================
# Linting and Formatting
# ==============================================================================

lint:
	$(RUFF) check .

lint-fix:
	$(RUFF) check . --fix

# ==============================================================================
# Testing
# ==============================================================================

test:
	$(PYTEST)

test-cov:
	$(PYTEST) --cov-report=xml

# ==============================================================================
# Dependency Management
# ==============================================================================

install:
	pipenv sync --dev
