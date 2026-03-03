from __future__ import annotations

from pathlib import Path

from collatz.literature import (
    BibEntry,
    bib_entry_to_zotero_item,
    candidate_pdf_urls,
    download_first_pdf,
    parse_bibtex_entries,
    validate_entry,
)


def test_parse_bibtex_entries_extracts_core_fields():
    text = """
@article{Lagarias1985Collatz,
  author = {Lagarias, Jeffrey C.},
  title = {The 3x+1 problem and its generalizations},
  year = {1985},
  doi = {10.1080/00029890.1985.11971450},
  url = {https://example.org/paper.pdf},
}
"""
    entries = parse_bibtex_entries(text)
    assert len(entries) == 1
    entry = entries[0]
    assert entry.key == "Lagarias1985Collatz"
    assert entry.fields["doi"] == "10.1080/00029890.1985.11971450"
    assert entry.fields["url"] == "https://example.org/paper.pdf"


def test_validate_entry_doi_success():
    entry = BibEntry(
        entry_type="article",
        key="TestKey",
        fields={"doi": "10.1000/example", "title": "My Title"},
    )

    def fake_fetch(url: str, headers: dict[str, str] | None) -> dict[str, object]:
        assert "10.1000%2Fexample" in url
        assert headers is not None
        return {"message": {"title": ["Resolved Title"]}}

    result = validate_entry(entry, fetch_json=fake_fetch)
    assert result.status == "ok"
    assert result.reason == "doi_resolved"
    assert result.matched_title == "Resolved Title"


def test_candidate_pdf_urls_combines_sources():
    entry = BibEntry(
        entry_type="article",
        key="ArxivKey",
        fields={
            "eprint": "2401.12345",
            "doi": "10.1000/example",
            "url": "https://publisher.org/main.pdf",
        },
    )

    def fake_fetch(url: str, headers: dict[str, str] | None) -> dict[str, object]:
        assert "crossref" in url
        return {
            "message": {
                "link": [
                    {"content-type": "application/pdf", "URL": "https://cdn.publisher.org/article.pdf"},
                    {"content-type": "text/html", "URL": "https://publisher.org/article"},
                ]
            }
        }

    urls = candidate_pdf_urls(entry, fetch_json=fake_fetch)
    assert "https://publisher.org/main.pdf" in urls
    assert "https://arxiv.org/pdf/2401.12345.pdf" in urls
    assert "https://cdn.publisher.org/article.pdf" in urls


def test_download_first_pdf_writes_output():
    entry = BibEntry(entry_type="article", key="Key", fields={"url": "https://example.org/file.pdf"})

    def fake_binary(url: str, headers: dict[str, str] | None) -> bytes:
        assert url.endswith(".pdf")
        return b"%PDF-1.7\\nmock"

    def fake_json(url: str, headers: dict[str, str] | None) -> dict[str, object]:
        return {}

    tmp_path = Path("analysis/results/test_literature_downloads")
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = download_first_pdf(entry, output_dir=tmp_path, fetch_binary=fake_binary, fetch_json=fake_json)
    assert path is not None
    assert path.exists()
    assert path.read_bytes().startswith(b"%PDF")


def test_bib_entry_to_zotero_item_maps_authors():
    entry = BibEntry(
        entry_type="article",
        key="Smith2020Thing",
        fields={
            "title": "A Thing",
            "author": "Smith, Alice and Bob Jones",
            "year": "2020",
            "doi": "10.1000/demo",
        },
    )
    item = bib_entry_to_zotero_item(entry)
    assert item["itemType"] == "journalArticle"
    assert item["title"] == "A Thing"
    assert item["DOI"] == "10.1000/demo"
    assert len(item["creators"]) == 2
    assert item["creators"][0]["lastName"] == "Smith"
