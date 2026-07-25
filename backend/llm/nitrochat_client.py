"""Small client for the model gateway already configured in NitroCloud.

The paired NitroChat deployment keeps the gateway credential server-side. This
backend calls the deployed chat endpoint, so no provider API key is stored in
the ForgeOps repository or sent to the browser.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
import time
from typing import Any

import httpx

from backend.config import (
    FORGEOPS_MODEL,
    HTTP_TIMEOUT_SECONDS,
    LIVE_AGENTS_ENABLED,
    NITROCHAT_CHAT_URL,
)


@dataclass
class LLMCallResult:
    data: dict[str, Any]
    content: str
    latency_ms: int
    model: str
    live: bool
    error: str | None = None


def _parse_json_object(content: str) -> dict[str, Any]:
    text = content.strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    if fenced:
        text = fenced.group(1).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        parsed = json.loads(text[start : end + 1])
        if isinstance(parsed, dict):
            return parsed

    raise ValueError("The model response did not contain a JSON object")


class NitroChatClient:
    """Runs one isolated LLM call for a named agent role."""

    def __init__(
        self,
        endpoint: str = NITROCHAT_CHAT_URL,
        model: str = FORGEOPS_MODEL,
        enabled: bool = LIVE_AGENTS_ENABLED,
        timeout: float = HTTP_TIMEOUT_SECONDS,
    ) -> None:
        self.endpoint = endpoint
        self.model = model
        self.enabled = enabled
        self.timeout = timeout

    def complete_json(
        self,
        *,
        agent: str,
        system_prompt: str,
        payload: dict[str, Any],
    ) -> LLMCallResult:
        if not self.enabled:
            return LLMCallResult(
                data={},
                content="",
                latency_ms=0,
                model=self.model,
                live=False,
                error="Live agents are disabled by FORGEOPS_LIVE_AGENTS",
            )

        start = time.perf_counter()
        try:
            response = httpx.post(
                self.endpoint,
                json={
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                f"For the ForgeOps manufacturing investigation, act as the "
                                f"{agent} Agent. {system_prompt}\n"
                                "Return exactly one valid JSON object (a fenced JSON object is acceptable). "
                                f"Investigation input: {json.dumps(payload, ensure_ascii=False)}"
                            ),
                        },
                    ],
                    "stream": False,
                },
                timeout=self.timeout,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            envelope = response.json()
            content = envelope.get("message", {}).get("content", "")
            if not isinstance(content, str) or not content.strip():
                raise ValueError("NitroChat returned an empty assistant message")

            return LLMCallResult(
                data=_parse_json_object(content),
                content=content,
                latency_ms=round((time.perf_counter() - start) * 1000),
                model=self.model,
                live=True,
            )
        except Exception as exc:
            return LLMCallResult(
                data={},
                content="",
                latency_ms=round((time.perf_counter() - start) * 1000),
                model=self.model,
                live=False,
                error=str(exc),
            )
