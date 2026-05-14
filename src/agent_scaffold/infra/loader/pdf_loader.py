from pathlib import Path

from agent_scaffold.infra.loader.ports import DocumentLoader, LoadedDocument


class PDFLoader(DocumentLoader):
    async def load(self, source: str) -> list[LoadedDocument]:
        path = Path(source)
        if not path.exists():
            return [LoadedDocument(content="", source=source, metadata={"error": "file not found"})]

        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            documents = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                documents.append(LoadedDocument(
                    content=text,
                    source=source,
                    metadata={"file_type": "pdf", "page": i + 1, "total_pages": len(reader.pages)},
                ))
            return documents
        except ImportError:
            return [LoadedDocument(content="", source=source, metadata={"error": "pypdf not installed"})]

    async def load_bytes(self, data: bytes, filename: str = "") -> list[LoadedDocument]:
        import io
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(data))
            documents = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                documents.append(LoadedDocument(
                    content=text,
                    source=filename,
                    metadata={"file_type": "pdf", "page": i + 1, "total_pages": len(reader.pages)},
                ))
            return documents
        except ImportError:
            return [LoadedDocument(content="", source=filename, metadata={"error": "pypdf not installed"})]
