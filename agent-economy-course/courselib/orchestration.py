"""Minimal observability primitive for economy labs."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Trace:
    """Append-only event log so economic flows are inspectable, not magic."""

    events: list[dict[str, Any]] = field(default_factory=list)

    def emit(self, kind: str, **data: Any) -> None:
        self.events.append({"t": round(time.time(), 6), "kind": kind, **data})

    def of_kind(self, kind: str) -> list[dict[str, Any]]:
        return [e for e in self.events if e["kind"] == kind]

    def __len__(self) -> int:
        return len(self.events)
