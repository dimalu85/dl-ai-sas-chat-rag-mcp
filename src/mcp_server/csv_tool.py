"""CSV query logic for the natural disaster MCP tool."""

import time
from functools import lru_cache
from pathlib import Path

import pandas as pd

from src.config import CSV_QUERY_DEFAULT_LIMIT
from src.mcp_server.models import McpResponse, build_error_response, build_success_response
from src.mcp_server.validation import validate_csv


@lru_cache(maxsize=4)
def _load_csv(path: str) -> pd.DataFrame:
    """Load and cache a CSV file.  Uses string path for LRU hashability."""
    return pd.read_csv(path)


def query_disasters(
    csv_path: str | Path,
    *,
    country: str | None = None,
    disaster_type: str | None = None,
    year: int | None = None,
    year_range: tuple[int, int] | None = None,
    min_deaths: int | None = None,
    sort_by: str | None = None,
    limit: int = CSV_QUERY_DEFAULT_LIMIT,
) -> McpResponse:
    """Query the disaster CSV with optional filters.

    Parameters
    ----------
    csv_path : path to the CSV file
    country : filter by country name (case-insensitive substring match)
    disaster_type : filter by disaster type (case-insensitive substring match)
    year : filter by exact year
    year_range : filter by (start_year, end_year) inclusive
    min_deaths : minimum Total Deaths threshold
    sort_by : column name to sort descending
    limit : max rows to return (default 20)

    Returns
    -------
    McpResponse with data containing ``count``, ``total_matching``, ``rows``,
    and ``columns`` on success.
    """
    start = time.perf_counter()
    csv_path = str(Path(csv_path).resolve())

    # Validate first
    errors = validate_csv(csv_path)
    if errors:
        elapsed = (time.perf_counter() - start) * 1000
        return build_error_response("; ".join(errors), timing_ms=elapsed)

    try:
        df = _load_csv(csv_path)
        mask = pd.Series(True, index=df.index)

        if country:
            mask &= df["Country"].str.contains(country, case=False, na=False)

        if disaster_type:
            mask &= df["Disaster Type"].str.contains(disaster_type, case=False, na=False)

        if year is not None:
            mask &= df["Year"] == year

        if year_range is not None:
            yr_start, yr_end = year_range
            mask &= (df["Year"] >= yr_start) & (df["Year"] <= yr_end)

        if min_deaths is not None:
            mask &= df["Total Deaths"].fillna(0) >= min_deaths

        result = df[mask]

        if sort_by and sort_by in result.columns:
            result = result.sort_values(sort_by, ascending=False, na_position="last")

        total_matching = len(result)
        result = result.head(limit)

        # Select key columns for response readability
        display_cols = [
            c for c in [
                "Year", "Country", "Disaster Type", "Disaster Subtype",
                "Total Deaths", "Total Affected", "Total Damages ('000 US$)",
            ]
            if c in result.columns
        ]
        rows = result[display_cols].fillna("").to_dict(orient="records")

        elapsed = (time.perf_counter() - start) * 1000
        return build_success_response(
            data={
                "count": len(rows),
                "total_matching": total_matching,
                "columns": display_cols,
                "rows": rows,
            },
            timing_ms=round(elapsed, 2),
        )

    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return build_error_response(str(exc), timing_ms=elapsed)
