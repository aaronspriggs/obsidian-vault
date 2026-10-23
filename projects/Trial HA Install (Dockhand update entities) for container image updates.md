---
type: task
status: done
priority: low
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[Uptime Kuma]]'
parent: '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
completed: 2026-10-23
notion_id: 3f97ae76-22ba-8182-a6da-e1491dfaf00a
---

# Trial HA Install (Dockhand update entities) for container image updates

Done 2026-10-23.

## Outcome

HA Install (ha-dockhand's `update.big_boi_containers_<name>`, which calls Dockhand's `POST /api/containers/batch-update-stream` for one container: pull + recreate that container only) works for every servarr container. Sonarr and Radarr passed via one-tap Install on 2026-10-16. Radarr, NZBGet, Prowlarr, Seerr and gluetun-watchdog passed via one-tap Update all on 2026-10-23 (59 s, one at a time). NZBGet and Prowlarr kept `NetworkMode: container:<Gluetun's ID>`, which was the main risk. The only side effect was a stale Radarr health error about NZBGet that cleared on the next health check. Gluetun is opted out (`dockhand.update=false`) because recreating it alone strands NZBGet and Prowlarr.

## Decisions

- **2026-10-14 (Aaron):** nightly snapshots are the safety net, not a pre-update snapshot.
- **2026-10-23 (Aaron):** HA Install is the default for routine image updates. Daytime: one Install push per container from Alert2. Anything still pending at 09:00: one push with Update all (N). Whole-stack deploy only when Gluetun has an update. Recorded in runbook [Managing the Servarr Docker Stack](<../runbooks/Managing the Servarr Docker Stack.md>).

## Links

- [2026-10-16 Updated Sonarr and Radarr images via HA one-tap Install](<../changes/2026-10-16 Updated Sonarr and Radarr images via HA one-tap Install.md>)
- [2026-10-23 09-00 report batches overnight container updates into one Update all push](<../changes/2026-10-23 09-00 report batches overnight container updates into one Update all push.md>)

## Changes

![[Changes.base#For this project]]
