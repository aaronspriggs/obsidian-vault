---
date: 2026-10-23
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
project:
- '[[One-tap approval notifications (updates and similar)]]'
---

# 09:00 report batches overnight container updates into one Update all push

Aaron, 2026-10-23: the morning after Dockhand's 04:00 check flagged five image updates he got six pushes (one Install push per container plus the overnight summary listing the same five) and had no way to install them together; only the Sunday report had Update all. He asked for overnight updates to arrive as one summary with Update all, and daytime updates to stay single.

`automation.homelab_alerts_09_00_report` (UI, not in repo) now computes `updates` (installable pending `update.big_boi_containers_*`, Gluetun excluded, and which of them appeared overnight by their Alert2 alert's `last_on_time`) and drops those Alert2 update alerts from the overnight still-open/cleared list. If any appeared overnight it sends one push: with exactly one pending, the old single Install push (`CONTAINER_UPDATE`, tag `alert2.homelab_<name>_update`); with two or more, "⬆️ N container updates available" listing every pending one, subtitle "👆 Tap to Update all (N)", buttons **Update all (N)** (`CONTAINER_UPDATE_ALL`, existing `automation.homelab_container_update_all_on_approval`) and Open dashboard, tag `homelab-morning-updates`. The overnight summary only goes out if something other than those updates happened. Daytime update alerts are unchanged (Alert2 pushes one per container with Install). Gluetun's button-less update alert still shows in the overnight list. The Update all handler's description now names both entry points.

**Verified:** ran the report's actions at 15:30 UTC with the five updates still pending (radarr, nzbget, prowlarr, seerr, gluetun-watchdog): the trace shows the overnight push skipped (nothing else open) and one push "⬆️ 5 container updates available" with Update all (5). **First real Update all (Aaron's tap, 15:31 UTC):** handler finished in 59 s with ✅ for all five. Afterwards every `update.big_boi_containers_*` is `off`, Dockhand's pending list is empty, all five containers running (seerr healthy), NZBGet and Prowlarr `NetworkMode` = `container:a808b3e0e6af…` = Gluetun's current ID, no Alert2 alert fired. Radarr's health showed a stale 'Unable to communicate with NZBGet' (Radarr was recreated 9 s before NZBGet); Claude ran `CheckHealth` on Radarr and Sonarr and both came back empty.
