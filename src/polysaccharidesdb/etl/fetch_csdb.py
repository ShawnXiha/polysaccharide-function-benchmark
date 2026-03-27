"""Fetch a lightweight CSDB export from publication ID ranges."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from polysaccharidesdb.paths import DATA_INTERIM, DATA_RAW


SEARCH_URL = "http://csdb.glycoscience.ru/database/core/search_id.php"
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
    parser = argparse.ArgumentParser(description="Fetch lightweight CSDB publication records")
    parser.add_argument("--start-publication-id", type=int, default=1)
    parser.add_argument("--end-publication-id", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--sleep-seconds", type=float, default=0.15)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=DATA_RAW / "csdb_export.csv",
    )
    parser.add_argument(
        "--raw-jsonl",
        type=Path,
        default=DATA_INTERIM / "csdb_raw_records.jsonl",
    )
    parser.add_argument(
        "--state-json",
        type=Path,
        default=DATA_INTERIM / "csdb_fetch_state.json",
    )
    return parser.parse_args()


def make_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.headers.update(DEFAULT_HEADERS)
    return session


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def extract_publication_dois(soup: BeautifulSoup) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for div in soup.find_all("div", id=re.compile(r"^block\d+$")):
        pub_index = div.get("id", "").replace("block", "")
        text = clean_text(div.get_text(" ", strip=True))
        match = re.search(r"Publication DOI:\s*([^\s]+)", text, flags=re.IGNORECASE)
        if match:
            mapping[pub_index] = match.group(1)
    return mapping


def parse_publication_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    doi_map = extract_publication_dois(soup)
    records: list[dict] = []

    for form in soup.find_all("form", attrs={"action": "search_id.php"}):
        mode_input = form.find("input", attrs={"name": "mode"})
        id_input = form.find("input", attrs={"name": "id_list"})
        if mode_input is None or id_input is None or mode_input.get("value") != "record":
            continue

        form_name = form.get("name", "")
        match = re.match(r"bigrec(\d+)_(\d+)_(\d+)", form_name)
        if not match:
            continue
        csdb_id, pub_index, compound_index = match.groups()

        organism_source = clean_text(form.get_text(" ", strip=True))
        organism_source = organism_source.replace(f"CSDB ID {csdb_id} (all data & tools)", "").strip()

        span = soup.find("span", id=f"sweet{pub_index}_{compound_index}")
        structure_text = ""
        if span is not None:
            structure_cell = span.find("td", attrs={"class": "structure"})
            if structure_cell is not None:
                structure_text = clean_text(structure_cell.get_text(" ", strip=True))

        class_div = soup.find("div", id=f"block{pub_index}_{compound_index}")
        compound_class = ""
        if class_div is not None:
            class_text = clean_text(class_div.get_text(" ", strip=True))
            class_match = re.search(r"Compound class:\s*([^\s].*?)$", class_text, flags=re.IGNORECASE)
            if class_match:
                compound_class = class_match.group(1)

        records.append(
            {
                "source_record_id": csdb_id,
                "publication_index": pub_index,
                "compound_index": compound_index,
                "raw_representation": structure_text,
                "canonical_representation": structure_text,
                "monomer_composition": "",
                "linkage": "",
                "branching": compound_class,
                "modification": "",
                "mw_or_range": "",
                "organism_source": organism_source,
                "function_label": "unknown",
                "evidence_type": "unknown",
                "doi": doi_map.get(pub_index, ""),
                "license": "unknown",
            }
        )

    return records


def write_outputs(records: list[dict], output_csv: Path, raw_jsonl: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in CSV_FIELDS})

    raw_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with raw_jsonl.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    session = make_session()
    all_records: list[dict] = []
    failed_batches: list[dict] = []

    for start in range(args.start_publication_id, args.end_publication_id + 1, args.batch_size):
        end = min(args.end_publication_id, start + args.batch_size - 1)
        try:
            response = session.post(
                SEARCH_URL,
                data={
                    "id_list": f"{start}-{end}",
                    "mode": "publication",
                    "rec_per_page": str(args.batch_size * 4),
                    "start_rec": "1",
                    "sort_by": "ID",
                },
                timeout=args.timeout,
            )
            response.raise_for_status()
            batch_records = parse_publication_page(response.text)
            all_records.extend(batch_records)
            print(f"Fetched publication IDs {start}-{end}: {len(batch_records)} CSDB records")
        except Exception as exc:  # pragma: no cover
            failed_batches.append({"start": start, "end": end, "error": str(exc)})
        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)

    # Deduplicate by CSDB record ID.
    deduped: dict[str, dict] = {}
    for record in all_records:
        deduped[record["source_record_id"]] = record
    records = sorted(deduped.values(), key=lambda item: int(item["source_record_id"]))

    write_outputs(records=records, output_csv=args.output_csv, raw_jsonl=args.raw_jsonl)

    state = {
        "search_url": SEARCH_URL,
        "start_publication_id": args.start_publication_id,
        "end_publication_id": args.end_publication_id,
        "batch_size": args.batch_size,
        "records_saved": len(records),
        "failed_batches": failed_batches,
        "output_csv": str(args.output_csv),
        "raw_jsonl": str(args.raw_jsonl),
    }
    args.state_json.parent.mkdir(parents=True, exist_ok=True)
    with args.state_json.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)

    print(f"Saved {len(records)} normalized CSDB rows to {args.output_csv}")
    print(f"Fetch state saved to {args.state_json}")


if __name__ == "__main__":
    main()
