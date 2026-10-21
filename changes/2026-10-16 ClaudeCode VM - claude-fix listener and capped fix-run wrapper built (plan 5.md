---
date: 2026-10-16
type: install
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/b86831c
notion_id: 3fb7ae76-22ba-81c4-9b53-f3b14ea57694
---

# ClaudeCode VM: claude-fix listener and capped fix-run wrapper built (plan 5 step 1)

Plan 5 step 1 of the Claude access model. New ~/.local/bin/claude-fix (repo claudecode-vm/claude-fix): `serve` listens on :8765 for POST /fix {alert_id} with a bearer token, from HA (192.168.1.218) and [localhost](http://localhost/) only; GET /health for Kuma. The ID must be in ~/.config/homelab/claude-fix-runbooks.json (allowlist, empty until the pilot runbook); no alert text reaches the prompt. `run <ID>` enforces the caps: one run at a time (flock), 3 started runs per rolling 24h, --max-turns 30, --max-budget-usd 1.00 (backstop until step 4 measures), 20 min wall clock, Sonnet, --permission-mode dontAsk with the entry's tools plus the Notion tools. --setting-sources user,project keeps settings.local.json's --write allow rules out of fix runs. Outcomes (incl. refusals) go to an HA webhook. Tested: fake-claude end to end (401/403/404/400, lock refusal, cap refusal, result parsing) and one real Haiku smoke run ($0.035, 2 turns): dockhand-api --write denied, ha-mcp and Notion connected. Unit claude-fix-listener.service installed, not enabled: it needs the 1Password item 'Claude fix listener' (password = bearer token, webhook_id) that Aaron creates. make check ok.
