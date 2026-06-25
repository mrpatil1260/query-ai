import csv
from pathlib import Path

from app.services.pdf_service import extract_text_from_file


def test_extract_text_from_txt(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello Query AI", encoding="utf-8")

    text = extract_text_from_file(str(file_path))

    assert "Hello Query AI" in text


def test_extract_text_from_md(tmp_path):
    file_path = tmp_path / "sample.md"
    file_path.write_text("# Heading\n\nSome markdown content.", encoding="utf-8")

    text = extract_text_from_file(str(file_path))

    assert "Heading" in text
    assert "Some markdown content." in text


def test_extract_text_from_csv(tmp_path):
    file_path = tmp_path / "sample.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Role"])
        writer.writerow(["Prasad", "Engineer"])

    text = extract_text_from_file(str(file_path))

    assert "Name | Role" in text
    assert "Prasad | Engineer" in text


def test_unsupported_file_type(tmp_path):
    file_path = tmp_path / "sample.xyz"
    file_path.write_text("dummy", encoding="utf-8")

    try:
        extract_text_from_file(str(file_path))
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "Unsupported file type" in str(e)