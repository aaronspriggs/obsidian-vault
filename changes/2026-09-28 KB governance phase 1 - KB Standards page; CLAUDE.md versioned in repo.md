---
date: 2026-09-28
type: doc
system:
- '[[ClaudeCode (VM)]]'
notion_id: 3e97ae76-22ba-81ee-bd93-d09d3017ed5e
---

# KB governance phase 1: KB Standards page; CLAUDE.md versioned in repo

Created KB Standards; trimmed [CLAUDE.md](http://claude.md/) Notion section to hard rules + link; [CLAUDE.md](http://claude.md/) now in repo (commit 9e10db8).

**What:** Phase 1 of [KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)](<../projects/KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager).md>).
- Created [STANDARDS](<../STANDARDS.md>) (subpage of the homepage): operating model, page skeletons per database, required properties (phase 2 properties marked), writing rules (absolute dates, rewrite not append, 1,500-word split), secrets policy (1Password / Proton Authenticator), edit-safety rules, lifecycle, and who does what between Claude Code and Cowork.
- `CLAUDE.md`: the Notion section is now the hard rules plus a link to KB Standards; added the session-start `HEALTH.md` read and the edit-safety rules (phase 0 step 2). The "Page organization" section moved to KB Standards.
- `CLAUDE.md` moved into the repo at [claudecode-vm/CLAUDE.md](https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/CLAUDE.md), commit [9e10db8](https://github.com/aaronspriggs/spriggs-homelab/commit/9e10db8).
**Symlink:** Aaron replaced `~/homelab-agent/CLAUDE.md` with a symlink to the repo copy on 2026-09-28 (Claude Code's auto mode blocks it from replacing its own instructions); verified by Claude Code the same day. Pre-change copy kept at `~/homelab-agent/.archive/CLAUDE.md.pre-phase1`.
**Cowork:** Aaron replaced the Cowork project instructions on 2026-09-28 with a merged version that points to KB Standards (it adds the two-Claudes split, writing rules and secrets policy), and removed the attached `homelab-cheatsheet.md` and `homelab-notion-kb-guide.md`. Before removal, every cheatsheet gotcha was confirmed present in the KB export; the cheatsheet was already stale (HA 2026.9.0, "Proton Pass").
**Verify:** `readlink ~/homelab-agent/CLAUDE.md` points at `~/homelab/claudecode-vm/CLAUDE.md`.
