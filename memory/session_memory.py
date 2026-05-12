from memory.store import InMemoryStore


class SessionMemory:
    def __init__(self, store: InMemoryStore | None = None) -> None:
        self._store = store or InMemoryStore()

    def add_turn(self, session_id: str, text: str) -> None:
        self._store.append(session_id, text)

    def history(self, session_id: str) -> list[str]:
        return self._store.list(session_id)
