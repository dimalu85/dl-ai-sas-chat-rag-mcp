"""Shared test fixtures for the natural disaster chat app."""

import csv
import os
import sys
import tempfile

import pytest

# Ensure src/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


FIXTURE_CSV_ROWS = [
    {
        "Year": "2010",
        "Country": "Haiti",
        "Disaster Type": "Earthquake",
        "Disaster Subtype": "Ground movement",
        "Total Deaths": "222570",
        "Total Affected": "3700000",
        "Total Damages ('000 US$)": "8000000",
    },
    {
        "Year": "2011",
        "Country": "Japan",
        "Disaster Type": "Earthquake",
        "Disaster Subtype": "Tsunami",
        "Total Deaths": "19846",
        "Total Affected": "368820",
        "Total Damages ('000 US$)": "210000000",
    },
    {
        "Year": "2005",
        "Country": "United States",
        "Disaster Type": "Storm",
        "Disaster Subtype": "Tropical cyclone",
        "Total Deaths": "1833",
        "Total Affected": "500000",
        "Total Damages ('000 US$)": "125000000",
    },
    {
        "Year": "2008",
        "Country": "China",
        "Disaster Type": "Earthquake",
        "Disaster Subtype": "Ground movement",
        "Total Deaths": "87564",
        "Total Affected": "45976596",
        "Total Damages ('000 US$)": "85000000",
    },
    {
        "Year": "2020",
        "Country": "Japan",
        "Disaster Type": "Flood",
        "Disaster Subtype": "Riverine flood",
        "Total Deaths": "82",
        "Total Affected": "5000",
        "Total Damages ('000 US$)": "",
    },
]

FIXTURE_CSV_COLUMNS = list(FIXTURE_CSV_ROWS[0].keys())


@pytest.fixture
def fixture_csv(tmp_path):
    """Create a small fixture CSV and return its path."""
    csv_path = tmp_path / "test_disasters.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIXTURE_CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(FIXTURE_CSV_ROWS)
    return csv_path


@pytest.fixture
def bad_columns_csv(tmp_path):
    """CSV with wrong columns."""
    csv_path = tmp_path / "bad_columns.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["A", "B", "C"])
        writer.writeheader()
        writer.writerow({"A": 1, "B": 2, "C": 3})
    return csv_path


@pytest.fixture
def bad_types_csv(tmp_path):
    """CSV with required columns but non-numeric Year."""
    csv_path = tmp_path / "bad_types.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIXTURE_CSV_COLUMNS)
        writer.writeheader()
        row = dict(FIXTURE_CSV_ROWS[0])
        row["Year"] = "not-a-number"
        row["Total Deaths"] = "abc"
        writer.writerow(row)
    return csv_path
