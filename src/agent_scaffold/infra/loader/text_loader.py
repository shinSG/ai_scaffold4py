from pathlib import Path

from agent_scaffold.infra.loader.ports import DocumentLoader, LoadedDocument


class TextLoader(DocumentLoader):
    async def load(self, source: str) -> list[LoadedDocument]:
        path = Path(source)
        if not path.exists():
            return [LoadedDocument(content="", source=source, metadata={"error": "file not found"})]
        content = path.read_text(encoding="utf-8")
        return [LoadedDocument(content=content, source=source, metadata={"file_type": "text", "size": len(content)})]

    async def load_bytes(self, data: bytes, filename: str = "") -> list[LoadedDocument]:
        content = data.decode("utf-8")
        return [LoadedDocument(content=content, source=filename, metadata={"file_type": "text", "size": len(content)})]
