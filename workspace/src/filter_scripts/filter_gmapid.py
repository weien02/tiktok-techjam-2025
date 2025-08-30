#!/usr/bin/env python3
import json
from pathlib import Path

# ====== CONFIG ======
reviews_path = Path("../../sampleData/user_past_reviews.jsonl") # file with user reviews + gmap_id
business_path = Path("../../dataSource/meta-Utah.json") # file with business info
out_path = Path("../../sampleData/unique_gmap_ids.jsonl")  # output
# ====================

# Step 1: Collect unique gmap_ids from reviews
unique_gmap_ids = set()
with reviews_path.open("r", encoding="utf-8") as fin:
    for lineno, line in enumerate(fin, 1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Skipping review line {lineno}: JSON decode error -> {e}")
            continue

        gid = record.get("gmap_id")
        if gid:
            unique_gmap_ids.add(gid)

print(f"Found {len(unique_gmap_ids)} unique gmap_ids from reviews.")

# Step 2: Filter business_data.jsonl for matching gmap_ids
filtered_records = []
with business_path.open("r", encoding="utf-8") as fin:
    for lineno, line in enumerate(fin, 1):
        line = line.strip()
        if not line:
            continue
        try:
            biz = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Skipping business line {lineno}: JSON decode error -> {e}")
            continue

        gid = biz.get("gmap_id")
        if gid in unique_gmap_ids:
            filtered_records.append({
                "gmap_id": gid,
                "name": biz.get("name"),
                "address": biz.get("address"),
                "description": biz.get("description"),
                "category": biz.get("category"),
            })

# Step 3: Write output JSONL
with out_path.open("w", encoding="utf-8") as fout:
    for rec in filtered_records:
        fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"Wrote {len(filtered_records)} filtered business records → {out_path}")
