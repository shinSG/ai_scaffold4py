from pathlib import Path


class PromptLoader:
    def __init__(self, base_dir: str = "prompts/templates") -> None:
        self._base_dir = Path(base_dir)

    def load(self, name: str) -> str:
        prompt_path = self._base_dir / f"{name}.prompt"
        return prompt_path.read_text(encoding="utf-8")
