---
date: 2026-09-25
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
notion_id: 3e67ae76-22ba-81d3-a8f3-e9447cbc9807
---

# Set up read-only TrueNAS API access for Claude (claude user + Read-Only Administrator + API key); first audit findings

**Setup:**
- Aaron created a local TrueNAS user `claude` (password disabled, nologin, no sudo, not an SMB user) and gave its primary group the **Read-Only Administrator** privilege. In 25.04 the Add User form has no role field; roles are set on the group via Credentials → Groups → Edit → Privileges.
- He created a user-linked API key `claude-readonly` and piped it over SSH into `~/.config/homelab/truenas-api-key` (mode 600) on the ClaudeCode VM, so it never went through chat.
- Claude installed `python3-websocket` via apt and wrote `~/.local/bin/truenas-api`, a JSON-RPC client that's WSS-only because 25.04 revokes API keys used over HTTP.
**Verified:** it authenticates as `claude` with READONLY_ADMIN (read roles only), and a write call (`alert.dismiss`) is rejected with EACCES.
**First audit findings** (details on the TrueNAS SCALE (Big Boi) page):
- `Big Boi/ix-apps` (Dockhand stack definitions) has **no snapshot task**; its last snapshot is from 2026-01-19.
- The BIGBOI task excludes `plex_content` and `plex_recordings`.
- Snapshot retention is 30 days.
- Dockhand 1.1.4 → 1.1.34 is available.
- CRITICAL alert: the `truenas_default` certificate expired 2026-03-01.
- The pool feature-flag upgrade notice is active.
- Pool healthy, last scrub 0 errors.
- The Plex zvol is `vmstore/Plex-9wert`.
- No TrueNAS OS update is pending.
