---
date: 2026-09-27
type: install
system:
- '[[ClaudeCode (VM)]]'
notion_id: 3e87ae76-22ba-81a7-b46b-d43ae7d667c7
---

# Installed kb-export: weekly Notion KB backup to git + HEALTH.md lint (no AI)

Weekly read-only export of the whole KB to markdown on branch kb-export of spriggs-homelab, with a [HEALTH.md](http://health.md/) lint report and a gitleaks gate. Commit cd94671; first export 3f24d40.

Part of [KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)](<../projects/KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager).md>), phase 0 (safety net).
**What:** the script [`kb-export/kb-export`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/kb-export), commit [cd94671](https://github.com/aaronspriggs/spriggs-homelab/commit/cd94671). It's Python stdlib only and uses no AI or Claude usage. It runs from `kb-export.timer` on Sundays at 06:30 America/Denver, after homelab-update, with Persistent=true. It uses the read-only `kb-export` Notion integration.
**Each run:**
1. Exports every visible page, with its properties as front matter, to `~/kb-export`. That's a separate clone on the orphan branch [`kb-export`](https://github.com/aaronspriggs/spriggs-homelab/tree/kb-export), which never merges to main.
2. Writes `HEALTH.md`: missing required properties, stalled Active/Blocked projects (30+ days), runbooks with no System, pages outside the KB, and `make check`.
3. Runs gitleaks with the repo rules. On a hit it does not commit, and sends a time-sensitive push through the existing "Homelab — VM Update Reports" webhook (host "Notion KB").
4. Commits and pushes, then pings Kuma (push URL pending).
**First run, 2026-09-27:** 162 pages, 218 API requests, about 85 s. Pushed as [3f24d40](https://github.com/aaronspriggs/spriggs-homelab/commit/3f24d40). No secrets found in current page content. Notion page history isn't exported, so it isn't scanned.
**Verified:**
- The gate blocked a commit when a fake HA webhook URL was planted (exit 2).
- `make check` is all ok, with the 3 new files in `deployed.tsv`.
**Restore path:** Notion Free keeps only 7 days of page history. The git history of the `kb-export` branch is now the long-term history and restore source.
**Kuma:** push monitor "KB Export" (8-day heartbeat) created by Aaron 2026-09-28. Its URL is in `~/.config/kb-export/kb-export.json`. Test push returned 200. The first attempt got a 404, most likely because the monitor wasn't active yet.
