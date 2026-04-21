import pytest

from app.application.services.pdf_service import PDFService


class FakePage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class FakeReader:
    def __init__(self, _stream):
        self.pages = [
            FakePage("First page"),
            FakePage(None),
            FakePage("Second page"),
        ]


def test_extract_text_returns_expected_pdf_data(monkeypatch):
    monkeypatch.setattr(
        "app.application.services.pdf_service.PdfReader",
        FakeReader,
    )

    result = PDFService().extract_text(b"%PDF-test", "sample.pdf")

    assert result.filename == "sample.pdf"
    assert result.text == "First page\n\nSecond page"
    assert result.page_count == 3
    assert result.character_count == len("First page\n\nSecond page")


def test_extract_text_raises_value_error_for_invalid_pdf(monkeypatch):
    def broken_reader(_stream):
        raise RuntimeError("cannot read")

    monkeypatch.setattr(
        "app.application.services.pdf_service.PdfReader",
        broken_reader,
    )

    with pytest.raises(ValueError, match="Invalid PDF"):
        PDFService().extract_text(b"not-a-pdf", "invalid.pdf")
