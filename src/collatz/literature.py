from __future__ import annotations

import json
import re
import secrets
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


JsonFetcher = Callable[[str, dict[str, str] | None], dict[str, Any]]
BinaryFetcher = Callable[[str, dict[str, str] | None], bytes]


@dataclass(frozen=True)
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]


@dataclass(frozen=True)
class ValidationResult:
    key: str
    status: str
    reason: str
    doi: str | None
    title: str | None
    matched_title: str | None


def _clean_bib_value(raw: str) -> str:
    value = raw.strip()
    if value.endswith(","):
        value = value[:-1].rstrip()
    if value.startswith("{") and value.endswith("}"):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return re.sub(r"\s+", " ", value).strip()


def parse_bibtex_entries(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []
    entry_re = re.compile(
        r"@(?P<entry_type>[a-zA-Z]+)\s*\{\s*(?P<key>[^,\s]+)\s*,(?P<body>.*?)\n\}",
        flags=re.DOTALL,
    )
    field_re = re.compile(
        r"(?P<name>[a-zA-Z][a-zA-Z0-9_-]*)\s*=\s*(?P<value>\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\"(?:\\.|[^\"])*\"|[^,\n]+)\s*,?",
        flags=re.DOTALL,
    )
    for match in entry_re.finditer(text):
        body = match.group("body")
        fields: dict[str, str] = {}
        for field_match in field_re.finditer(body):
            name = field_match.group("name").lower()
            value = _clean_bib_value(field_match.group("value"))
            fields[name] = value
        entries.append(
            BibEntry(
                entry_type=match.group("entry_type").lower(),
                key=match.group("key"),
                fields=fields,
            )
        )
    return entries


def _fetch_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def _fetch_binary(url: str, headers: dict[str, str] | None = None) -> bytes:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def _extract_arxiv_id(entry: BibEntry) -> str | None:
    eprint = entry.fields.get("eprint")
    if eprint:
        return eprint.replace("arXiv:", "").strip()
    url = entry.fields.get("url", "")
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([^/?#]+)", url, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).removesuffix(".pdf")


def validate_entry(entry: BibEntry, fetch_json: JsonFetcher = _fetch_json) -> ValidationResult:
    doi = entry.fields.get("doi")
    title = entry.fields.get("title")
    if doi:
        doi_url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
        try:
            response = fetch_json(doi_url, {"User-Agent": "collatz-lab-literature-sync/1.0"})
            message = response.get("message", {})
            matched_title = None
            titles = message.get("title", [])
            if isinstance(titles, list) and titles:
                matched_title = str(titles[0])
            return ValidationResult(
                key=entry.key,
                status="ok",
                reason="doi_resolved",
                doi=doi,
                title=title,
                matched_title=matched_title,
            )
        except Exception as exc:  # pragma: no cover - network failures are environment-specific
            return ValidationResult(
                key=entry.key,
                status="error",
                reason=f"doi_lookup_failed:{exc.__class__.__name__}",
                doi=doi,
                title=title,
                matched_title=None,
            )
    arxiv_id = _extract_arxiv_id(entry)
    if arxiv_id:
        return ValidationResult(
            key=entry.key,
            status="ok",
            reason="arxiv_id_present",
            doi=None,
            title=title,
            matched_title=title,
        )
    return ValidationResult(
        key=entry.key,
        status="warning",
        reason="missing_identifier",
        doi=None,
        title=title,
        matched_title=None,
    )


def _normalize_pdf_url(url: str) -> str | None:
    candidate = url.strip()
    if not candidate:
        return None
    if candidate.lower().endswith(".pdf"):
        return candidate
    return None


def candidate_pdf_urls(
    entry: BibEntry,
    fetch_json: JsonFetcher = _fetch_json,
) -> list[str]:
    urls: list[str] = []
    direct_url = entry.fields.get("url", "")
    normalized = _normalize_pdf_url(direct_url)
    if normalized:
        urls.append(normalized)

    arxiv_id = _extract_arxiv_id(entry)
    if arxiv_id:
        urls.append(f"https://arxiv.org/pdf/{arxiv_id}.pdf")

    doi = entry.fields.get("doi")
    if doi:
        doi_url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
        try:
            response = fetch_json(doi_url, {"User-Agent": "collatz-lab-literature-sync/1.0"})
            links = response.get("message", {}).get("link", [])
            if isinstance(links, list):
                for link_info in links:
                    if not isinstance(link_info, dict):
                        continue
                    if link_info.get("content-type") == "application/pdf":
                        link_url = str(link_info.get("URL", "")).strip()
                        if link_url:
                            urls.append(link_url)
        except Exception:  # pragma: no cover
            pass

    deduped: list[str] = []
    seen: set[str] = set()
    for url in urls:
        if url not in seen:
            deduped.append(url)
            seen.add(url)
    return deduped


def download_first_pdf(
    entry: BibEntry,
    output_dir: Path,
    fetch_binary: BinaryFetcher = _fetch_binary,
    fetch_json: JsonFetcher = _fetch_json,
) -> Path | None:
    output_dir.mkdir(parents=True, exist_ok=True)
    urls = candidate_pdf_urls(entry, fetch_json=fetch_json)
    for idx, url in enumerate(urls):
        try:
            content = fetch_binary(url, {"User-Agent": "collatz-lab-literature-sync/1.0"})
            if not content.startswith(b"%PDF"):
                continue
            suffix = "" if idx == 0 else f"_{idx}"
            destination = output_dir / f"{entry.key}{suffix}.pdf"
            destination.write_bytes(content)
            return destination
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError:
            continue
    return None


def _split_authors(raw: str) -> list[dict[str, str]]:
    authors = [part.strip() for part in raw.split(" and ") if part.strip()]
    creators: list[dict[str, str]] = []
    for author in authors:
        if "," in author:
            last, first = [chunk.strip() for chunk in author.split(",", 1)]
        else:
            parts = author.split()
            if len(parts) == 1:
                first, last = "", parts[0]
            else:
                first = " ".join(parts[:-1])
                last = parts[-1]
        creators.append({"creatorType": "author", "firstName": first, "lastName": last})
    return creators


def bib_entry_to_zotero_item(entry: BibEntry) -> dict[str, Any]:
    item: dict[str, Any] = {
        "itemType": "journalArticle",
        "title": entry.fields.get("title", ""),
        "creators": _split_authors(entry.fields.get("author", "")),
        "date": entry.fields.get("year", ""),
        "DOI": entry.fields.get("doi", ""),
        "url": entry.fields.get("url", ""),
        "extra": f"Citation Key: {entry.key}",
    }
    if "journal" in entry.fields:
        item["publicationTitle"] = entry.fields["journal"]
    if "booktitle" in entry.fields and not item.get("publicationTitle"):
        item["publicationTitle"] = entry.fields["booktitle"]
    return item


class ZoteroClient:
    def __init__(self, user_id: str, api_key: str, fetch_json: JsonFetcher = _fetch_json) -> None:
        self.user_id = user_id
        self.api_key = api_key
        self.fetch_json = fetch_json
        self.base_url = "https://api.zotero.org"

    def _request(
        self,
        path: str,
        method: str = "GET",
        payload: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {
            "Zotero-API-Key": self.api_key,
            "User-Agent": "collatz-lab-literature-sync/1.0",
        }
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            headers["Zotero-Write-Token"] = secrets.token_hex(16)
            data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, method=method, headers=headers, data=data)
        with urllib.request.urlopen(request, timeout=45) as response:
            body = response.read().decode("utf-8")
        if not body:
            return {}
        return json.loads(body)

    def get_groups(self) -> list[dict[str, Any]]:
        response = self._request(f"/users/{self.user_id}/groups")
        if isinstance(response, list):
            return response
        return []

    def find_group_id_by_name(self, group_name: str) -> str | None:
        for group in self.get_groups():
            data = group.get("data", {})
            name = str(data.get("name", "")).strip()
            if name.lower() == group_name.strip().lower():
                return str(group.get("id", ""))
        return None

    def create_collection(self, group_id: str, name: str) -> dict[str, Any]:
        return self._request(f"/groups/{group_id}/collections", method="POST", payload=[{"name": name}])

    def create_items(self, group_id: str, items: list[dict[str, Any]]) -> dict[str, Any]:
        return self._request(f"/groups/{group_id}/items", method="POST", payload=items)


def write_knowledge_note(entry: BibEntry, validation: ValidationResult, pdf_path: Path | None, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    note_path = output_dir / f"{entry.key}.md"
    doi = entry.fields.get("doi", "")
    lines = [
        f"# {entry.key}",
        "",
        f"- Title: {entry.fields.get('title', '(missing)')}",
        f"- DOI: {doi or '(none)'}",
        f"- URL: {entry.fields.get('url', '(none)')}",
        f"- Validation: {validation.status} ({validation.reason})",
        f"- PDF: {str(pdf_path) if pdf_path else '(not found)'}",
        "",
        "## Tags",
        "- TODO",
        "",
        "## Summary",
        "TODO",
        "",
        "## Relevance",
        "- TODO",
        "",
        "## Where Cited",
        "- paper/sections/related_work.tex",
    ]
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return note_path
