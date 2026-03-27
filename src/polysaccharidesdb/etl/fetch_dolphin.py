"""Fetch and normalize DoLPHiN records from the public website."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from polysaccharidesdb.paths import DATA_INTERIM, DATA_RAW


BASE_URL = "http://www.dolphindatabase.net"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}
CSV_FIELDS = [
    "source_record_id",
    "raw_representation",
    "canonical_representation",
    "monomer_composition",
    "linkage",
    "branching",
    "modification",
    "mw_or_range",
    "organism_source",
    "function_label",
    "evidence_type",
    "doi",
    "license",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch DoLPHiN website records")
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=DATA_RAW / "dolphin_export.csv",
        help="Normalized CSV export path",
    )
    parser.add_argument(
        "--raw-jsonl",
        type=Path,
        default=DATA_INTERIM / "dolphin_raw_records.jsonl",
        help="Raw parsed record dump path",
    )
    parser.add_argument(
        "--state-json",
        type=Path,
        default=DATA_INTERIM / "dolphin_fetch_state.json",
        help="Crawler state summary path",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Number of rows requested per index page",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="1-based start page",
    )
    parser.add_argument(
        "--end-page",
        type=int,
        default=0,
        help="1-based inclusive end page, 0 means infer from total items",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=0,
        help="Maximum number of detail records to fetch, 0 means no limit",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.15,
        help="Delay between detail requests",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds",
    )
    return parser.parse_args()


def make_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.headers.update(DEFAULT_HEADERS)
    return session


def fetch_html(session: requests.Session, url: str, timeout: float) -> str:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_total_items(index_html: str) -> int | None:
    match = re.search(r"total\s+(\d+)\s+items", index_html, flags=re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1))


def parse_detail_ids(index_html: str) -> list[str]:
    ids = re.findall(r'href="/detail/(\d+)"', index_html)
    return sorted(set(ids), key=int)


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    return value


def split_functions(value: str) -> list[str]:
    text = clean_text(value).lower()
    if not text or text == "unknown":
        return ["unknown"]
    parts = re.split(r"[;,/|]+", text)
    return [part.strip().replace(" ", "_") for part in parts if part.strip()]


def extract_nested_pairs(cell) -> list[list[str]]:
    pairs: list[list[str]] = []
    for row in cell.find_all("tr"):
        values = [
            clean_text(item.get_text(" ", strip=True))
            for item in row.find_all(["th", "td"], recursive=False)
        ]
        values = [value for value in values if value]
        if values:
            pairs.append(values)
    return pairs


def parse_detail_record(detail_id: str, detail_html: str) -> dict:
    soup = BeautifulSoup(detail_html, "html.parser")
    info_table = None
    for table in soup.find_all("table"):
        table_text = clean_text(table.get_text(" ", strip=True)).lower()
        if "polysaccharide" in table_text and "source name" in table_text and "doi" in table_text:
            info_table = table
            break
    if info_table is None:
        raise ValueError(f"Unable to find detail info table for {detail_id}")

    fields: dict[str, str] = {}
    nested: dict[str, list[list[str]]] = {}
    for row in info_table.find_all("tr", recursive=False):
        cells = row.find_all(["th", "td"], recursive=False)
        if len(cells) < 2:
            continue
        key = clean_text(cells[0].get_text(" ", strip=True))
        value = clean_text(cells[1].get_text(" ", strip=True))
        fields[key] = value
        nested[key] = extract_nested_pairs(cells[1])

    monosaccharide_pairs = [
        pair for pair in nested.get("Monosaccharide", []) if len(pair) >= 2
    ]
    monomer_composition = "; ".join(
        f"{pair[0]} {pair[1]}" for pair in monosaccharide_pairs
    )

    glycosidic_pairs = [
        pair[0] for pair in nested.get("Main Glycosidic Bond(s)", []) if pair
    ]
    linkage = "; ".join(glycosidic_pairs) if glycosidic_pairs else fields.get(
        "Main Glycosidic Bond(s)", ""
    )

    raw_representation_parts = [
        fields.get("Polysaccharide", ""),
        linkage,
        fields.get("Main Chain", ""),
        fields.get("Side Chain", ""),
        monomer_composition,
    ]
    raw_representation = " | ".join(
        part for part in raw_representation_parts if clean_text(part)
    )

    physiological_functions = split_functions(fields.get("Physiological Functions", ""))
    if fields.get("Intestinal Microbiota Regulation", "").lower() == "yes":
        if "microbiota_regulation" not in physiological_functions:
            physiological_functions.append("microbiota_regulation")

    return {
        "source_record_id": detail_id,
        "detail_url": f"{BASE_URL}/detail/{detail_id}",
        "polysaccharide_name": fields.get("Polysaccharide", ""),
        "source_name": fields.get("Source Name", ""),
        "weight": fields.get("Weight", ""),
        "main_chain": fields.get("Main Chain", ""),
        "side_chain": fields.get("Side Chain", ""),
        "nmr_information": fields.get("NMR Information", ""),
        "physiological_functions": physiological_functions,
        "intestinal_microbiota_regulation": fields.get(
            "Intestinal Microbiota Regulation", ""
        ),
        "related_diseases": fields.get("Related Diseases (based on ICD-11)", ""),
        "doi": fields.get("DOI", ""),
        "main_glycosidic_bonds": glycosidic_pairs,
        "monosaccharide_pairs": monosaccharide_pairs,
        "normalized_export_row": {
            "source_record_id": detail_id,
            "raw_representation": raw_representation,
            "canonical_representation": raw_representation,
            "monomer_composition": monomer_composition,
            "linkage": linkage,
            "branching": fields.get("Side Chain", ""),
            "modification": "",
            "mw_or_range": fields.get("Weight", ""),
            "organism_source": fields.get("Source Name", ""),
            "function_label": ";".join(physiological_functions),
            "evidence_type": "unknown",
            "doi": fields.get("DOI", ""),
            "license": "unknown",
        },
    }


def write_outputs(
    normalized_rows: list[dict],
    raw_records: list[dict],
    output_csv: Path,
    raw_jsonl: Path,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(normalized_rows)

    raw_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with raw_jsonl.open("w", encoding="utf-8") as handle:
        for record in raw_records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    session = make_session()

    first_index_html = fetch_html(
        session=session,
        url=f"{BASE_URL}/index?page={args.start_page}&page_size={args.page_size}",
        timeout=args.timeout,
    )
    total_items = parse_total_items(first_index_html)
    inferred_end_page = (
        math.ceil(total_items / args.page_size) if total_items is not None else args.start_page
    )
    end_page = args.end_page if args.end_page > 0 else inferred_end_page

    detail_ids: list[str] = []
    seen_ids: set[str] = set()
    failed_pages: list[dict] = []

    for page in range(args.start_page, end_page + 1):
        try:
            html = (
                first_index_html
                if page == args.start_page
                else fetch_html(
                    session=session,
                    url=f"{BASE_URL}/index?page={page}&page_size={args.page_size}",
                    timeout=args.timeout,
                )
            )
            for detail_id in parse_detail_ids(html):
                if detail_id not in seen_ids:
                    seen_ids.add(detail_id)
                    detail_ids.append(detail_id)
                if args.max_records > 0 and len(detail_ids) >= args.max_records:
                    break
            if args.max_records > 0 and len(detail_ids) >= args.max_records:
                break
        except Exception as exc:  # pragma: no cover
            failed_pages.append({"page": page, "error": str(exc)})

    raw_records: list[dict] = []
    normalized_rows: list[dict] = []
    failed_details: list[dict] = []

    for index, detail_id in enumerate(detail_ids, start=1):
        try:
            detail_html = fetch_html(
                session=session,
                url=f"{BASE_URL}/detail/{detail_id}",
                timeout=args.timeout,
            )
            record = parse_detail_record(detail_id=detail_id, detail_html=detail_html)
            raw_records.append(record)
            normalized_rows.append(record["normalized_export_row"])
            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)
        except Exception as exc:  # pragma: no cover
            failed_details.append({"detail_id": detail_id, "error": str(exc)})
        if index % 50 == 0 or index == len(detail_ids):
            print(f"Fetched {index}/{len(detail_ids)} DoLPHiN detail pages")

    write_outputs(
        normalized_rows=normalized_rows,
        raw_records=raw_records,
        output_csv=args.output_csv,
        raw_jsonl=args.raw_jsonl,
    )

    state = {
        "base_url": BASE_URL,
        "start_page": args.start_page,
        "end_page": end_page,
        "page_size": args.page_size,
        "max_records": args.max_records,
        "total_items_reported": total_items,
        "detail_ids_discovered": len(detail_ids),
        "records_saved": len(normalized_rows),
        "failed_pages": failed_pages,
        "failed_details": failed_details,
        "output_csv": str(args.output_csv),
        "raw_jsonl": str(args.raw_jsonl),
    }
    args.state_json.parent.mkdir(parents=True, exist_ok=True)
    with args.state_json.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)

    print(f"Saved {len(normalized_rows)} normalized DoLPHiN rows to {args.output_csv}")
    print(f"Saved {len(raw_records)} raw parsed DoLPHiN rows to {args.raw_jsonl}")
    print(f"Fetch state saved to {args.state_json}")


if __name__ == "__main__":
    main()
