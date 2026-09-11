# Meeting Memory Console

> From conversation to consequence.

Meeting Memory Console is a working Streamlit prototype for turning meeting intelligence into trusted memory, accountable action, and visible learning.

It is designed around a practical question.

> What happens after a useful signal appears in a meeting?

A transcript, summary, or action item can preserve what was said. This prototype focuses on what happens next. It makes a signal visible, shows the evidence behind it, proposes an accountable route, records action, and captures what the organisation learned from the result.

## Why it exists

Important companies contain more intelligence than they can currently use.

The problem is rarely that nobody noticed. The problem is that the noticing did not survive the meeting.

A decision may never be recorded. A customer objection may repeat across several conversations without becoming visible as a pattern. A product insight may reach the room but not the roadmap. A commitment may be made without a clear owner after the call ends.

Meeting Memory Console demonstrates one possible operating layer for preventing that value from disappearing.

## What it does

The application provides four focused workspaces.

| Workspace | Purpose |
| --- | --- |
| Signal Desk | Review meaningful signals that need attention |
| Pattern Library | Discover themes that repeat across conversations |
| Action Queue | Confirm destination, ownership, action, and workflow status |
| Learning Loop | Review completed work, observed outcomes, and recorded learning |

## Product principles

- Evidence before automation
- Human review before consequential action
- Clear ownership before workflow progress
- Outcomes and learning after completion
- Small, inspectable components over unnecessary complexity
- Demonstration data only

## Technical approach

The application uses:

- Python 3.11 or newer
- Streamlit for the interface
- Pydantic for validated domain models
- SQLite for local persistence
- Pandas for analysis and filtering
- Plotly for focused visual summaries
- Pytest for automated tests
- Ruff for formatting and linting
- GitHub Actions for automated quality checks

The project separates domain models, repositories, services, user interface code, data, tests, and documentation.

```text
Streamlit interface
        |
        v
Service layer
        |
        v
Repository layer
        |
        v
SQLite persistence
        |
        v
Validated domain models
```

## Local setup

Clone the repository.

```bash
git clone [https://github.com/FriesRdBest/meeting-memory-console.git](https://github.com/FriesRdBest/meeting-memory-console.git)
cd meeting-memory-console
```

Create and activate a virtual environment.

```bash
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the application.

```bash
python -m streamlit run app.py
```

## Testing and code quality

Run tests.

```bash
python -m pytest
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

## Demonstration data

All data in this repository is illustrative and fictional.

The application includes no real company data, customer data, meeting recordings, transcripts, personal information, internal information, or data from TL;DV. Account names, meeting names, quotes, owners, actions, and outcomes exist only to demonstrate the workflow.

The application supports a reset to the original demonstration dataset after interactions.

## Documentation

- [Architecture](docs/architecture.md)
- [Privacy and limitations](docs/privacy-and-limitations.md)

## Intentional scope

This is a working product prototype, not a production deployment.

It intentionally does not include authentication, access controls, live integrations, real time updates, background jobs, multi user collaboration, cloud infrastructure, real customer information, or production security operations.

A production implementation would require stakeholder requirements, user research, security review, privacy assessment, data governance, integration design, engineering collaboration, and measured rollout.

## Role proposal context

Meeting Memory Console was built as a working proposal for a Director of Intelligence Design & Operations role.

The prototype demonstrates a way to transform conversation intelligence into a reliable organisational system. The purpose is not merely to preserve what happened in a meeting. It is to make useful information easier to find, easier to own, harder to lose, and more likely to improve what happens next.

## License

This repository is shared for review purposes. No license is granted for reuse, modification, redistribution, or commercial use.
