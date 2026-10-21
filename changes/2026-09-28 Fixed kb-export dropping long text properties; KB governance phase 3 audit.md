---
date: 2026-09-28
type: fix
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/a2c8c86
notion_id: 3e97ae76-22ba-81ec-ac97-da99f8f21088
---

# Fixed kb-export dropping long text properties; KB governance phase 3 audit

kb-export omitted text properties of 500+ chars from the backup (29 pages); now written into the page body. Phase 3 audit table added to the KB governance project.

**What:** `kb-export` built each page's front matter from properties under 500 characters and never wrote the longer ones anywhere, so long `Notes`/`Details` values (29 pages) were missing from the git backup. Long text properties are now written at the top of the page body as `**Name:** value`. Commit [a2c8c86](https://github.com/aaronspriggs/spriggs-homelab/commit/a2c8c86), deployed to `~/.local/bin/kb-export`, `make check` clean; the rerun export committed the recovered text and passed gitleaks.
**Found during:** the phase 3 audit of [KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)](<../projects/KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager).md>). The audit's findings table is on that page.
**Verify:** `grep -l '^\*\*Notes:\*\*' ~/kb-export/*/*.md | wc -l` returns 29 or more.
**Roll back:** revert a2c8c86 and reinstall the script.
