---
status: active
category: docker
ip: 192.168.1.248
port: 3002
url: http://192.168.1.248:3002/
runs_on:
- '[[Dockhand]]'
last_verified: 2026-10-14
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks/uptime-kuma
notion_id: 3ea7ae76-22ba-81aa-ac2a-c370b72c0080
---

Homelab uptime monitor (Docker stack via Dockhand on Big Boi, :3002). 17 monitors feed HA through the Uptime Kuma integration; HA alerts only when something is down.

## Overview

Uptime Kuma watches every homelab service and host, plus push heartbeats from scheduled jobs, and feeds Home Assistant, which does the alerting. Deployed 2026-09-24 as phase 1 of "Homelab health monitoring with Home Assistant alerts (silent when nominal)". Verified via HA's Uptime Kuma integration 2026-09-29.

## Access

- UI: [http://192.168.1.248:3002/](http://192.168.1.248:3002/). Admin login (Kuma has a single user) in Aaron's password manager and, since 2026-10-14, in 1Password `Uptime Kuma` in the Claude vault. Claude uses it via `kuma-api`/`kuma-adopt` on the ClaudeCode VM (repo `uptime-kuma/`), which drive Kuma's internal [socket.io](http://socket.io/) API through AutoKuma's `kuma` CLI; Kuma's API keys only unlock `/metrics`. Monitors are code, managed by AutoKuma (see Config).
- HA reads it with a Kuma API key entered by Aaron in the HA integration (never in chat or Notion). `/metrics` needs that key.
- Push monitor URLs contain tokens: they live only in each client's config file on the ClaudeCode or Plex VM, never in Notion or the repo (gitleaks has a rule for them).

## Config

- Dockhand stack `uptime-kuma`, image `louislam/uptime-kuma:2` (tracks v2.x), host port 3002 → container 3001 (Dockhand has 3001). Default network `uptime-kuma_default` is IPv4-only (172.16.1.0/24, `enable_ipv6: false` since 2026-10-14). The IPv6 subnet that the TrueNAS pool assigned broke compose recreates, so image updates failed. Compose: [repo stacks/uptime-kuma](https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks/uptime-kuma).
- Data: SQLite in `/mnt/Big Boi/BIGBOI/uptime-kuma`, covered by the daily `BIGBOI` snapshot (30 days).
- **Monitors as code (since 2026-10-14):** a second service in the stack, AutoKuma `ghcr.io/bigboot/autokuma:2.1.0-rc.2` (files only, no Docker socket), keeps Kuma equal to repo `stacks/uptime-kuma/monitors/*.toml` (one file per monitor; file name = AutoKuma ID; never rename a file, it would recreate the monitor with a new Kuma ID and new HA entities). `stacks/uptime-kuma/render` inlines the files into `compose.yaml`; Claude deploys it with Dockhand's `PUT /api/stacks/uptime-kuma/compose` and `forceRecreate: false` (Dockhand's default recreates Kuma too). Removing a file deletes the monitor after 5 min. AutoKuma logs in with Dockhand stack secrets `KUMA_USERNAME`/`KUMA_PASSWORD`; its ID map is in `/mnt/Big Boi/BIGBOI/autokuma` (if lost, run `kuma-adopt` before restarting it, then restart Kuma). Every monitor's description says it's managed by AutoKuma; edits in the Kuma UI get reverted within 30 s. Procedure and pitfalls: repo `stacks/README.md` and `uptime-kuma/README.md`.
- **Known Kuma 2.5.6 bug:** a tag created after Kuma starts breaks Prometheus metrics for monitors carrying it (HA entities go unavailable) until Kuma restarts. Restart Kuma after creating any tag.
- **17 monitors (2026-10-14; the three JSON health monitors were deleted that day):**
    - Services: Plex, Sonarr, Radarr, Prowlarr, NZBGet, Seerr, Home Assistant, Dockhand, TrueNAS.
    - Hosts/devices: UDM Pro, ClaudeCode VM, Wall Panel Pi, HDHomeRun.
    - Push heartbeats: Plex VM Updates, ClaudeCode VM Updates (homelab-update), TrueNAS Alert Relay (900 s), KB Export (8 days).
- **Alerting lives in HA, in Alert2 (since 2026-10-09):** each monitor's `sensor.*_status` carries label `homelab_watch` (24 entities incl. UniFi device states), and Alert2 generates one alert per labelled entity (`alert2.homelab_<name>_down`, UniFi `_offline`); push heartbeats are listed explicitly in the heartbeat generator. Config: repo `ha/alert2.yaml`. **To add a monitor:** add a file under `stacks/uptime-kuma/monitors/`, render, commit and deploy (a push monitor's token then has to go into its client's config on its host), reload the Uptime Kuma integration, add the `homelab_watch` label to its `sensor.*_status`, then run `alert2.reload` (a push monitor also needs a line in the heartbeat generator and the service generator's exclusion list). Pushes 09:00–20:00 only, with a 09:00 report of overnight alerts. The old `automation.homelab_service_device_alerts` is turned off. Arr app health is no longer alerted from the three Kuma JSON health monitors: Alert2's `homelab_<app>_health` alerts use HA's own `rest:` sensors (`sensor.<app>_health_errors`/`_messages`, repo `ha/rest-arr-health.yaml`), firing after 30 min of errors and only while the app is up. The three JSON health monitors were deleted 2026-10-14 (Aaron) and their HA devices removed. Reloading the Uptime Kuma integration is safe: Alert2 conditions ignore `unavailable`.

## Dependencies

Runs on [Dockhand](<Dockhand.md>) on [TrueNAS SCALE (Big Boi)](<TrueNAS SCALE (Big Boi).md>): if Big Boi is down, Kuma is too and HA sees the integration go unavailable (one "Kuma unreachable" alert rather than one per monitor). Alerts are delivered by [Home Assistant OS (VM)](<Home Assistant OS (VM).md>).

## Decisions

- **2026-09-24:** no Docker socket mount (it would give Kuma root on TrueNAS); container events come from Dockhand instead.
- **2026-09-24:** Kuma only detects; HA decides and notifies, quietly unless something is down.
- **2026-10-09:** HA's deciding/notifying moved to Alert2 (see the "Alerting redesign" project); arr app health moved off Kuma to HA `rest:` sensors to stop polling the same endpoints twice.
- **2026-10-14 (Aaron asked; design delegated to Claude):** Claude builds and maintains the alerting stack end to end, so Kuma monitors became code via AutoKuma using the Kuma admin login. Accepted risk: AutoKuma uses Kuma's unofficial [socket.io](http://socket.io/) API, so a Kuma upgrade can break it until AutoKuma catches up (monitoring keeps working; only changes stop). After Kuma upgrades, check `kuma-api monitor list` and AutoKuma's log.
- **2026-09-25:** dropped UniFi switch/AP ping monitors; HA's UniFi integration already reports their state.

## Related

Project history: "Homelab health monitoring with Home Assistant alerts (silent when nominal)". Runbooks: homelab-update, TrueNAS read-only API and alert relay.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
