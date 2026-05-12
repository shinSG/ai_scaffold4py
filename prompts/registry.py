class PromptRegistry:
    def __init__(self) -> None:
        self._mapping: dict[str, str] = {"default_system": "default_system"}

    def get(self, key: str) -> str:
        return self._mapping[key]
