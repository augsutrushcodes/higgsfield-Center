#!/usr/bin/env python3
"""Health check for the Higgsfield Center skill library.

Pure stdlib. Run from the repo root:

    python3 scripts/validate.py
    python3 scripts/validate.py --strict    # warnings become failures

Checks:
  1. Frontmatter contract on every SKILL.md
  2. Dispatcher parity  — every skills/<platform>/ is routed from root SKILL.md
  3. Relative links     — every markdown link to a repo path resolves
  4. Verification dates — flags anything older than STALE_DAYS
  5. Unverified blocks  — counts UNVERIFIED markers (reported, not failed)
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
DISPATCHER = ROOT / "SKILL.md"

STALE_DAYS = 30
TEMPLATE_DIR = "_template"
REQUIRED_META = ("version", "updated")
VALID_STATUS = {"draft", "verified", "stale"}

FAILURES: list[str] = []
WARNINGS: list[str] = []


def fail(label: str, detail: str = "") -> None:
    FAILURES.append(f"{label}{': ' + detail if detail else ''}")
    print(f"  FAIL  {label}" + (f" — {detail}" if detail else ""))
    return False


def warn(label: str, detail: str = "") -> None:
    WARNINGS.append(f"{label}{': ' + detail if detail else ''}")
    print(f"  WARN  {label}" + (f" — {detail}" if detail else ""))


def ok(label: str) -> None:
    print(f"  ok    {label}")


def frontmatter(text: str) -> str | None:
    """Return the YAML frontmatter block, or None if absent."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else None


def meta_block(fm: str) -> str:
    """Return the lines nested under `metadata:` so a stray top-level
    `version:` elsewhere in the frontmatter can't be read by mistake."""
    lines = fm.splitlines()
    out, collecting = [], False
    for line in lines:
        if re.match(r"^metadata:\s*$", line):
            collecting = True
            continue
        if collecting:
            if line and not line[0].isspace():
                break
            out.append(line)
    return "\n".join(out)


def skill_files() -> list[Path]:
    files = [DISPATCHER]
    files += sorted(SKILLS_DIR.glob("*/SKILL.md"))
    return files


def check_frontmatter() -> None:
    print("\nFrontmatter contract")
    for path in skill_files():
        rel = path.relative_to(ROOT)
        is_template = path.parent.name == TEMPLATE_DIR
        is_root = path == DISPATCHER
        text = path.read_text(encoding="utf-8")
        clean = True

        fm = frontmatter(text)
        if fm is None:
            fail(str(rel), "no YAML frontmatter")
            continue

        for key in ("name", "description"):
            if not re.search(rf"^{key}:", fm, re.M):
                clean = fail(str(rel), f"missing `{key}`")

        meta = meta_block(fm)
        if not meta.strip():
            clean = fail(str(rel), "missing `metadata:` block")
            continue

        for key in REQUIRED_META:
            if not re.search(rf"^\s+{key}:", meta, re.M):
                clean = fail(str(rel), f"missing `metadata.{key}`")

        # tags must be nested inside metadata, never top-level
        if re.search(r"^tags:", fm, re.M):
            clean = fail(str(rel), "`tags` is top-level — nest it under `metadata`")

        # parent contract: sub-skills declare it, the root dispatcher must not
        has_parent = re.search(r"^\s+parent:\s*(\S+)", meta, re.M)
        if is_root and has_parent:
            clean = fail(str(rel), "root dispatcher must not declare `metadata.parent`")
        elif not is_root and not has_parent:
            clean = fail(str(rel), "sub-skill missing `metadata.parent`")
        elif has_parent and not is_root:
            parent = has_parent.group(1)
            if parent != "higgsfield-center":
                clean = fail(str(rel), f"parent is `{parent}`, expected `higgsfield-center`")

        # status is required on platform skills so drafts stay visible
        status = re.search(r"^\s+status:\s*(\S+)", meta, re.M)
        if not is_root:
            if not status:
                clean = fail(str(rel), "missing `metadata.status`")
            elif status.group(1) not in VALID_STATUS:
                clean = fail(str(rel), f"status `{status.group(1)}` not in {sorted(VALID_STATUS)}")

        # name prefix keeps us collision-free against the upstream `higgsfield` skill
        name = re.search(r"^name:\s*(\S+)", fm, re.M)
        if name and not is_root and not is_template:
            if not name.group(1).startswith("hfc-"):
                clean = fail(str(rel), f"name `{name.group(1)}` must use the `hfc-` prefix")

        if clean:
            ok(str(rel))


def check_dispatcher_parity() -> None:
    print("\nDispatcher parity")
    text = DISPATCHER.read_text(encoding="utf-8")
    on_disk = {
        p.parent.name
        for p in SKILLS_DIR.glob("*/SKILL.md")
        if p.parent.name != TEMPLATE_DIR
    }
    for platform in sorted(on_disk):
        # a route is a link to the platform's file from the dispatcher
        if f"skills/{platform}/" in text:
            ok(f"{platform} routed")
        else:
            fail(f"{platform} on disk but not routed from SKILL.md")
    if not on_disk:
        warn("no platform skills on disk yet")


def check_links() -> None:
    print("\nRelative links")
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    checked = broken = 0
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts or "workspace" in md.parts:
            continue
        for target in pattern.findall(md.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            checked += 1
            if not (md.parent / path_part).resolve().exists():
                fail(f"{md.relative_to(ROOT)}", f"broken link → {target}")
                broken += 1
    if not broken:
        ok(f"{checked} relative links resolve")


def check_verification_dates() -> None:
    print("\nVerification freshness")
    today = dt.date.today()
    pattern = re.compile(r"\*\*Verified (\d{4}-\d{2}-\d{2})\*\*")
    found = False
    for path in skill_files():
        if path.parent.name == TEMPLATE_DIR:
            continue
        rel = path.relative_to(ROOT)
        dates = pattern.findall(path.read_text(encoding="utf-8"))
        if not dates:
            continue
        found = True
        oldest = min(dt.date.fromisoformat(d) for d in dates)
        age = (today - oldest).days
        if age > STALE_DAYS:
            warn(str(rel), f"verified {age}d ago — re-check before quoting numbers")
        else:
            ok(f"{rel} ({age}d old)")
    if not found:
        warn("no `**Verified YYYY-MM-DD**` markers found in any skill")


def check_unverified() -> None:
    print("\nUnverified claims")
    total = 0
    for path in skill_files():
        if path.parent.name == TEMPLATE_DIR:
            continue
        n = path.read_text(encoding="utf-8").count("**UNVERIFIED**")
        if n:
            total += n
            print(f"  note  {path.relative_to(ROOT)} — {n} unverified block(s)")
    if total:
        print(f"  note  {total} total — tracked, not a failure. See each file's TODO.")
    else:
        ok("no unverified blocks")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    print("Higgsfield Center — validate")
    check_frontmatter()
    check_dispatcher_parity()
    check_links()
    check_verification_dates()
    check_unverified()

    print("\n" + "-" * 52)
    print(f"{len(FAILURES)} failure(s), {len(WARNINGS)} warning(s)")
    if FAILURES:
        return 1
    if args.strict and WARNINGS:
        print("--strict: warnings are failures")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
