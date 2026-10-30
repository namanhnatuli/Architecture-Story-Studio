"""Archive inactive projects safely (M7 cleanup; stdlib only).

  python3 tools/archive_projects.py --archive <dir outside the repo> slug [slug ...] [--dry-run]

For every project:
  1. inventory every file (git-tracked and untracked) with size and SHA256;
  2. MOVE the untracked/generated files (renders, outputs, scenes, logs, QA images: never in git)
     to <archive>/generated/<slug>/..., then re-hash them there and stop on any mismatch;
  3. leave the git-tracked source in place for a `git mv` (history is preserved by git; the
     archive also holds a `git bundle --all`).
Writes <archive>/inventory.json. Nothing is deleted: a move on the same volume needs no extra space.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def git_files(args, path):
    out = subprocess.run(["git", "ls-files", "-z", *args, "--", str(path)], cwd=ROOT, capture_output=True, check=True)
    return sorted(n for n in out.stdout.decode().split("\0") if n)


def inventory(rel_paths):
    rows = []
    for rel in rel_paths:
        f = ROOT / rel
        if f.is_file() and not f.is_symlink():
            rows.append({"path": rel, "bytes": f.stat().st_size, "sha256": sha256(f)})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("slugs", nargs="+")
    args = ap.parse_args()
    archive = Path(args.archive).resolve()
    if ROOT in archive.parents or archive == ROOT:
        raise SystemExit("the archive must be outside the repository")
    report = {"created_utc": datetime.now(timezone.utc).isoformat(), "repository": str(ROOT), "projects": {}}
    for slug in args.slugs:
        base = Path("projects") / slug
        tracked = git_files([], base)
        generated = git_files(["--others"], base)
        entry = {"tracked": inventory(tracked), "generated": inventory(generated)}
        entry["tracked_bytes"] = sum(r["bytes"] for r in entry["tracked"])
        entry["generated_bytes"] = sum(r["bytes"] for r in entry["generated"])
        print(f"{slug}: {len(tracked)} tracked ({entry['tracked_bytes'] / 1e6:.1f} MB), "
              f"{len(generated)} generated ({entry['generated_bytes'] / 1e6:.1f} MB)")
        if not args.dry_run:
            for r in entry["generated"]:
                dst = archive / "generated" / r["path"].split("/", 1)[1]
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    raise SystemExit(f"refusing to overwrite {dst}")
                os.rename(ROOT / r["path"], dst)
                if dst.stat().st_size != r["bytes"] or sha256(dst) != r["sha256"]:
                    raise SystemExit(f"verification failed after moving {r['path']}")
                r["archived_at"] = str(dst.relative_to(archive))
            entry["generated_verified"] = True
        report["projects"][slug] = entry
    if not args.dry_run:
        archive.mkdir(parents=True, exist_ok=True)
        out = archive / "inventory.json"
        if out.exists():
            previous = json.loads(out.read_text())
            previous["projects"].update(report["projects"])
            report["projects"] = previous["projects"]
        out.write_text(json.dumps(report, indent=1) + "\n")
        print(f"WROTE {out}")


if __name__ == "__main__":
    sys.exit(main())
