"""Integration test: MCP server processes query correctly end-to-end."""

from src.mcp_server.server import query_natural_disasters


class TestMcpEndToEnd:
    def test_query_with_filters(self):
        result = query_natural_disasters(country="Japan", disaster_type="Earthquake")
        assert result["ok"] is True
        assert result["data"]["total_matching"] > 0
        for row in result["data"]["rows"]:
            assert "Japan" in row["Country"]
            assert "Earthquake" in row["Disaster Type"]

    def test_query_with_year_range(self):
        result = query_natural_disasters(year_start=2000, year_end=2010)
        assert result["ok"] is True
        for row in result["data"]["rows"]:
            assert 2000 <= row["Year"] <= 2010

    def test_empty_result_still_ok(self):
        result = query_natural_disasters(country="Atlantis")
        assert result["ok"] is True
        assert result["data"]["count"] == 0

    def test_response_envelope_complete(self):
        result = query_natural_disasters(year=2010)
        assert "ok" in result
        assert "data" in result
        assert "meta" in result
        assert result["meta"]["schema_version"] == "1.0"
        assert len(result["meta"]["request_id"]) > 0
        assert result["meta"]["timing_ms"] >= 0
