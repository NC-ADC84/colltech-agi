"""Quick importer: discover and normalize persona artifacts into JSON files.

Usage:
    python scripts/import_personalities.py --src <path-to-search> --out colltech_agi/personas

This is intentionally conservative: it extracts simple name/title and the
raw prompt/body text. Manual curation is recommended for complex personas.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import List


MD_TITLE_RE = re.compile(r"^#\s+(.+)", re.MULTILINE)


def extract_from_md(path: Path) -> dict:
    txt = path.read_text(encoding="utf-8")
    m = MD_TITLE_RE.search(txt)
    title = m.group(1).strip() if m else path.stem
    body = txt.strip()
    return {
        "name": title,
        "source": str(path),
        "type": "markdown",
        "content": body,
    }


def extract_from_py(path: Path) -> dict:
    txt = path.read_text(encoding="utf-8")
    # Heuristic: look for a top-level dict called PERSONALITY or a var named PERSONA
    name = path.stem
    persona_text = None
    if "PERSONALITY" in txt:
        persona_text = ""  # avoid executing unknown code; just capture full file
    return {
        "name": name,
        "source": str(path),
        "type": "python",
        "content": txt,
    }


def run(src: Path, out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    candidates: List[Path] = []
    for ext in ("*.md", "*.MD", "*.py", "*.json"):
        candidates.extend(src.rglob(ext))

    written = 0
    for p in sorted(set(candidates)):
        try:
            if p.suffix.lower() == ".md":
                doc = extract_from_md(p)
            elif p.suffix.lower() == ".py":
                doc = extract_from_py(p)
            elif p.suffix.lower() == ".json":
                # if it's already a JSON persona, copy as-is but normalize name
                data = json.loads(p.read_text(encoding="utf-8"))
                doc = {
                    "name": data.get("name", p.stem),
                    "source": str(p),
                    "type": "json",
                    "content": data,
                }
            else:
                continue

            name = re.sub(r"[^A-Za-z0-9_-]", "_", doc["name"])[:64]
            out_file = out / f"{name}.json"
            # If content is dict already, store under 'spec' so top-level keys are preserved
            payload = {
                "name": doc["name"],
                "source": doc["source"],
                "type": doc["type"],
                "spec": doc["content"] if isinstance(doc["content"], dict) else {"text": doc["content"]},
            }
            out_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            written += 1
        except Exception:
            # be conservative: skip problematic files
            continue

    print(f"Imported {written} persona candidates into {out}")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--src", type=Path, default=Path.cwd(), help="Root path to search for persona files")
    p.add_argument("--out", type=Path, default=Path("colltech_agi/personas"), help="Destination personas folder")
    args = p.parse_args()
    run(args.src, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
