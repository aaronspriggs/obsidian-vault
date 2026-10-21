#!/usr/bin/env python3
"""One-off migration of the Notion HomeLab KB into this vault.

Reads Notion with kb-export's read-only token and its tested API client and
block renderer (~/homelab/kb-export/kb-export), then writes notes in the vault
schema that .kb/check.py enforces. Rerunnable: it rewrites systems/, projects/,
changes/, runbooks/ and STANDARDS.md from live Notion each time, so the pilot
and the final cutover run the same code.
Usage: .kb/migrate.py [--dry-run]
"""
import datetime
import importlib.machinery
import os
import pathlib
import re
import shutil
import sys
import types

import yaml

HOME = pathlib.Path.home()
VAULT = pathlib.Path(__file__).resolve().parent.parent
loader = importlib.machinery.SourceFileLoader("kbx", str(HOME / "homelab/kb-export/kb-export"))
kbx = types.ModuleType("kbx")
loader.exec_module(kbx)

FOLDERS = {"Systems": "systems", "Projects": "projects", "Changes": "changes", "Runbooks": "runbooks"}
STANDARDS_ID = "3e97ae76-22ba-8169-8035-ff7c041b2ee7"
CHANGE_STEM_MAX = 80
ID_RE = re.compile(r"([0-9a-f]{32}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})")

# Runbook kind replaces Notion's Tags (which only repeated the System relation).
RUNBOOK_KINDS = [  # first match wins
    ("homelab-update", "procedure"), ("fix run", "procedure"),
    ("disaster recovery", "recovery"), ("rebuild", "recovery"), ("restore", "recovery"),
    ("offsite backup", "recovery"), ("mfa recovery", "recovery"), ("recovery", "recovery"),
    ("troubleshooting", "troubleshooting"), ("recovering", "troubleshooting"),
    ("conventions", "reference"),
    ("setup", "setup"), ("setting up", "setup"), ("set up", "setup"), ("creating", "setup"),
    ("api access", "setup"),
    ("reboot", "procedure"), ("updating", "procedure"), ("homelab-update", "procedure"),
    ("managing", "procedure"), ("alerting", "procedure"), ("fix run", "procedure"),
]

warnings = []
paths = {}      # notion id -> vault-relative path ("systems/Big Boi.md")
names = {}      # notion id -> note name (file stem)
current_dir = ""  # folder of the note being rendered, for relative links


def norm(i):
    return i.replace("-", "")


def clean_title(title):
    """Strip deprecation markers from a title; return (title, deprecated, replaced_by)."""
    dep = re.search(r"\s*[\[(]\s*deprecated\b([^\])]*)[\])]", title, re.I)
    replaced = None
    if dep:
        m = re.search(r"replaced by (.+)", dep.group(1), re.I)
        replaced = m.group(1).strip(" —-") if m else None
        title = title[:dep.start()] + title[dep.end():]
    return title.strip(), bool(dep), replaced


def stem_for(title):
    s = re.sub(r"(^|[\s(])/", r"\1", title.replace(": ", " - ").replace(" / ", " - ")).replace("/", "-")
    s = re.sub(r'[\\:*?"<>|#^\[\]]', "", s)
    return re.sub(r"\s+", " ", s).strip(" .")


def truncate(s, n):
    if len(s) <= n:
        return s
    head = s[:n]
    clause = max(head.rfind(sep) for sep in ("; ", " — ", " - ", ", "))
    cut = head[:clause] if clause >= n // 2 else head.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;-—+&")


def link(target_id, text=None):
    """Markdown link to another note, relative to the note being rendered."""
    tid = norm(target_id)
    if tid not in paths:
        return None
    rel = os.path.relpath(paths[tid], current_dir or ".")
    return f"[{text or names[tid]}](<{rel}>)"


def wikilink(target_id):
    tid = norm(target_id)
    return f"[[{names[tid]}]]" if tid in names else None


def md_text(rich, titles):
    out = []
    for r in rich or []:
        if r["type"] == "mention" and r["mention"]["type"] in ("page", "database"):
            m = r["mention"]
            tid = m[m["type"]]["id"]
            out.append(link(tid) or r["plain_text"])
            if norm(tid) not in paths:
                warnings.append(f"{current_dir}: mention of unmigrated page {r['plain_text']!r}")
            continue
        if r["type"] == "mention" and r["mention"]["type"] == "date":
            out.append(kbx.fmt_date(r["mention"]["date"]))
            continue
        t = r.get("plain_text", "")
        if not t:
            continue
        a = r.get("annotations", {})
        if a.get("code"):
            t = f"`{t}`"
        if a.get("bold"):
            t = f"**{t}**"
        if a.get("italic"):
            t = f"*{t}*"
        if a.get("strikethrough"):
            t = f"~~{t}~~"
        href = r.get("href")
        if href:
            m = ID_RE.search(href) if (href.startswith("/") or "notion." in href) else None
            if m and link(m.group(1), t):
                t = link(m.group(1), t)
            elif href.startswith("/"):
                warnings.append(f"{current_dir}: internal link to unmigrated page {href} ({t!r})")
            else:
                if "notion." in href:
                    warnings.append(f"{current_dir}: Notion URL kept as-is: {href}")
                t = f"[{t}]({href})"
        out.append(t)
    return "".join(out)


