from pathlib import Path

from agent_scaffold.infra.loader.ports import DocumentLoader


def get_document_loader(source: str) -> DocumentLoader:
    lower = source.lower()
    if lower.endswith(".pdf"):
        from agent_scaffold.infra.loader.pdf_loader import PDFLoader
        return PDFLoader()
    if lower.startswith("http://") or lower.startswith("https://"):
        from agent_scaffold.infra.loader.web_loader import WebLoader
        return WebLoader()
    from agent_scaffold.infra.loader.text_loader import TextLoader
    return TextLoader()


def get_loader_by_type(file_type: str) -> DocumentLoader:
    if file_type == "pdf":
        from agent_scaffold.infra.loader.pdf_loader import PDFLoader
        return PDFLoader()
    if file_type == "web":
        from agent_scaffold.infra.loader.web_loader import WebLoader
        return WebLoader()
    from agent_scaffold.infra.loader.text_loader import TextLoader
    return TextLoader()
