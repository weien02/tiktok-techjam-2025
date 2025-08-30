#!/usr/bin/env python3
import json
from pathlib import Path

# ====== CONFIG ======
in_path = Path("../../dataSource/review-Utah.json")      # input json file
out_path = Path("../../sampleData/user_past_reviews.jsonl")  # output path
# ====================

unique_user_ids = []
reviews_by_user = {}

def clean_jsonl_line(s: str) -> str:
    """Fix common JSONL issues: BOM, trailing commas, stray brackets."""
    s = s.lstrip("\ufeff").strip()          # remove BOM and whitespace
    if not s or s in ("[", "]", ","):       # skip array markers if present
        return ""
    if s.endswith(","):                     # drop trailing comma if someone saved as "},"
        s = s[:-1].rstrip()
    return s

# Pass 1: read the file line-by-line and collect first 50 unique user_ids + reviews, adjustable
with in_path.open("r", encoding="utf-8") as fin:
    for lineno, line in enumerate(fin, 1):
        raw = clean_jsonl_line(line)
        if not raw:
            continue
        try:
            review = json.loads(raw)
        except json.JSONDecodeError as e:
            # Helpful debug: show where it failed but keep going
            print(f"Skipping line {lineno}: JSON decode error -> {e}")
            continue

        uid = review.get("user_id")
        if not uid:
            continue

        if uid not in unique_user_ids:
            if len(unique_user_ids) >= 50:
                # we already have our first 50 unique ids; keep collecting reviews for them only
                pass
            else:
                unique_user_ids.append(uid)
                reviews_by_user[uid] = []

        if uid in unique_user_ids and len(reviews_by_user[uid]) < 50:
            reviews_by_user[uid].append({
                "user_id": uid,
                "name": review.get("name"),
                "review": review.get("text", ""),
                "rating": review.get("rating"),
                "time": review.get("time"),
                "gmap_id": review.get("gmap_id"),
            })

# Write results as JSONL in the requested shape
out_path.parent.mkdir(parents=True, exist_ok=True)
with out_path.open("w", encoding="utf-8") as fout:
    for uid in unique_user_ids:
        for item in reviews_by_user.get(uid, []):
            fout.write(json.dumps(item, ensure_ascii=False) + "\n")

print("First 50 unique user_ids:")
for i, uid in enumerate(unique_user_ids, 1):
    print(f"{i:2d}. {uid}")

print(f"\nDone. Wrote filtered reviews to: {out_path}")
