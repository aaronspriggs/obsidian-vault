---
type: project
status: done
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
completed: 2026-10-15
notion_id: 3f97ae76-22ba-8129-b036-caf9ea3f3fdb
---

Built 2026-10-15: TrueNAS user claude-maint (privilege 'Claude maintenance'), key in 1Password, truenas-api --write with allowlist (app upgrade/restart, VM start/stop/restart, TrueNAS OS update). Read-only user renamed to claude-readonlyapi. Tiers unchanged. On-demand scrubs not possible without POOL_WRITE (not granted). Runbook: 'TrueNAS API access (read-only + maintenance writes) and alert relay'.

## Outcome

Done 2026-10-15. Claude has a second TrueNAS identity, `claude-maint` (privilege "Claude maintenance": `READONLY_ADMIN`, `APPS_WRITE`, `VM_WRITE`, `SYSTEM_UPDATE_WRITE`, `POOL_SCRUB_WRITE`), whose key lives only in 1Password and is used via `truenas-api --write`. The tool allowlists app upgrade/restart/start/stop, VM start/stop/restart and TrueNAS OS update; everything else the roles allow (deleting/reconfiguring apps and VMs, registries) is refused. Writes are logged and follow the KB Standards tiers. The read-only user was renamed `claude` → `claude-readonlyapi` (same key). Aaron added the `truenas-api --write` permission lines on 2026-10-15. On-demand scrubs turned out to need `POOL_WRITE` (not granted), so scrubs stay on their schedules.

## Decisions

- 2026-10-14 (Aaron): scope = apps, VMs, OS updates (+ scrubs, which the role can't start on demand); **no snapshots**; change-authority tiers unchanged.
- 2026-10-14 (Aaron): two TrueNAS accounts, so the relay's always-on, on-disk key stays read-only and the audit log separates background reads from maintenance writes.
- `VM_WRITE` and `APPS_WRITE` have nothing narrower in TrueNAS 25.04; the client allowlist is the guard (same model as `dockhand-api --write`).
- 2026-10-14: TrueNAS error tracebacks echo the API key, so both TrueNAS tools print/log only the error reason.

## Links

- Runbook: [TrueNAS API access (read-only + maintenance writes) and alert relay](<../runbooks/TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM).md>)
- Changes: [claude-maint + --write](<../changes/2026-10-15 Added TrueNAS maintenance API user claude-maint and truenas-api --write.md>), [read-only user rename + error redaction](<../changes/2026-10-14 Renamed TrueNAS read-only API user to claude-readonlyapi.md>)
- Commits: [28d211e](https://github.com/aaronspriggs/spriggs-homelab/commit/28d211e), [cd0a113](https://github.com/aaronspriggs/spriggs-homelab/commit/cd0a113), [548b601](https://github.com/aaronspriggs/spriggs-homelab/commit/548b601)
- Follow-ups: [Decide backup for the Dockhand TrueNAS app upgrade, then upgrade it](<Decide backup for the Dockhand TrueNAS app upgrade, then upgrade it.md>), [Rotate the TrueNAS read-only API key](<Rotate the TrueNAS read-only API key (claude-readonlyapi).md>). One-tap TrueNAS update approvals remain an idea from the closed project "One-tap approval notifications".

## Changes

![[Changes.base#For this project]]
