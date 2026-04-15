"""Contract tests for the MCP response envelope."""

from src.mcp_server.models import (
    McpResponse,
    McpResponseMeta,
    build_error_response,
    build_success_response,
)


class TestMcpResponseEnvelope:
    def test_success_has_required_fields(self):
        r = build_success_response(data={"rows": []})
        assert r.ok is True
        assert r.data is not None
        assert r.error is None
        assert isinstance(r.meta, McpResponseMeta)

    def test_error_has_required_fields(self):
        r = build_error_response(error="something broke")
        assert r.ok is False
        assert r.data is None
        assert r.error == "something broke"
        assert isinstance(r.meta, McpResponseMeta)

    def test_meta_has_schema_version(self):
        r = build_success_response(data={})
        assert r.meta.schema_version == "1.0"

    def test_meta_has_request_id(self):
        r = build_success_response(data={})
        assert isinstance(r.meta.request_id, str)
        assert len(r.meta.request_id) > 0

    def test_meta_has_timing(self):
        r = build_success_response(data={}, timing_ms=42.5)
        assert r.meta.timing_ms == 42.5

    def test_request_ids_are_unique(self):
        r1 = build_success_response(data={})
        r2 = build_success_response(data={})
        assert r1.meta.request_id != r2.meta.request_id

    def test_serialization_roundtrip(self):
        r = build_success_response(data={"count": 3, "rows": [1, 2, 3]}, timing_ms=1.5)
        d = r.model_dump()
        restored = McpResponse(**d)
        assert restored.ok == r.ok
        assert restored.data == r.data
        assert restored.meta.timing_ms == r.meta.timing_ms

    def test_envelope_invariant_ok_true_no_error(self):
        r = build_success_response(data=[])
        assert r.ok is True
        assert r.error is None

    def test_envelope_invariant_ok_false_has_error(self):
        r = build_error_response(error="fail")
        assert r.ok is False
        assert r.error is not None
        assert len(r.error) > 0
