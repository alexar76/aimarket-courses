"""Tiny event log printed by every lab — same idea as sibling courses."""

from __future__ import annotations

from typing import Any


class Trace:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def log(self, kind: str, **fields: Any) -> None:
        self.events.append({"kind": kind, **fields})

    def emit(self, kind: str, **fields: Any) -> None:
        self.log(kind, **fields)

    def __len__(self) -> int:
        return len(self.events)
