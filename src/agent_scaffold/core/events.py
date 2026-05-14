from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Event:
    name: str
    data: dict[str, Any] = field(default_factory=dict)
    source: str = ""


class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Any]] = {}

    def on(self, event_name: str, callback: Any) -> None:
        self._listeners.setdefault(event_name, []).append(callback)

    def off(self, event_name: str, callback: Any) -> None:
        if event_name in self._listeners:
            self._listeners[event_name] = [cb for cb in self._listeners[event_name] if cb is not callback]

    async def emit(self, event: Event) -> None:
        for callback in self._listeners.get(event.name, []):
            if callable(callback):
                result = callback(event)
                if hasattr(result, "__await__"):
                    await result

    def clear(self) -> None:
        self._listeners.clear()


event_bus = EventBus()
