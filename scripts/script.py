#!/usr/bin/env python3
"""Simple, dependency-free CSV cleaner.

Usage:
  python scripts/script.py --input examples/raw.csv --output outputs/clean.csv --dedup-cols user_id date

What it does:
  1) Trim whitespace on all string fields
  2) Normalize missing values: "", "NA", "N/A" -> empty
  3) Attempt to coerce 'qty' to int, 'price' to float; invalids -> empty
  4) Drop duplicates (entire row or by given columns)
  5) Drop columns that are entirely empty after cleaning
"""
import argparse, csv, sys, os
from typing import List, Dict

MISSING_TOKENS = {"", "NA", "N/A", "na", "n/a", "Na", "None"}

def parse_args():
    p = argparse.ArgumentParser(description="CSV cleaner (no external deps)")
    p.add_argument("--input", required=True, help="Path to raw CSV")
    p.add_argument("--output", required=True, help="Path to cleaned CSV")
    p.add_argument("--dedup-cols", nargs="*", default=None, help="Columns to consider for deduplication")
    return p.parse_args()

def normalize_value(v: str) -> str:
    if v is None:
        return ""
    v = v.strip()
    return "" if v in MISSING_TOKENS else v

def try_int(v: str):
    try:
        return str(int(v))
    except:
        return ""

def try_float(v: str):
    try:
        # normalize to standard decimal string without extra spaces
        return str(float(v))
    except:
        return ""

def clean_row(row: Dict[str,str]) -> Dict[str,str]:
    cleaned = {k: normalize_value(row.get(k, "")) for k in row.keys()}
    # Example type coercions; extend for your schema
    if "qty" in cleaned and cleaned["qty"]:
        cleaned["qty"] = try_int(cleaned["qty"])
    if "price" in cleaned and cleaned["price"]:
        cleaned["price"] = try_float(cleaned["price"])
    return cleaned

def drop_empty_columns(rows: List[Dict[str,str]]) -> List[Dict[str,str]]:
    if not rows:
        return rows
    keys = list(rows[0].keys())
    non_empty_keys = []
    for k in keys:
        any_non_empty = any(r.get(k, "") != "" for r in rows)
        if any_non_empty:
            non_empty_keys.append(k)
    # Rebuild rows with only non-empty columns
    pruned = [{k: r.get(k, "") for k in non_empty_keys} for r in rows]
    return pruned

def deduplicate(rows: List[Dict[str,str]], cols: List[str] | None) -> List[Dict[str,str]]:
    seen = set()
    out = []
    for r in rows:
        key = tuple(r[c] for c in cols) if cols else tuple(r.values())
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out

def main():
    args = parse_args()
    # Read
    try:
        with open(args.input, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            raw_rows = list(reader)
    except Exception as e:
        print(f"[ERROR] failed to read {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    # Clean
    cleaned = [clean_row(r) for r in raw_rows]
    cleaned = deduplicate(cleaned, args.dedup_cols)
    cleaned = drop_empty_columns(cleaned)

    # Ensure output dir
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Write
    if cleaned:
        fieldnames = list(cleaned[0].keys())
    else:
        fieldnames = []
    try:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in cleaned:
                writer.writerow(r)
    except Exception as e:
        print(f"[ERROR] failed to write {args.output}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Saved {args.output} | rows={len(cleaned)} | cols={len(fieldnames)}")

if __name__ == "__main__":
    main()
