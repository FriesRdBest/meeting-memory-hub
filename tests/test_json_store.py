from pathlib import Path

from repositories.json_store import read_records, write_records


def test_read_records_returns_empty_list_for_missing_file(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "missing.json"

    records = read_records(file_path)

    assert records == []


def test_write_records_creates_file_and_read_records_returns_data(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "nested" / "records.json"

    expected_records = [
        {
            "id": "SIG-001",
            "title": "Repeated onboarding friction is slowing adoption",
        },
        {
            "id": "SIG-002",
            "title": "Reporting requests are becoming a recurring theme",
        },
    ]

    write_records(file_path, expected_records)
    actual_records = read_records(file_path)

    assert file_path.exists()
    assert actual_records == expected_records
