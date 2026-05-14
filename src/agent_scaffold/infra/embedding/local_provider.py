import hashlib
import struct
from typing import Any


class LocalEmbeddingProvider:
    name = "local"

    def __init__(self, dimension: int = 384) -> None:
        self._dim = dimension

    @property
    def dimension(self) -> int:
        return self._dim

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._hash_embed(text) for text in texts]

    async def embed_query(self, text: str) -> list[float]:
        return self._hash_embed(text)

    def _hash_embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode()).digest()
        repeated = (digest * (self._dim // len(digest) + 1))[:self._dim]
        raw = struct.unpack(f"{self._dim}B", repeated)
        norm = sum(v * v for v in raw) ** 0.5 or 1.0
        return [v / norm for v in raw]
