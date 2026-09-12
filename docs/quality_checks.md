# Quality checks

This document describes the automated quality checks that run before a pull request is considered for merge.

## Test suite

The test suite validates the core workflow components.

| Test module | Purpose |
| --- | --- |
| `tests/test_models.py` | Domain model round trip tests for Signal, Action, and Reflection |
| `tests/test_json_store.py` | JSON storage helper tests for reading and writing records |
| `tests/test_repositories.py` | Repository layer tests for save and list operations |
| `tests/test_services.py` | Service layer tests for workflow operations |
| `tests/test_workflow.py` | End to end test for Signal → Action → Reflection workflow |
| `tests/test_quality_checks.py` | Quality checks that validate required fields before merge |

## GitHub Actions

The `.github/workflows/quality_checks.yml` workflow runs on every push and pull request.

The workflow:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs pytest
4. Runs all tests in the `tests/` directory

A pull request is ready for review when all tests pass.

## Running tests locally

Run all tests:

```bash
python -m pytest tests/
```

Run a specific test module:

```bash
python -m pytest tests/test_models.py
```

Run tests with verbose output:

```bash
python -m pytest tests/ -v
```

## Quality checklist

Before opening a pull request, confirm:

- All tests pass locally
- Code is formatted with Ruff
- Linting passes with no errors
- New features include corresponding tests
- Documentation is updated if relevant
