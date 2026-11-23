from __future__ import annotations

import argparse
import time
import zipfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser(description="Package this skill into a shareable zip.")
    ap.add_argument("--output", required=True, help="Output directory for zip")
    ap.add_argument("--name", default="rpg-workflow-dashboard")
    args = ap.parse_args()
    out_dir = Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    zip_path = out_dir / f"{args.name}-{stamp}.zip"
    root_name = args.name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in SKILL_DIR.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(SKILL_DIR)
            if "__pycache__" in rel.parts:
                continue
            z.write(p, Path(root_name) / rel)
    print(zip_path)


if __name__ == "__main__":
    main()
