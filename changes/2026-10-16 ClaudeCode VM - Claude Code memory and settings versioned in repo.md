---
date: 2026-10-16
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/dc9d2ae
notion_id: 3fb7ae76-22ba-81fa-a7da-ca0ae867c3fb
---

# ClaudeCode VM: Claude Code memory and settings versioned in repo; rebuild runbook and DR index written

Plan 4 of the Claude access model, part 1. The VM disk isn't backed up and the project allow rules and Claude Code auto-memory existed only there. Memory dir ~/.claude/projects/-home-aspriggs-homelab-agent/memory is now a symlink to repo claudecode-vm/claude/memory; ~/homelab-agent/.claude/settings.local.json is a deployed copy of claudecode-vm/claude/settings.local.json (in deployed.tsv). [CLAUDE.md](http://claude.md/) now says to commit memory writes (c30d890). make check all ok. Wrote runbooks 'Rebuild the ClaudeCode VM from scratch' (desk-checked, not test-rebuilt) and 'Disaster recovery: rebuild order (index)'. Found during the inventory: the VM's IP is a UDM fixed-IP reservation on MAC 00:a0:98:1e:c7:5c, so a rebuild must reuse that MAC.
