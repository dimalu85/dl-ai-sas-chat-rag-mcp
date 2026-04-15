"""CSV file validation for the MCP server."""

from pathlib import Path

import pandas as pd

from src.config import REQUIRED_CSV_COLUMNS

# Columns that must be numeric (allow NaN, but non-null values must be numbers)
NUMERIC_COLUMNS = ["Year", "Total Deaths", "Total Affected"]


def validate_csv(path: str | Path) -> list[str]:
    """Validate a CSV file for use with the disaster query tool.

    Returns a list of error strings.  An empty list means the file is valid.
    """
    errors: list[str] = []
    path = Path(path)

    # 1. File existence
    if not path.exists():
        errors.append(f"File not found: {path}")
        return errors

    if not path.is_file():
        errors.append(f"Path is not a file: {path}")
        return errors

    # 2. Readable as CSV
    try:
        df = pd.read_csv(path, nrows=5)
    except Exception as exc:
        errors.append(f"Failed to read CSV: {exc}")
        return errors

    # 3. Required columns
    missing = [col for col in REQUIRED_CSV_COLUMNS if col not in df.columns]
    if missing:
        errors.append(f"Missing required columns: {missing}")
        return errors

    # 4. Numeric type checks (read full file for type validation)
    try:
        df_full = pd.read_csv(path, usecols=NUMERIC_COLUMNS)
    except Exception as exc:
        errors.append(f"Failed to read numeric columns: {exc}")
        return errors

    for col in NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df_full[col]):
            errors.append(
                f"Column '{col}' is not numeric (dtype: {df_full[col].dtype})"
            )

    return errors
