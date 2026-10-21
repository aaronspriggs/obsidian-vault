---
date: 2026-10-07
type: fix
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/a79429e
notion_id: 3f27ae76-22ba-8186-8824-c99fc3bf81f2
---

# Changed 1Password lookups to vault/item IDs after an item rename broke dockhand-api

What: `homelab-secret` now reads op://<vault ID>/<item ID>/<field>, and dockhand-api, unifi-api and claude-remote-control-start pass item IDs (titles kept in comments and READMEs). Why: Aaron renamed 'Dockhand API token' to 'Dockhand API token (Claude Code)' when adding the HA token, and dockhand-api failed with "isn't an item in the vault". IDs survive renames. Verify: dockhand-api /api/environments, unifi-api stat/health and the HA-MCP URL lookup all succeeded after deploy; `make check` clean. Note: the ha-mcp URL is only read at service start, so it kept working throughout.
