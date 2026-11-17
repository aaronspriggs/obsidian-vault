---
type: task
status: active
priority: medium
system:
- '[[Dockhand]]'
next_step: '2026-11-17 (Aaron): do it at the end of December, not now. The token was created 2026-10-01 with about 90 days, so it expires around 2026-12-30 (exact date in the 1Password item); rotate it in the week of 2026-12-21, in one sitting with the TrueNAS read-only key. Both are Tier 3 and need Aaron in the UI and in 1Password. If it is missed, dockhand-api returns HTTP 401.'
parent: '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
notion_id: 3ec7ae76-22ba-817d-9049-f7f3633774e9
---

Token created 2026-10-01 with ~90-day expiry (exact date in the 1Password item 'Dockhand API token (claude)'). Before it expires: log in as claude, Profile → API tokens → Generate token, update 1Password, overwrite ~/.config/homelab/dockhand-api-token (600) on the ClaudeCode VM, then revoke the old token. Symptom if missed: dockhand-api returns HTTP 401.
