## Testing and code quality

Run tests.

```bash
python -m pytest tests/
```

Check formatting.

```bash
python -m ruff format --check .
```

Run linting.

```bash
python -m ruff check .
```

Apply formatting locally.

```bash
python -m ruff format .
```

### Automated quality checks

This branch includes automated tests that run before a pull request is considered for merge.

- `tests/test_models.py` — Domain model round trip tests
- `tests/test_json_store.py` — JSON storage helper tests
- `tests/test_repositories.py` — Repository layer tests
- `tests/test_services.py` — Service layer tests
- `tests/test_workflow.py` — End to end workflow test
- `tests/test_quality_checks.py` — Quality checks before merge

GitHub Actions runs these tests automatically on every push and pull request to `main`.
