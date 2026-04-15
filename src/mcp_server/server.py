"""MCP server exposing natural disaster CSV query tool via stdio transport."""

from mcp.server.fastmcp import FastMCP

from src.config import CSV_PATH, MCP_SERVER_NAME
from src.mcp_server.csv_tool import query_disasters

mcp = FastMCP(MCP_SERVER_NAME)


@mcp.tool()
def query_natural_disasters(
    country: str | None = None,
    disaster_type: str | None = None,
    year: int | None = None,
    year_start: int | None = None,
    year_end: int | None = None,
    min_deaths: int | None = None,
    sort_by: str | None = None,
    limit: int = 20,
) -> dict:
    """Query the EM-DAT natural disaster dataset (1970-2021).

    Filters are optional and combinable:
    - country: filter by country name (substring, case-insensitive)
    - disaster_type: filter by type, e.g. Earthquake, Flood, Storm
    - year: exact year
    - year_start / year_end: year range (inclusive)
    - min_deaths: minimum death toll
    - sort_by: column to sort by descending (e.g. 'Total Deaths')
    - limit: max rows returned (default 20)

    Returns a dict with ok, data (count, total_matching, rows), error, and meta.
    """
    year_range = None
    if year_start is not None and year_end is not None:
        year_range = (year_start, year_end)

    response = query_disasters(
        csv_path=CSV_PATH,
        country=country,
        disaster_type=disaster_type,
        year=year,
        year_range=year_range,
        min_deaths=min_deaths,
        sort_by=sort_by,
        limit=limit,
    )
    return response.model_dump()


if __name__ == "__main__":
    mcp.run(transport="stdio")
