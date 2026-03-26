#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

POSTS_DIR = Path("src/content/posts")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare a Software Rewired blog branch and post path.")
    p.add_argument("--brief")
    p.add_argument("--brief-file")
    p.add_argument("--title")
    p.add_argument("--slug")
    p.add_argument("--tags")
    p.add_argument("--author")
    p.add_argument("--date", dest="post_date")
    p.add_argument("--branch-prefix", default="blog/")
    p.add_argument("--skip-git", action="store_true")
    p.add_argument("--allow-dirty", action="store_true")
    args = p.parse_args()
    if not args.brief and not args.brief_file:
        p.error("Provide either --brief or --brief-file.")
    return args


def repo_root() -> Path:
    explicit = os.environ.get("REPO_PATH")
    return Path(explicit).expanduser().resolve() if explicit else Path(__file__).resolve().parents[2]


def run(cwd: Path, *cmd: str) -> str:
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()
def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "new-blog-post"


def brief_text(args: argparse.Namespace) -> str:
    if args.brief_file:
        return Path(args.brief_file).expanduser().read_text(encoding="utf-8").strip()
    return args.brief.strip()


def default_branch(root: Path) -> str:
    try:
        ref = run(root, "git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
        return ref.split("/", 1)[1]
    except subprocess.CalledProcessError:
        return os.environ.get("BLOG_DEFAULT_BRANCH", "main")


def ensure_branch(root: Path, branch: str, allow_dirty: bool) -> None:
    if run(root, "git", "status", "--porcelain") and not allow_dirty:
        raise RuntimeError("Git worktree is dirty. Commit or stash changes first, or rerun with --allow-dirty.")
    base = default_branch(root)
    run(root, "git", "checkout", base)
    run(root, "git", "pull", "--ff-only", "origin", base)
    if run(root, "git", "branch", "--list", branch):
        raise RuntimeError(f"Branch already exists: {branch}")
    run(root, "git", "checkout", "-b", branch)
def style_samples(posts_dir: Path) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    for path in sorted(posts_dir.glob("*.md"), reverse=True)[:3]:
        raw = path.read_text(encoding="utf-8")
        if not raw.startswith("---\n"):
            continue
        front, _, body = raw[4:].partition("\n---\n")
        title = re.search(r'^title:\s*"(.*)"$', front, re.M)
        summary = re.search(r'^summary:\s*"(.*)"$', front, re.M)
        samples.append({
            "path": path.as_posix(),
            "title": title.group(1) if title else path.stem,
            "summary": summary.group(1) if summary else "",
            "excerpt": body.strip()[:900],
        })
    return samples


def main() -> int:
    args = parse_args()
    root = repo_root()
    posts_dir = root / POSTS_DIR
    brief = brief_text(args)
    author = args.author or os.environ.get("BLOG_AUTHOR", "Anurag Mohan")
    post_date = args.post_date or str(date.today())
    slug = slugify(args.slug or args.title or brief.splitlines()[0][:80])
    branch = f"{args.branch_prefix}{slug}"
    if not args.skip_git:
        ensure_branch(root, branch, args.allow_dirty)
    payload = {
        "branch": branch if not args.skip_git else "(unchanged)",
        "post_path": str(posts_dir / f"{slug}.md"),
        "slug": slug,
        "date": post_date,
        "author": author,
        "title_hint": args.title or "",
        "tags_hint": [tag.strip() for tag in (args.tags or "").split(",") if tag.strip()],
        "brief": brief,
        "style_samples": style_samples(posts_dir),
    }
    print(json.dumps(payload, indent=2))
    return 0
if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
