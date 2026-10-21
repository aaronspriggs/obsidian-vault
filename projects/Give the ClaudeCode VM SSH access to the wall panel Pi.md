---
type: task
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
- '[[Raspberry Pi Wall Panel]]'
notion_id: 3e97ae76-22ba-81a2-9a9d-ff4aacd25226
---

From ClaudeCode Known Gaps (2026-09-28). Pi 192.168.1.84 only trusts Aaron's Macs; this VM has no keypair for it (checked 2026-09-28: publickey denied).

## Goal

Let Claude read and fix wall panel (TouchKio) config directly instead of Aaron pulling files.

## Plan

1. Aaron approves generating a dedicated keypair on the ClaudeCode VM (`~/.ssh/id_ed25519_wallpanel`).
2. Aaron appends the public key to the Pi's `~/.ssh/authorized_keys`.
3. Add a `Host wallpanel` entry to `~/.ssh/config` here; verify with `ssh wallpanel true`.

## Open questions

Which Pi user, and whether Claude should have sudo there (probably not; scope like `claude-maint` on Plex if needed).
