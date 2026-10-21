---
type: task
status: backlog
priority: medium
system:
- '[[Dockhand]]'
parent: '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
notion_id: 3ec7ae76-22ba-817d-9049-f7f3633774e9
---

Token created 2026-10-01 with ~90-day expiry (exact date in the 1Password item 'Dockhand API token (claude)'). Before it expires: log in as claude, Profile → API tokens → Generate token, update 1Password, overwrite ~/.config/homelab/dockhand-api-token (600) on the ClaudeCode VM, then revoke the old token. Symptom if missed: dockhand-api returns HTTP 401.
