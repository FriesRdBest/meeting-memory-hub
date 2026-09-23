# Meeting Memory Hub

A Streamlit workspace for turning meeting transcripts and notes into structured, searchable memory that supports follow-up, accountability, and institutional recall.

The app ingests transcripts or notes, extracts decisions, actions, owners, and context, and exposes them through filters and search so teams can quickly reconstruct what was decided, who owns what, and why.

## Features

- **Ingest** — Paste or upload meeting transcripts and notes in common formats.
- **Extract** — Derive decisions, action items, owners, deadlines, and context from raw text.
- **Organize** — Group items by meeting, project, team, or owner.
- **Search** — Find past decisions and commitments using keywords, people, or date ranges.
- **Export** — Generate summaries for follow-up emails, status reports, or project documentation.

## Local development

### Requirements

- Python 3.10 or later
- `pip`

### Setup

```bash
git clone https://github.com/FriesRdBest/meeting-memory-hub.git
cd meeting-memory-hub
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will provide a local URL, normally `http://localhost:8501`.

## Repository structure

```text
.
├── app.py                 # Streamlit application
├── config.py              # Configuration helpers
├── pages/                 # Additional Streamlit pages
├── models/                # Data models and schemas
├── services/              # Core services (parsing, extraction, export)
├── utils/                 # Shared utilities
├── tests/                 # Unit and integration tests
├── data/                  # Example transcripts and fixtures
├── docs/                  # Documentation and usage notes
├── scripts/               # Build and maintenance scripts
├── repositories/          # Data-access abstractions
├── requirements.txt       # Runtime dependencies
├── pyproject.toml         # Project metadata and tooling
├── .github/               # GitHub configuration
├── .streamlit/            # Streamlit configuration
├── .devcontainer/         # Codespaces / dev container setup
├── CHANGELOG.md           # Notable changes
├── CONTRIBUTING.md        # Contribution guidance
└── LICENSE                # Apache License 2.0
```

## Contributing

Contributions and focused feedback are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## License

Copyright 2026 Robin Sylvester.

Licensed under the [Apache License, Version 2.0](LICENSE).
