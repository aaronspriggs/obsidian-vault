#!/usr/bin/env python3
"""Validate the vault: schema, enums, links and unique note names.

Runs from the pre-commit hook and exits 1 on any error. With --health it also
prints the working list HEALTH.md used to give (stalled projects, unverified
Systems, untested runbooks, gaps that are allowed but should be filled).
No AI is involved. Usage: .kb/check.py [--health]
"""
import datetime
import pathlib
import re
import subprocess
import sys
import urllib.parse

import yaml

VAULT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".kb", ".obsidian", ".trash", "templates", "attachments"}
STALLED_DAYS, VERIFY_DAYS, TEST_DAYS = 30, 90, 180

SCHEMA = {  # folder -> {property: (required, allowed values or kind)}
    "systems": {"status": (True, {"active", "spare", "planned", "deprecated"}),
                "category": (True, {"hardware", "vm", "docker", "network", "software"}),
                "runs_on": (False, "links"), "last_verified": (False, "date"), "superseded_by": (False, "link")},
    "projects": {"type": (True, {"task", "project", "idea"}),
                 "status": (True, {"active", "blocked", "backlog", "done"}),
                 "priority": (True, {"high", "medium", "low"}), "system": (True, "links"),
                 "parent": (False, "link"), "completed": (False, "date"), "superseded_by": (False, "link")},
    "changes": {"date": (True, "date"), "type": (True, {"fix", "upgrade", "config", "install", "doc", "research"}),
                "system": (True, "links"), "project": (False, "links"), "commit": (False, "url")},
    "runbooks": {"kind": (True, {"setup", "procedure", "troubleshooting", "recovery", "reference"}),
                 "status": (True, {"active", "deprecated"}), "system": (True, "links"),
                 "last_tested": (False, "date"), "superseded_by": (False, "link")},
}
WIKILINK = re.compile(r"!?\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\]\((<[^>]+>|[^)\s]+)\)")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def notes():
    for p in sorted(VAULT.rglob("*")):
        rel = p.relative_to(VAULT)
        if p.is_file() and p.suffix in (".md", ".base") and not SKIP_DIRS & set(rel.parts[:-1]):
            yield p, rel


def split(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5:]
    return None, text


def last_commit(rel):
    out = subprocess.run(["git", "-C", str(VAULT), "log", "-1", "--format=%cs", "--", str(rel)],
                         capture_output=True, text=True).stdout.strip()
    return datetime.date.fromisoformat(out) if out else None


def main():
    health = "--health" in sys.argv
    errors, gaps = [], []
    files = list(notes())
    by_name = {}
    for p, rel in files:
        key = (rel.stem if p.suffix == ".md" else rel.name).lower()
        if key in by_name:
            errors.append(f"{rel}: duplicate note name (also {by_name[key]})")
        by_name[key] = rel

    def resolves(target):
        target = target.strip()
        return target.lower() in by_name or target.lower().removesuffix(".md") in by_name

    today = datetime.date.today()
    report = {"Stalled projects": [], "Systems to verify": [], "Untested runbooks": []}
    for p, rel in files:
        if p.suffix != ".md":
            continue
        text = p.read_text()
        fm_text, body = split(text)
        folder = rel.parts[0] if len(rel.parts) > 1 else ""
        fm = {}
        if folder in SCHEMA:
            if fm_text is None:
                errors.append(f"{rel}: no frontmatter")
                continue
            try:
                fm = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError as e:
                errors.append(f"{rel}: bad YAML: {e}")
                continue
            for prop, (required, rule) in SCHEMA[folder].items():
                v = fm.get(prop)
                if v in (None, "", []):
                    if required and not (prop == "priority" and fm.get("status") == "done"):
                        errors.append(f"{rel}: missing {prop}")
                    continue
                if isinstance(rule, set) and v not in rule:
                    errors.append(f"{rel}: {prop}={v!r} not one of {sorted(rule)}")
                elif rule == "date" and not isinstance(v, datetime.date):
                    errors.append(f"{rel}: {prop}={v!r} is not a YYYY-MM-DD date")
                elif rule in ("link", "links"):
                    vals = v if isinstance(v, list) else [v]
                    if rule == "link" and isinstance(v, list):
                        errors.append(f"{rel}: {prop} must be a single link")
                    for x in vals:
                        m = WIKILINK.fullmatch(str(x).strip())
                        if not m:
                            errors.append(f"{rel}: {prop} value {x!r} is not a [[link]]")
                        elif not resolves(m.group(1)):
                            errors.append(f"{rel}: {prop} links to missing note {m.group(1)!r}")
            for prop in set(fm) - set(SCHEMA[folder]) - {"ip", "port", "url", "repo", "next_step", "notion_id"}:
                errors.append(f"{rel}: unknown property {prop!r}")
        body = CODE.sub("", body)  # links inside code are examples, not links
        for m in WIKILINK.finditer(body):
            if not resolves(m.group(1)):
                errors.append(f"{rel}: link to missing note {m.group(1)!r}")
        for m in MDLINK.finditer(body):
            dest = m.group(1).strip("<>").split("#")[0]
            if not dest or re.match(r"[a-z][a-z0-9+.-]*:", dest, re.I):
                continue
            if not (p.parent / urllib.parse.unquote(dest)).resolve().exists():
                errors.append(f"{rel}: broken link {dest!r}")
        if re.search(r"https?://(www\.|app\.)?notion\.(so|com)/", body):
            gaps.append(f"{rel}: still links to Notion")

        if not health or not fm:
            continue
        status = fm.get("status")
        if folder == "projects":
            if status in ("active", "blocked") and not fm.get("next_step"):
                gaps.append(f"{rel}: {status} but no next_step")
            if status == "done" and not fm.get("completed"):
                gaps.append(f"{rel}: done but no completed date")
            touched = last_commit(rel)
            if status == "active" and touched and (today - touched).days >= STALLED_DAYS:
                report["Stalled projects"].append(f"{rel} (last change {touched})")
        if folder == "systems" and status != "deprecated":
            lv = fm.get("last_verified")
            if not lv or (today - lv).days >= VERIFY_DAYS:
                report["Systems to verify"].append(f"{rel} ({lv or 'never'})")
        if folder == "runbooks" and status != "deprecated":
            lt = fm.get("last_tested")
            if not lt or (today - lt).days >= TEST_DAYS:
                report["Untested runbooks"].append(f"{rel} ({lt or 'never'})")

    for e in errors:
        print("ERROR", e)
    if health:
        for heading, rows in report.items():
            print(f"\n## {heading} ({len(rows)})")
            print("\n".join(f"- {r}" for r in rows) or "- none")
        print(f"\n## Gaps ({len(gaps)})")
        print("\n".join(f"- {g}" for g in gaps) or "- none")
    print(f"{len(files)} files checked, {len(errors)} errors", file=sys.stderr)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