kbx.md_text = md_text


class Renderer(kbx.Renderer):
    embed = None  # what a linked database view becomes in the note being rendered

    def block(self, b, depth, num):
        t = b["type"]
        ind = "    " * depth
        if t == "child_database":
            if self.embed:
                return [ind + self.embed]
            warnings.append(f"{current_dir}: dropped a linked database view")
            return []
        if t in ("child_page", "link_to_page"):
            d = b.get(t, {})
            target = b["id"] if t == "child_page" else d.get(d.get("type"), "")
            return [ind + (link(target) or d.get("title", ""))]
        return super().block(b, depth, num)


def date_value(s):
    if not s:
        return None
    try:
        return datetime.date.fromisoformat(s[:10]) if "→" not in s else s
    except ValueError:
        return s  # a range; kept as text


def lower(v):
    return v.lower() if isinstance(v, str) and v else None


def rel_links(raw, prop):
    p = raw.get(prop)
    if not p or p["type"] != "relation":
        return []
    return [w for w in (wikilink(r["id"]) for r in p["relation"]) if w]


def rich(raw, prop):
    p = raw.get(prop)
    return md_text(p.get(p["type"]), {}).strip() if p and p["type"] in ("rich_text", "title") else ""


def plain_prop(p, prop):
    v = p["properties"].get(prop)
    return kbx.prop_value(v, {}) if v else None


def frontmatter(folder, p, deprecated, replaced_by):
    raw = p["properties"]
    get = lambda k: plain_prop(p, k)
    if folder == "systems":
        fm = {"status": "deprecated" if deprecated else lower(get("Status")), "category": lower(get("Category")),
              "ip": get("IP") or None, "port": get("Port"), "url": get("Access URL"),
              "runs_on": rel_links(raw, "Runs On"), "last_verified": date_value(get("Last Verified")),
              "repo": get("Repo")}
    elif folder == "projects":
        status = lower(get("Status"))
        parent = rel_links(raw, "Parent")
        fm = {"type": lower(get("Type")), "status": "backlog" if status == "deferred" else status,
              "priority": lower(get("Priority")), "system": rel_links(raw, "System"),
              "parent": parent[0] if parent else None, "next_step": get("Next Step") or None,
              "completed": date_value(get("Date Completed"))}
    elif folder == "changes":
        fm = {"date": date_value(get("When")), "type": lower(get("Type")), "system": rel_links(raw, "System"),
              "project": rel_links(raw, "Project"), "commit": get("Commit")}
    else:
        title = clean_title(kbx.page_title(p))[0].lower()
        kind = next((k for key, k in RUNBOOK_KINDS if key in title), None)
        if not kind:
            warnings.append(f"runbooks: no kind for {title!r}")
        fm = {"kind": kind, "status": "deprecated" if deprecated else "active", "system": rel_links(raw, "System"),
              "last_tested": date_value(get("Last Tested")), "repo": get("Repo")}
    if deprecated and replaced_by:
        match = [i for i, n in names.items() if n.lower() == stem_for(replaced_by).lower()]
        if match:
            fm["superseded_by"] = f"[[{names[match[0]]}]]"
    fm["notion_id"] = p["id"]
    return {k: v for k, v in fm.items() if v not in (None, "", [])}


