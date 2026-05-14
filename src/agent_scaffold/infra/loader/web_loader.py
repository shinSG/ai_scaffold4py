import httpx

from agent_scaffold.infra.loader.ports import DocumentLoader, LoadedDocument


class WebLoader(DocumentLoader):
    async def load(self, source: str) -> list[LoadedDocument]:
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(source)
                response.raise_for_status()
            content = self._extract_text(response.text)
            return [LoadedDocument(
                content=content,
                source=source,
                metadata={"file_type": "web", "status_code": response.status_code, "content_type": response.headers.get("content-type", "")},
            )]
        except Exception as e:
            return [LoadedDocument(content="", source=source, metadata={"error": str(e)})]

    async def load_bytes(self, data: bytes, filename: str = "") -> list[LoadedDocument]:
        content = data.decode("utf-8")
        return [LoadedDocument(content=content, source=filename, metadata={"file_type": "web"})]

    @staticmethod
    def _extract_text(html: str) -> str:
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            return soup.get_text(separator="\n", strip=True)
        except ImportError:
            import re
            text = re.sub(r"<[^>]+>", " ", html)
            return re.sub(r"\s+", " ", text).strip()
