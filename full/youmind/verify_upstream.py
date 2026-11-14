"""Verify the untouched pinned YouMind archive, without importing/running upstream code.
Run with bundled Python. All reads/writes are confined to this directory.
"""
from pathlib import Path
import hashlib
import json
from collections import Counter

BASE = Path(__file__).resolve().parent
REVISION = "39c0c0033904de9c164df3ec2245d3b44526df04"
ROOT = BASE / f"ai-image-prompts-skill-{REVISION}"
tree = json.loads((BASE / "upstream-tree.json").read_text(encoding="utf-8"))
assert tree["sha"] == REVISION and not tree.get("truncated"), "Incomplete tree response"
blobs = [entry for entry in tree["tree"] if entry["type"] == "blob"]
files = []
for entry in blobs:
    path = ROOT / entry["path"]
    data = path.read_bytes()
    sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    assert len(data) == entry["size"] and sha == entry["sha"], f"Blob mismatch: {path}"
    files.append({"path": entry["path"], "bytes": len(data), "gitBlobSha1": sha,
                  "sha256": hashlib.sha256(data).hexdigest()})
manifest = json.loads((ROOT / "references/manifest.json").read_text(encoding="utf-8"))
seen = {}
category_results = []
schema_errors = []
no_sample = []
empty_descriptions = []
media_urls = set()
for category in manifest["categories"]:
    path = ROOT / "references" / category["file"]
    records = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(records, list), f"Not an array: {path}"
    assert len(records) == category["count"], f"Count mismatch: {path}"
    ids = Counter()
    for record in records:
        valid = (isinstance(record.get("id"), int)
                 and all(isinstance(record.get(k), str) and record[k].strip()
                         for k in ["content", "title"])
                 and isinstance(record.get("description"), str)
                 and isinstance(record.get("sourceMedia"), list)
                 and all(isinstance(url, str) and url.startswith("https://")
                         for url in record["sourceMedia"])
                 and isinstance(record.get("needReferenceImages"), bool))
        if not valid:
            schema_errors.append({"file": category["file"], "id": record.get("id")})
        ids[record["id"]] += 1
        if not record["description"].strip():
            empty_descriptions.append(record["id"])
        if not record.get("sourceMedia"):
            no_sample.append(record["id"])
        media_urls.update(record.get("sourceMedia", []))
        if record["id"] in seen:
            assert record == seen[record["id"]], f"Conflicting duplicate ID: {record['id']}"
        seen[record["id"]] = record
    assert max(ids.values(), default=0) <= 1, f"Repeated ID within {path}"
    category_results.append({**category, "actualCount": len(records), "bytes": path.stat().st_size})
assert not schema_errors, f"Schema errors: {schema_errors[:10]}"
assert len(seen) <= manifest["totalPrompts"], "Export exceeds CMS input total"
# Upstream generate-references.ts: totalPrompts = allPrompts.length (CMS input),
# while transformToOutputPrompt omits records with no sample images.
report = {
    "source": "https://github.com/YouMind-OpenLab/ai-image-prompts-skill",
    "revision": REVISION,
    "packageVersion": json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"],
    "skillPath": str(ROOT / "SKILL.md"),
    "manifestUpdatedAt": manifest["updatedAt"],
    "allGitBlobsVerified": True,
    "upstreamFileCount": len(files),
    "upstreamBytes": sum(f["bytes"] for f in files),
    "referenceJsonBytes": sum(f["bytes"] for f in files if f["path"].startswith("references/") and f["path"].endswith(".json")),
    "manifestCmsInputTotal": manifest["totalPrompts"],
    "uniquePrompts": len(seen),
    "cmsInputMinusExportedUnique": manifest["totalPrompts"] - len(seen),
    "totalSemantics": "manifest totalPrompts counts CMS input; exported references omit records without sample images and may omit unknown-only useCases (generate-references.ts:92-105,271-289,324-333)",
    "categoryMemberships": sum(c["actualCount"] for c in category_results),
    "categoryCount": len(category_results),
    "allCategoryCountsMatch": True,
    "allPromptSchemasValid": True,
    "allRepeatedIdsConsistent": True,
    "uniquePromptsWithoutSample": len(set(no_sample)),
    "emptyDescriptionIds": sorted(set(empty_descriptions)),
    "emptyDescriptionMemberships": len(empty_descriptions),
    "distinctSampleMediaUrls": len(media_urls),
    "remoteMediaAvailabilityChecked": False,
    "originalScriptsExecuted": False,
    "categories": category_results,
    "files": files,
}
(BASE / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in report.items() if k not in ("files", "categories")}, ensure_ascii=False, indent=2))
print("All category counts and all upstream Git blob SHA1 hashes verified.")
