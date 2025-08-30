#!/usr/bin/env python3
import json
from pathlib import Path

# ====== CONFIG ======
in_path = Path("../../sampleData/user_past_reviews.jsonl")    # input json file
out_path = Path("../../sampleData/unique_gmap_ids.jsonl")    # output path
# ====================

unique_gmap_ids = set()

with in_path.open("r", encoding="utf-8") as fin:
    for lineno, line in enumerate(fin, 1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Skipping line {lineno}: JSON decode error -> {e}")
            continue

        gmap_id = record.get("gmap_id")
        if gmap_id:
            unique_gmap_ids.add(gmap_id)

# Write results (one gmap_id per line as JSON)
with out_path.open("w", encoding="utf-8") as fout:
    for gid in sorted(unique_gmap_ids):
        fout.write(json.dumps({"gmap_id": gid}, ensure_ascii=False) + "\n")

print(f"Extracted {len(unique_gmap_ids)} unique gmap_ids → {out_path}")
