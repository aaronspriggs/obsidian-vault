---
date: 2026-10-15
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Give Claude a scoped TrueNAS maintenance key (apps, VMs, system updates)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/28d211e
notion_id: 3fa7ae76-22ba-81f8-a21d-c04dc1bc1f7b
---

# Added TrueNAS maintenance API user claude-maint and truenas-api --write

Aaron created TrueNAS user/group claude-maint with privilege 'Claude maintenance' and stored its key in 1Password. truenas-api --write logs in as claude-maint with an allowlist (app upgrade/restart, VM start/stop/restart, OS update). Tested safely.

**TrueNAS (Aaron):** group + user `claude-maint`, privilege "Claude maintenance" (`READONLY_ADMIN`, `APPS_WRITE`, `VM_WRITE`, `SYSTEM_UPDATE_WRITE`, `POOL_SCRUB_WRITE`), API key stored in 1Password **TrueNAS API Key (claude-maint)**.
**Claude** ([28d211e](https://github.com/aaronspriggs/spriggs-homelab/commit/28d211e)): `truenas-api --write <method>` reads the key at run time via `homelab-secret`, logs in as `claude-maint`, allows only `app.upgrade/redeploy/start/stop`, `vm.start/stop/restart`, `update.download/update`, waits on jobs, logs to `~/.local/state/homelab/truenas-api.log`. Read mode unchanged (`claude-readonlyapi`).
**Verified:** login as claude-maint OK with the five roles; `core.get_methods` showed the role also allows `app.delete`, `vm.delete`, `vm.update`, registries etc. (hence the allowlist); `vm.delete` refused by the allowlist; `vm.start [4]` (Plex, running) returned "already running", logged, nothing changed.
**Findings:** `POOL_SCRUB_WRITE` only edits scrub schedules (no on-demand scrub without `POOL_WRITE`, not granted). The Dockhand TrueNAS app shows `upgrade_available` (not acted on).
