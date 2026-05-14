from collections import defaultdict


class InMemoryStore:
    def __init__(self) -> None:
        self._data: dict[str, list[str]] = defaultdict(list)

    def append(self, session_id: str, item: str) -> None:
        self._data[session_id].append(item)

    def list(self, session_id: str) -> list[str]:
        return self._data[session_id]
