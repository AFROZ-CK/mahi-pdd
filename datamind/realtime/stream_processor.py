"""In-memory stream processor for near real-time event analytics."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque


@dataclass
class StreamProcessor:
    """Maintain a bounded queue and aggregate recent event payloads."""

    max_events: int = 100
    _events: Deque[dict] = field(default_factory=deque)

    def ingest(self, event: dict) -> dict:
        """Ingest one event and return stream stats."""
        self._events.append(event)
        while len(self._events) > self.max_events:
            self._events.popleft()

        numeric_values = [v for item in self._events for v in item.values() if isinstance(v, (int, float))]
        average = float(sum(numeric_values) / len(numeric_values)) if numeric_values else 0.0
        return {"events_in_window": len(self._events), "numeric_average": average}
