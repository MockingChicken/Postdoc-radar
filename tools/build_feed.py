"""Build jobs.json (the live posting list the website reads) from exported posting files.

Usage: python3 tools/build_feed.py <dir with one <id>.json per posting> <meta.json> <output jobs.json>
"""
import json, os, sys
from datetime import datetime, timezone

src, meta_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
jobs = []
for name in sorted(os.listdir(src)):
    if not name.endswith(".json"):
        continue
    with open(os.path.join(src, name), encoding="utf-8") as f:
        doc = json.load(f)
    doc = doc.get("data", doc)  # accept either a bare body or {id, data}
    doc["id"] = name[:-5]
    jobs.append(doc)
with open(meta_path, encoding="utf-8") as f:
    meta = json.load(f)
meta = meta.get("data", meta)
keep = {k: meta.get(k) for k in ("lastRun", "lastAdded", "sources", "baseline")}
keep["total"] = len(jobs)
feed = {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "meta": keep, "jobs": jobs}
with open(out, "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, separators=(",", ":"))
print(f"wrote {out}: {len(jobs)} postings")
