---
date: 2026-11-15
type: config
system:
- '[[ClaudeCode (VM)]]'
- '[[Claude Code (Remote Control service)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/545ffa13d6331b5c76318b204a7e42e45bf016e8
---

# Deleted the loose files on the ClaudeCode VM and the retired kb-export copies

## What changed

Step 7 of the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>). Aaron approved the list on 2026-11-15 ("yes and kb-export"); nothing was versioned. Deleted:

- `~/rack-artifact/` (4 files, 2026-11-15 04:06): an early build of the 30U rack page and three one-off patch scripts. The vault's `attachments/Rack - 30U rack layout page.html` is the later v17.
- `~/work-claude-brief.md` (2026-10-20): a brief for Aaron's work Claude Code instance, distilled from this setup. Not homelab state, and out of date after the review. It was the one item whose content existed nowhere else; Aaron was given the `scp` line before he approved.
- `~/homelab-agent/mockup.html` and `mockup2.html` (2026-09-04): design mockups for the battery card and the Home Health dashboard, which has since been built.
- `~/homelab-agent/out/` (2026-11-09): a page summarising the GPU discussion. It said itself that the decisions are in the vault (Big Boi rebuild and AV1 pipeline projects).
- `~/homelab-agent/.archive/` (2026-09): the pre-governance `CLAUDE.md`, an ha-mcp setup status and the old cheat sheet, all pointing at Notion and replaced by the vault.
- `~/homelab-agent/.claude/settings.local.json.bak` (2026-10-15): a copy from the day before the file went into git.
- `~/homelab-agent/.claude/skills/` (`design-review`, `frontend-design`, 2026-09-04): used for the mockups and never invoked in the 68 transcripts. Claude Code no longer lists them in each session.
- The retired kb-export's deployed copies: `~/.local/bin/kb-export`, `/etc/systemd/system/kb-export.service` and `kb-export.timer`. Each was compared with the repo's copy first and matched; `systemctl daemon-reload` afterwards.

Kept: the `~/kb-export` clone (its branch is on GitHub at the same commit, bd168bb) and `~/.config/kb-export/`, which go with [Revoke the unused kb-export Notion integration token](<../projects/Revoke the unused kb-export Notion integration token.md>).

## Why

The VM's disk isn't backed up, so a file outside the two repos is either lost in a rebuild or wasn't worth keeping. Each of these was superseded by the vault or git, or wasn't homelab material. Why nothing was versioned is in the project's Decisions.

## How

`rm` on the VM. Repo commit 545ffa1 updates `claudecode-vm/README.md` (no project skills) and `kb-export/README.md` (deployed copies removed).

## Verify / roll back

Verify: `ls ~` shows only `homelab`, `homelab-agent`, `kb-export` and `obsidian-vault`; `~/homelab-agent` holds only `CLAUDE.md`, `.mcp.json` and `.claude/settings.local.json`; `systemctl list-unit-files 'kb-export*'` lists nothing; `make check` is 40 of 40 ok. Roll back: the kb-export script and units reinstall from the repo's `kb-export/`. The other files can't be restored; the rack page, the GPU decisions and the dashboard live in the vault and Home Assistant.
