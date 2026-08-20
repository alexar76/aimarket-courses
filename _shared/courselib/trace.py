"""Minimal execution trace for course labs (M-observability pattern)."""

from __future__ import annotations

from typing import Any


class Trace:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def __len__(self) -> int:
        return len(self.events)

    def log(self, kind: str, **fields: Any) -> None:
        self.events.append({"kind": kind, **fields})

    def of_kind(self, kind: str) -> list[dict[str, Any]]:
        return [e for e in self.events if e.get("kind") == kind]
