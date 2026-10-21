---
date: 2026-10-16
type: upgrade
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[Uptime Kuma]]'
project:
- '[[Trial HA Install (Dockhand update entities) for container image updates]]'
notion_id: 3fc7ae76-22ba-8184-9c3c-cc8b66047663
---

# Updated Sonarr and Radarr images via HA one-tap Install

First real use of HA Install on update.big_boi_containers_*: Aaron tapped Install on the container-update push 2026-10-16 ~14:04 MDT. Logged retroactively 2026-10-17 by Claude after a live check.

## What changed

Sonarr (now 4.0.20.3014) and Radarr (now 6.4.4.10685) were pulled and recreated on Big Boi at 2026-10-16 20:04 UTC (14:04 MDT), one container each, through HA's Install on `update.big_boi_containers_sonarr` / `_radarr`. The Install push came from `automation.homelab_container_update_on_approval` (last triggered 14:04:18 MDT). The update was flagged 2026-10-15 22:02 MDT.

## Why

Dockhand flagged new `lscr.io/linuxserver/*:latest` images. This is also the first real run of the trial task's HA Install method.

## How

Aaron tapped Install on his phone. ha-dockhand called Dockhand's `POST /api/containers/batch-update-stream` for each container. No stack deploy.

## Verify / roll back

Verified 2026-10-17 by Claude: Dockhand shows both containers running, created 20:04:07 and 20:04:26 UTC; `/api/v3/health` returns `[]` for both; both HA update entities returned to `off` (Sonarr 14:04:08, Radarr 14:04:27 MDT). Downtime per container wasn't measured: no automation trace was stored, so the tap time is unknown. Roll back by pinning the previous image tag in the servarr compose file and redeploying the stack.
