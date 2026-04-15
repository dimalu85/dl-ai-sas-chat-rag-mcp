"""Pydantic response models for the MCP server."""

import time
import uuid
from typing import Any

from pydantic import BaseModel, Field


class McpResponseMeta(BaseModel):
    """Metadata attached to every MCP response."""

    schema_version: str = "1.0"
    request_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    timing_ms: float = 0.0


class McpResponse(BaseModel):
    """Standardised envelope for all MCP tool responses."""

    ok: bool
    data: Any = None
    error: str | None = None
    meta: McpResponseMeta = Field(default_factory=McpResponseMeta)


def build_success_response(
    data: Any,
    timing_ms: float = 0.0,
    request_id: str | None = None,
) -> McpResponse:
    """Create a successful MCP response envelope."""
    meta = McpResponseMeta(
        timing_ms=timing_ms,
        **({"request_id": request_id} if request_id else {}),
    )
    return McpResponse(ok=True, data=data, meta=meta)


def build_error_response(
    error: str,
    timing_ms: float = 0.0,
    request_id: str | None = None,
) -> McpResponse:
    """Create an error MCP response envelope."""
    meta = McpResponseMeta(
        timing_ms=timing_ms,
        **({"request_id": request_id} if request_id else {}),
    )
    return McpResponse(ok=False, error=error, meta=meta)
