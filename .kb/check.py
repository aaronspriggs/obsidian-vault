#!/usr/bin/env python3
"""Validate the vault: schema, enums, links and unique note names.

Runs from the pre-commit hook and exits 1 on any error. With --health it also
prints the working list HEALTH.md used to give (open work, stalled projects,
unverified Systems, untested runbooks, gaps that are allowed but should be
filled). With --map it prints the link graph instead: one line per System, or
with a note name, everything linked to or from that note grouped by kind, so a
lookup starts from one short listing instead of opening every backlink.
No AI is involved. Usage: .kb/check.py [--health | --map [note]]
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
LINK_PROPS = ("system", "project", "runs_on", "parent", "superseded_by")
PRIORITY = {"high": 0, "medium": 1, "low": 2}


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


def project_line(name, fm):
    line = f"[{fm.get('status')}/{fm.get('priority')}] {name}"
    step = str(fm.get("next_step") or "")
    return line + (f" -> {step[:117] + '...' if len(step) > 120 else step}" if step else "")


def backlinks(graph):
    back = {k: set() for k in graph}
    for k, node in graph.items():
        for t in node["links"]:
            if t in back and t != k:
                back[t].add(k)
    return back


def print_overview(graph):
    """One line per System: what's open against it and when it last changed."""
    back = backlinks(graph)
    for k, node in sorted(graph.items()):
        fm = node["fm"]
        if node["folder"] != "systems" or fm.get("status") == "deprecated":
            continue
        near = [graph[b] for b in back[k]]
        n = lambda f, *st: sum(1 for x in near if x["folder"] == f and (not st or x["fm"].get("status") in st))
        dates = [x["fm"]["date"] for x in near if x["folder"] == "changes"]
        print(f"- {node['rel'].stem} [{fm.get('category')}, {fm.get('status')}]"
              f"{' ' + str(fm['ip']) if fm.get('ip') else ''}: {n('projects', 'active', 'blocked')} open,"
              f" {n('projects', 'backlog')} backlog, {n('runbooks', 'active')} runbooks,"
              f" last change {max(dates) if dates else 'none'}")


def print_map(graph, query, recent=10):
    """Everything linked to or from one note, grouped so the open and current parts come first."""
    q = query.lower().removesuffix(".md")
    hits = [q] if q in graph else [k for k in graph if q in k]
    if len(hits) != 1:
        print(f"{len(hits)} notes match {query!r}" + "".join(f"\n- {graph[h]['rel']}" for h in sorted(hits)))
        sys.exit(2)
    k = hits[0]
    node, back = graph[k], backlinks(graph)
    fm = node["fm"]
    print(f"# {node['rel']} ({fm.get('status', '-')})\n{node['summary'][:200]}")
    for label, prop in (("Runs on", "runs_on"), ("Superseded by", "superseded_by"), ("Parent", "parent")):
        v = fm.get(prop)
        if v:
            print(f"{label}: {', '.join(v) if isinstance(v, list) else v}")
    near = {x: graph[x] for x in (node["links"] | back[k]) - {k} if x in graph}
    by = lambda f, *st: sorted((x for x in near.values()
                                if x["folder"] == f and (not st or x["fm"].get("status") in st)),
                               key=lambda x: x["rel"].stem)
    runs_on = lambda x: x["fm"].get("runs_on") or []
    hosted = {x["rel"].stem for x in by("systems") if any(f"[[{k}]]" == str(r).lower() for r in runs_on(x))}
    sections = [
        ("Open projects", [project_line(x["rel"].stem, x["fm"]) for x in sorted(
            by("projects", "active", "blocked"), key=lambda x: PRIORITY.get(x["fm"].get("priority"), 3))]),
        ("Runbooks", [f"{x['rel'].stem} ({x['fm'].get('kind')})" for x in by("runbooks", "active")]),
        ("Systems", [x["rel"].stem + (" (hosted here)" if x["rel"].stem in hosted else "")
                     for x in by("systems") if x["fm"].get("status") != "deprecated"]),
    ]
    for heading, rows in sections:
        if rows:
            print(f"\n## {heading} ({len(rows)})\n" + "\n".join(f"- {r}" for r in rows))
    backlog = by("projects", "backlog")
    if backlog:
        print(f"\n## Backlog ({len(backlog)}): " + "; ".join(x["rel"].stem for x in backlog))
    changes = sorted(by("changes"), key=lambda x: (x["fm"].get("date"), x["rel"].stem), reverse=True)
    if changes:
        print(f"\n## Changes ({min(recent, len(changes))} newest of {len(changes)})\n"
              + "\n".join(f"- {x['rel'].stem}" if x["rel"].stem.startswith(str(x["fm"].get("date")))
                          else f"- {x['fm'].get('date')} {x['rel'].stem}" for x in changes[:recent]))
    hidden = len(by("projects", "done")) + sum(1 for x in near.values() if x["fm"].get("status") == "deprecated")
    if hidden:
        print(f"\n{hidden} done/deprecated hidden")


def main():
    health = "--health" in sys.argv
    errors, gaps, graph = [], [], {}
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
    report = {"Open work": [], "Stalled projects": [], "Systems to verify": [], "Untested runbooks": []}
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
        node = graph[rel.stem.lower()] = {"rel": rel, "folder": folder, "fm": fm, "links": set(),
                                          "summary": next((ln for ln in body.splitlines() if ln.strip()), "")}
        for prop in LINK_PROPS:
            v = fm.get(prop) or []
            for x in v if isinstance(v, list) else [v]:
                if m := WIKILINK.fullmatch(str(x).strip()):
                    node["links"].add(m.group(1).strip().lower())
        body = CODE.sub("", body)  # links inside code are examples, not links
        for m in WIKILINK.finditer(body):
            node["links"].add(m.group(1).strip().lower().removesuffix(".md"))
            if not resolves(m.group(1)):
                errors.append(f"{rel}: link to missing note {m.group(1)!r}")
        for m in MDLINK.finditer(body):
            dest = m.group(1).strip("<>").split("#")[0]
            if not dest or re.match(r"[a-z][a-z0-9+.-]*:", dest, re.I):
                continue
            node["links"].add(pathlib.Path(urllib.parse.unquote(dest)).stem.lower())
            if not (p.parent / urllib.parse.unquote(dest)).resolve().exists():
                errors.append(f"{rel}: broken link {dest!r}")
        if re.search(r"https?://(www\.|app\.)?notion\.(so|com)/", body):
            gaps.append(f"{rel}: still links to Notion")

        if not health or not fm:
            continue
        status = fm.get("status")
        if folder == "projects":
            if status in ("active", "blocked"):
                report["Open work"].append(project_line(rel.stem, fm))
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
    if "--map" in sys.argv:
        args = sys.argv[sys.argv.index("--map") + 1:]
        print_map(graph, " ".join(args)) if args else print_overview(graph)
    if health:
        report["Open work"].sort(key=lambda r: (not r.startswith("[active"),
                                                PRIORITY.get(r.split("/")[1].split("]")[0], 3)))
        for heading, rows in report.items():
            print(f"\n## {heading} ({len(rows)})")
            print("\n".join(f"- {r}" for r in rows) or "- none")
        print(f"\n## Gaps ({len(gaps)})")
        print("\n".join(f"- {g}" for g in gaps) or "- none")
    print(f"{len(files)} files checked, {len(errors)} errors", file=sys.stderr)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
