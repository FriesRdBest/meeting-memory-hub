# Meeting Memory Console

Turn useful conversation signals into structured, reviewable workflow.

## What this is

Meeting Memory Console helps organizations:

- Surface meaningful signals from conversations
- Group repeated signals into patterns
- Propose destinations and owners for review
- Record human decisions before action
- Preserve outcomes and learning as organizational memory

The current build uses fictional demonstration data to make the intended operating model tangible and inspectable.

## Quick start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

3. Open the URL shown in your terminal.

## Demo walkthrough

For a guided end-to-end demo, see:

- [docs/demo-walkthrough.md](docs/demo-walkthrough.md)

This walks you through:

- Signal Desk → Action Queue → Learning Loop
- Creating an action from SIG-001
- Recording a reflection and seeing the full trace

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

## Documentation

See the [docs/](docs/) folder for:

- [Architecture](docs/architecture.md)
- [Privacy and limitations](docs/privacy-and-limitations.md)
- [Quality checks](docs/quality_checks.md)
- [Demo walkthrough](docs/demo-walkthrough.md)

## Next steps

This prototype demonstrates the operating model. A production implementation would add:

- Live meeting ingestion
- Authentication and access control
- Production security and privacy controls
- Integration with existing systems
