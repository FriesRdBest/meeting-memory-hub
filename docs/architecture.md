# Architecture

This document describes the architecture of Meeting Memory Console.

## Overview

The application follows a layered architecture that separates concerns and enables automated testing.

```text
Streamlit interface (app.py, pages/)
        |
        v
Service layer (services/)
        |
        v
Repository layer (repositories/)
        |
        v
SQLite persistence (data/*.json)
        |
        v
Validated domain models (models/)
```

## Components

### Domain models

Located in `models/`.

- `signal.py` — Signal model for capturing meaningful observations from meetings
- `action.py` — Action model for tracking accountable work
- `reflection.py` — Reflection model for recording outcomes and learning

Models use Pydantic for validation and provide `from_dict` and `to_dict` methods for serialization.

### Repository layer

Located in `repositories/`.

- `json_store.py` — Shared JSON storage helper for reading and writing records
- `signal_repository.py` — Signal repository using JSON storage
- `action_repository.py` — Action repository using JSON storage
- `reflection_repository.py` — Reflection repository using JSON storage

Repositories provide `save` and `list_all` methods for persistence operations.

### Service layer

Located in `services/`.

- `signal_service.py` — Signal service for workflow operations
- `action_service.py` — Action service for workflow operations
- `reflection_service.py` — Reflection service for workflow operations

Services coordinate repository operations and implement business logic.

### User interface

Located in `app.py` and `pages/`.

- `app.py` — Main Streamlit application entry point
- `pages/` — Streamlit pages for Signal Desk, Pattern Library, Action Queue, and Learning Loop

The interface uses services to load and save data.

### Automated tests

Located in `tests/`.

- `test_models.py` — Domain model round trip tests
- `test_json_store.py` — JSON storage helper tests
- `test_repositories.py` — Repository layer tests
- `test_services.py` — Service layer tests
- `test_workflow.py` — End to end workflow test
- `test_quality_checks.py` — Quality checks before merge

Tests use pytest and run automatically via GitHub Actions.

## Data flow

1. User interacts with Streamlit interface
2. Interface calls service layer methods
3. Service layer coordinates repository operations
4. Repository layer reads or writes JSON files
5. Domain models validate data structure

## Quality checks

GitHub Actions runs automated tests on every push and pull request.

See [quality_checks.md](quality_checks.md) for details.

## Future considerations

A production implementation would consider:

- Database migration from JSON to SQLite or PostgreSQL
- Authentication and authorization
- API layer for external integrations
- Background jobs for async operations
- Logging and monitoring
- Security hardening and privacy controls
