---
type: project
status: done
priority: medium
system:
- '[[Uptime Kuma]]'
parent: '[[Alerting redesign - one dispatcher, one detector per symptom, label-driven alerts]]'
next_step: 'Done 2026-10-14: AutoKuma deployed, 17 monitors adopted in place, edit path tested. Follow-up lives on the Uptime Kuma page (check AutoKuma after Kuma upgrades).'
completed: 2026-10-14
notion_id: 3f97ae76-22ba-8171-a947-c454fa2a153e
---

# AutoKuma: Uptime Kuma monitors as code, managed by Claude

Aaron 2026-10-14: wants Claude to build and maintain the whole alerting stack without manual UI steps. Kuma has no management API (API keys only unlock /metrics), so this uses AutoKuma (BigBoot/AutoKuma), which drives Kuma's internal [socket.io](http://socket.io/) API with the single admin login (1Password 'Uptime Kuma', Claude vault).

## Goal

Monitors are defined in the repo and applied automatically, so Claude can add, change or remove a monitor end to end (repo file → deploy → Kuma → HA label → Alert2) without Aaron opening Kuma.

## Design (decided 2026-10-14, Claude, delegated by Aaron)

- AutoKuma v2.1.0-rc.2 as a second service in the Dockhand `uptime-kuma` stack. RC chosen over stable 2.0.0 because it has the fixes this setup depends on: reconnect after Kuma restarts, `@/file` secrets, file preprocessing. Pinned tag.
- Files source only (`AUTOKUMA__DOCKER__ENABLED=false`): no Docker socket, per the 2026-09-24 decision.
- One TOML file per monitor in repo `stacks/uptime-kuma/monitors/`; file name = AutoKuma ID. `stacks/uptime-kuma/render` inlines them into `compose.yaml` as Compose `configs:` (Dockhand bundles Compose 5.x), so deploying the stack ships them. No Git-stack conversion needed.
- Existing 17 monitors are adopted in place (same Kuma IDs, so HA's Uptime Kuma entities don't change): `kuma-adopt` tags them `AutoKuma=<id>`, and AutoKuma's one-time v1 migration (`AUTOKUMA__MIGRATE=true`, empty /data) maps them. Rehearsed on the ClaudeCode VM: 17 adopted, then 75 s of syncs with zero creates/updates.
- AutoKuma merges each file over the live monitor, but the client fills unset fields with defaults (interval 60, 200-299, …), so files state every field. `push_token` is the exception: absent on purpose so Kuma keeps the token the clients use.
- `on_delete=delete` with a 300 s grace period. AutoKuma's ID map lives in `/mnt/Big Boi/BIGBOI/autokuma` (snapshotted); if it's lost, run `kuma-adopt` before restarting AutoKuma or it creates duplicates.
- Credentials: Dockhand stack secrets `KUMA_USERNAME`/`KUMA_PASSWORD` (encrypted in Dockhand's DB, injected at deploy).
- Risks accepted: Kuma calls the [socket.io](http://socket.io/) API unsupported for third parties, so a Kuma upgrade can break AutoKuma until it catches up (monitoring keeps working; only changes stop). Check after Kuma upgrades.

## Done so far (2026-10-14)

- Aaron created the Kuma login item and deleted the three JSON health monitors.
- `kuma-api` (read-only unless `--write`) and `kuma-adopt` on the ClaudeCode VM; repo `uptime-kuma/`.
- Monitor files, render script, compose with AutoKuma: commit 75e52e9 (not yet deployed).
- Orphaned HA devices Sonarr/Radarr/Prowlarr Health removed.
- Kuma bug found: a tag created after Kuma's start breaks Prometheus metrics for tagged monitors until Kuma restarts (HA entities go unavailable). The adoption tag was removed again and Kuma restarted; tag only right before AutoKuma's first start, then restart Kuma.

## Remaining

1. Stack secrets (blocked, see Next Step).
2. `kuma-adopt`, then immediately deploy via `PUT /api/stacks/uptime-kuma/compose` (restart true); check AutoKuma logs ("Migrating 17 monitors", no creates), that the 17 monitor IDs are unchanged and the tag is gone; then restart the uptime-kuma container and confirm HA's Kuma sensors are up.
3. Update the Uptime Kuma system page (monitor count 17, new add-a-monitor procedure) and close this out.

## Changes

![[Changes.base#For this project]]
