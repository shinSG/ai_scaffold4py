from agent_scaffold.memory.store import InMemoryStore


class LongTermMemory:
    def __init__(self, store: InMemoryStore | None = None) -> None:
        self._store = store or InMemoryStore()

    def save(self, namespace: str, value: str) -> None:
        self._store.append(namespace, value)

    def query(self, namespace: str) -> list[str]:
        return self._store.list(namespace)
