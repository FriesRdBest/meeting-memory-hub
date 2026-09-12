# Contributing to Meeting Memory Console

This document describes how to contribute to the Meeting Memory Console prototype.

## Getting started

1. Fork the repository
2. Clone your fork
3. Create a new branch for your change
4. Make your changes
5. Run tests and quality checks
6. Open a pull request

## Code quality

Before opening a pull request, ensure the following checks pass locally.

Run tests:

```bash
python -m pytest tests/
```

Check formatting:

```bash
python -m ruff format --check .
```

Run linting:

```bash
python -m ruff check .
```

Apply formatting if needed:

```bash
python -m ruff format .
```

## Pull request checklist

- Tests pass locally and in GitHub Actions
- Code is formatted with Ruff
- Linting passes with no errors
- Commit messages are clear and descriptive
- Changes are documented in the README if relevant

## Questions

Open an issue to discuss larger changes or ask questions before starting work.
