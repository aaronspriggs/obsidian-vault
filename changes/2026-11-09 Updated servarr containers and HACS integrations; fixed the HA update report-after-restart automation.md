---
date: 2026-11-09
type: upgrade
system:
- '[[Home Assistant OS (VM)]]'
- '[[Servarr Stack (Docker Compose)]]'
---

# Updated servarr containers and HACS integrations; fixed the HA update report-after-restart automation

## What changed

**Containers** (HA Install on each `update.big_boi_containers_*`, one at a time, maintenance mode on): sonarr 4.0.20.3014-ls2 → ls4, radarr 6.4.4.10685-ls325 → ls326, nzbget v26.3-ls270 → ls271, prowlarr 2.7.0.5723-ls166 → ls167, gluetun-watchdog (alpine:latest re-pull). nzbget and prowlarr `NetworkMode` match Gluetun's container ID afterwards. Dockhand reports nothing pending.

**HACS:** Meross LAN v5.8.0 → v6.0.0 (multi-channel devices become one HA device per channel; entity names and IDs kept), Rivian 2.0.0 → 2.0.1, ha-dockhand v1.11.1 → v1.11.3, ha-mcp v9.0.0 → v9.1.2 (9.1.1 landed first, 9.1.2 appeared right after), Battery Notes 3.7.2 → 3.8.1, Bubble Card v3.4.3, Power Flow Card Plus v0.4.1, Clock Weather Card v3.1.0, Wall Clock Card v3.18.1. Two HA restarts. Dashboard clients (wall panel) need a hard refresh for the new cards.

**`automation.ha_updates_report_after_restart`:** the condition `states('input_text.ha_update_in_progress') | count('|') == 3` raised `TypeError: len() takes exactly one argument (2 given)` on every startup (Jinja's `count` filter is `length`, not `str.count`), so the "✅ Core updated" confirmation after an approved Core/OS update could never run. Changed to `states('input_text.ha_update_in_progress').count('|') == 3`, tested with `ha_eval_template`. No other automation uses the pattern.

**HA Core 2026.10.4 → 2026.11.0:** Aaron installed it by hand at 14:07 MST (Core/OS stay his call, decision 2026-09-25). Verified after: ha-mcp 9.1.2 connects, the fixed report-after-restart automation evaluates its condition without error (false, since this install didn't go through the approval flow), and startup shows only the known HomeKit "Kitchen" error plus deprecation warnings from rivian, dyson_local and chargepoint (break in 2027.5–2027.11). New repair: Nest `legacy_pubsub_topic` (left alone; Nest is being decommissioned).

## Why

Aaron asked for everything pending to be updated, and reported intermittent errors when installing containers from HA. None reproduced: all five installs succeeded, HA's log has no ha-dockhand errors in the last 10 days, and Dockhand's log since 2026-10-15 has one failure, a registry rate limit (`toomanyrequests`) during an image pull on 2026-11-01 09:00 MST.

## How

Rollback: HACS → redownload the previous version and restart HA. Containers: the `-ls` tags above are linuxserver tags that can be pinned in the servarr compose if needed. Startup errors after the restarts were only the known HomeKit "Kitchen" / `camera.kitchen` one.
