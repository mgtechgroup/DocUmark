def convert(file_path: str) -> str:
    from html.parser import HTMLParser

    with open(file_path, encoding="utf-8", errors="replace") as f:
        html = f.read()

    class _Extractor(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.parts: list[str] = []
            self._skip = False

        def handle_starttag(self, tag: str, attrs: list) -> None:
            if tag in ("script", "style"):
                self._skip = True

        def handle_endtag(self, tag: str) -> None:
            if tag in ("script", "style"):
                self._skip = False

        def handle_data(self, data: str) -> None:
            if not self._skip:
                stripped = data.strip()
                if stripped:
                    self.parts.append(stripped)

    extractor = _Extractor()
    extractor.feed(html)
    text = "\n\n".join(extractor.parts)
    return f"# Document\n\n{text}"
