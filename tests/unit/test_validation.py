"""Unit tests for src.mcp_server.validation."""

from src.mcp_server.validation import validate_csv


class TestValidateCSV:
    def test_valid_csv(self, fixture_csv):
        errors = validate_csv(fixture_csv)
        assert errors == []

    def test_missing_file(self, tmp_path):
        errors = validate_csv(tmp_path / "does_not_exist.csv")
        assert len(errors) == 1
        assert "not found" in errors[0].lower()

    def test_not_a_file(self, tmp_path):
        errors = validate_csv(tmp_path)
        assert len(errors) == 1
        assert "not a file" in errors[0].lower()

    def test_missing_columns(self, bad_columns_csv):
        errors = validate_csv(bad_columns_csv)
        assert any("Missing required columns" in e for e in errors)

    def test_bad_numeric_types(self, bad_types_csv):
        errors = validate_csv(bad_types_csv)
        assert any("not numeric" in e.lower() for e in errors)
