---
date: 2026-09-28
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/6ea7299
notion_id: 3e97ae76-22ba-8149-9aed-cb2fd28730f4
---

# KB governance phase 2: schema properties, derived formulas and views

Added phase 2 properties to all four DBs, checkbox formulas for time-based views, 5 views, Type backfill on 7 projects; kb-export lints Systems Status (commit 6ea7299).

**What:** Phase 2 of [KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)](<../projects/KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager).md>).
- **Systems:** `Status` (Active/Spare/Planned/Deprecated), `Runs On` ↔ `Hosts` (self-relation), `Last Verified` (date), `Repo` (URL). Category options unchanged; new ones get added in phase 4 with the new pages.
- **Projects:** `Parent` ↔ `Sub-items` (self-relation), `Next Step` (text), `Last Edited` (last edited time), and `Changes` (reverse of Changes → Project).
- **Changes:** `Commit` (URL), `Project` (relation to Projects).
- **Runbooks:** `Last Tested` (date), `Repo` (URL).
- **Derived checkbox formulas:** Projects `Stalled`, Systems `Needs Verification`, Runbooks `Untested`, Changes `Recent`. The view API only takes fixed ISO dates, so a "30+ days ago" filter needs a formula to stay current.
- **Views:** Projects "Open work" (Active/Blocked, by Priority) and "Stalled"; Changes "Last 14 days"; Systems "Needs verification"; Runbooks "Untested". The API wouldn't save a filter on a formula property, so the last four show the formula column but aren't filtered on it yet (Aaron adds the filter in the UI; see the project page).
- **Backfill:** `Type` set on the 7 projects missing it (Task: motion sensor, home theatre wiring, screensaver, DDNS, servarr autoheal; Project: Pi-hole, Overseerr→Seerr). Home Assistant OS `Runs On` = TrueNAS SCALE (Big Boi), set while testing the relation pairing.
- **kb-export:** exports formula values and lints "Systems missing Status or Category" (commit [6ea7299](https://github.com/aaronspriggs/spriggs-homelab/commit/6ea7299)); deployed to `~/.local/bin/kb-export`, `make check` clean, test export e3cf37e.
- [STANDARDS](<../STANDARDS.md>): dropped the *(phase 2)* markers and documented the derived columns.
**Gotcha:** in the Notion MCP's DDL, each `RELATION(..., DUAL ...)` statement creates its own pair. Adding both sides of a self-relation in one call produced two pairs (`Runs On`/`Hosts 1` and `Hosts`/`Runs On 1`); the empty extra pair was dropped and the survivor renamed. Add only one side.
**Verify:** the "Stalled" formula matched [HEALTH.md](http://health.md/)'s 8 stale Active projects before the Type backfill touched one of them (now 7).
**Roll back:** drop the added columns; the git export at 3f24d40 holds the pre-change schema (`databases/*.json`).
