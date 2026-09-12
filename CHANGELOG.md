# Changelog

All notable changes to Meeting Memory Console are documented in this file.

## [Unreleased]

### Added

- Automated test suite for domain models, JSON storage, repositories, services, and end to end workflow
- GitHub Actions workflow for automated quality checks on push and pull request
- Quality checks that validate required workflow fields before merge
- `pyproject.toml` for project configuration and tool settings
- `requirements.txt` for dependency management
- `.gitignore` for Python, virtual environments, IDE, and testing files
- `CONTRIBUTING.md` with contribution guidelines and pull request checklist
- `CHANGELOG.md` for tracking changes
- Documentation of automated quality checks in README

### Changed

- Updated README testing section to reference automated quality checks

### Fixed

- Ensured data directory is tracked in version control with `.gitkeep`

## [0.1.0] - 2026-09-12

### Added

- Initial prototype with Signal Desk, Pattern Library, Action Queue, and Learning Loop
- Domain models for Signal, Action, and Reflection
- Repository and service layers for workflow management
- Streamlit interface for reviewing signals, actions, and learning
- Demonstration data for illustrative purposes