def main():
    global current_dir
    dry = "--dry-run" in sys.argv
    api = kbx.Notion(kbx.TOKEN_FILE.read_text().strip())
    # Search finds the databases; their pages come from a direct query, because
    # search lags behind recent edits (a run once missed two just-edited pages).
    pages, dbs = [], []
    for o in api.paginate("POST", "/search", {"page_size": 100}):
        (pages if o["object"] == "page" else dbs).append(o)
    pages = [p for p in pages if p["parent"]["type"] != "database_id"]
    if not any(norm(p["id"]) == norm(STANDARDS_ID) for p in pages):
        pages.append(api.call("GET", f"/pages/{STANDARDS_ID}"))
    for d in dbs:
        if kbx.plain(d["title"]) in FOLDERS:
            pages += api.paginate("POST", f"/databases/{d['id']}/query", {"page_size": 100})
    pages = [p for p in pages if not p.get("archived") and not p.get("in_trash")]
    db_names = {norm(d["id"]): kbx.plain(d["title"]) for d in dbs}
    titles = {p["id"]: kbx.page_title(p) for p in pages}

    notes = []  # (page, folder, deprecated, replaced_by, full_title)
    for p in pages:
        parent = p["parent"]
        db = db_names.get(norm(parent.get("database_id", ""))) if parent["type"] == "database_id" else None
        if norm(p["id"]) == norm(STANDARDS_ID):
            paths[norm(p["id"])], names[norm(p["id"])] = "STANDARDS.md", "STANDARDS"
            notes.append((p, "", False, None, "KB Standards"))
            continue
        if db not in FOLDERS:
            warnings.append(f"skipped page outside the four databases: {titles[p['id']]!r}")
            continue
        folder = FOLDERS[db]
        title, deprecated, replaced_by = clean_title(titles[p["id"]])
        stem = stem_for(title)
        if folder == "changes":
            when = (plain_prop(p, "When") or p["created_time"][:10])[:10]
            stem = f"{when} {truncate(stem, CHANGE_STEM_MAX)}"
        base, n = stem, 2
        while stem.lower() in {s.lower() for s in names.values()}:
            stem = f"{base} ({n})"
            n += 1
        if stem != base:
            warnings.append(f"name collision: {base!r} became {stem!r}")
        paths[norm(p["id"])], names[norm(p["id"])] = f"{folder}/{stem}.md", stem
        notes.append((p, folder, deprecated, replaced_by, title))
    for d in dbs:
        name = db_names[norm(d["id"])]
        if name in FOLDERS:
            paths[norm(d["id"])], names[norm(d["id"])] = f"bases/{name}.base", f"{name}.base"

    # Reverse relations that become embedded views instead of stored properties.
    hosts, sub_items, project_changes = set(), set(), set()
    for p, folder, *_ in notes:
        kbx.full_relations(api, p)
        raw = p["properties"]
        if folder == "systems":
            hosts |= {norm(r["id"]) for r in raw.get("Runs On", {}).get("relation", [])}
        if folder == "projects":
            sub_items |= {norm(r["id"]) for r in raw.get("Parent", {}).get("relation", [])}
        if folder == "changes":
            project_changes |= {norm(r["id"]) for r in raw.get("Project", {}).get("relation", [])}

    if dry:
        for p, folder, *_ in notes:
            print(paths[norm(p["id"])])
        print("\n".join(warnings), file=sys.stderr)
        return

    for f in list(FOLDERS.values()):
        shutil.rmtree(VAULT / f, ignore_errors=True)
        (VAULT / f).mkdir()
    render = Renderer(api, titles)
    for p, folder, deprecated, replaced_by, title in sorted(notes, key=lambda n: paths[norm(n[0]["id"])]):
        pid = norm(p["id"])
        current_dir = folder
        Renderer.embed = "![[Projects.base#Open for this system]]" if folder == "systems" else None
        lead = {"systems": "Notes", "projects": "Notes", "changes": "Details", "runbooks": "Summary"}.get(folder)
        body = [rich(p["properties"], lead)] if lead and rich(p["properties"], lead) else []
        body += [""] + render.children(p["id"])
        if folder == "systems":
            if pid in hosts:
                body += ["", "## Runs on this", "", "![[Systems.base#Runs on this]]"]
            body += ["", "## Runbooks", "", "![[Runbooks.base#For this system]]",
                     "", "## Recent changes", "", "![[Changes.base#For this system]]"]
        if folder == "projects":
            if pid in sub_items:
                body += ["", "## Sub-items", "", "![[Projects.base#Sub-items]]"]
            if pid in project_changes:
                body += ["", "## Changes", "", "![[Changes.base#For this project]]"]
        text = re.sub(r"\n{3,}", "\n\n", "\n".join(body).strip()) + "\n"
        if names[pid] != title and folder:  # filename shortened or cleaned: keep the full title visible
            text = f"# {title}\n\n" + text
        if folder:
            fm = frontmatter(folder, p, deprecated, replaced_by)
            text = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n" + text
        (VAULT / paths[pid]).write_text(text)
    print(f"wrote {len(notes)} notes; {api.requests} Notion API requests")
    print("\n".join(sorted(set(warnings))), file=sys.stderr)


if __name__ == "__main__":
    main()
