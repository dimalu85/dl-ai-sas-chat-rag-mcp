"""Unit tests for src.mcp_server.csv_tool."""

from src.mcp_server.csv_tool import _load_csv, query_disasters


class TestQueryDisasters:
    def test_filter_by_country(self, fixture_csv):
        r = query_disasters(fixture_csv, country="Japan")
        assert r.ok
        assert r.data["total_matching"] == 2
        countries = {row["Country"] for row in r.data["rows"]}
        assert countries == {"Japan"}

    def test_filter_by_year(self, fixture_csv):
        r = query_disasters(fixture_csv, year=2010)
        assert r.ok
        assert r.data["total_matching"] == 1
        assert r.data["rows"][0]["Country"] == "Haiti"

    def test_filter_by_year_range(self, fixture_csv):
        r = query_disasters(fixture_csv, year_range=(2008, 2011))
        assert r.ok
        assert r.data["total_matching"] == 3  # Haiti 2010, Japan 2011, China 2008

    def test_filter_by_disaster_type(self, fixture_csv):
        r = query_disasters(fixture_csv, disaster_type="Earthquake")
        assert r.ok
        assert r.data["total_matching"] == 3

    def test_filter_by_min_deaths(self, fixture_csv):
        r = query_disasters(fixture_csv, min_deaths=10000)
        assert r.ok
        assert r.data["total_matching"] == 3  # Haiti, Japan, China

    def test_combined_filters(self, fixture_csv):
        r = query_disasters(
            fixture_csv, disaster_type="Earthquake", min_deaths=50000
        )
        assert r.ok
        assert r.data["total_matching"] == 2  # Haiti, China

    def test_sort_by(self, fixture_csv):
        r = query_disasters(fixture_csv, sort_by="Total Deaths")
        assert r.ok
        assert r.data["rows"][0]["Country"] == "Haiti"

    def test_limit(self, fixture_csv):
        r = query_disasters(fixture_csv, limit=2)
        assert r.ok
        assert r.data["count"] == 2
        assert r.data["total_matching"] == 5

    def test_empty_result(self, fixture_csv):
        r = query_disasters(fixture_csv, country="Atlantis")
        assert r.ok
        assert r.data["count"] == 0
        assert r.data["rows"] == []

    def test_invalid_file(self, tmp_path):
        r = query_disasters(tmp_path / "nope.csv")
        assert not r.ok
        assert r.error is not None

    def test_response_has_timing(self, fixture_csv):
        r = query_disasters(fixture_csv, country="Japan")
        assert r.meta.timing_ms >= 0

    def test_response_columns_present(self, fixture_csv):
        r = query_disasters(fixture_csv)
        assert "Year" in r.data["columns"]
        assert "Country" in r.data["columns"]
        assert "Disaster Type" in r.data["columns"]
