import pytest

from agent_scaffold.infra.loader.text_loader import TextLoader
from agent_scaffold.infra.loader.factory import get_loader_by_type


@pytest.mark.asyncio
async def test_text_loader_load_bytes() -> None:
    loader = TextLoader()
    docs = await loader.load_bytes(b"hello world", filename="test.txt")
    assert len(docs) == 1
    assert docs[0].content == "hello world"
    assert docs[0].source == "test.txt"
    assert docs[0].metadata["file_type"] == "text"


@pytest.mark.asyncio
async def test_text_loader_load_missing_file() -> None:
    loader = TextLoader()
    docs = await loader.load("/nonexistent/file.txt")
    assert len(docs) == 1
    assert "error" in docs[0].metadata


def test_get_loader_by_type_text() -> None:
    loader = get_loader_by_type("text")
    assert isinstance(loader, TextLoader)


def test_get_loader_by_type_pdf() -> None:
    loader = get_loader_by_type("pdf")
    assert type(loader).__name__ == "PDFLoader"


def test_get_loader_by_type_web() -> None:
    loader = get_loader_by_type("web")
    assert type(loader).__name__ == "WebLoader"
