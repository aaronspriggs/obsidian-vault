---
type: task
status: active
priority: low
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[Uptime Kuma]]'
parent: '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
next_step: '2026-10-17: Sonarr/Radarr passed via one-tap Install on 10-16. Remaining: Install the pending NZBGet update (Aaron taps, or Claude runs it on request), then Claude checks NetworkMode still matches Gluetun''s ID. After that, pick the default method with Aaron.'
notion_id: 3f97ae76-22ba-8182-a6da-e1491dfaf00a
---

HA Install = ha-dockhand calling POST /api/containers/batch-update-stream for one container (pull + recreate of that container only). Gluetun is opted out via dockhand.update=false (2026-10-14), so Install isn't offered for it.

## Why

Aaron sees Dockhand image updates in HA's system updates and wants to know if clicking Install there is a better routine than Claude's whole-stack `POST /api/stacks/<stack>/deploy {pull, forceRecreate}`. Both work; this trial collects evidence to pick a default.

## How HA Install works (verified 2026-10-14 from `custom_components/dockhand/update.py`)

- Each `update.big_boi_containers_<name>` entity's Install calls Dockhand's `POST /api/containers/batch-update-stream` with that one container ID. Dockhand pulls the container's current tag and recreates only that container with its existing config. It runs a vulnerability scan if a scanner is configured, and HA polls `/api/jobs/<id>` for progress.
- It doesn't go through compose, so the compose-network bug from 2026-10-14 (Kuma's IPv6 gateway) doesn't apply.
- Install is hidden for system containers (ix-dockhand) and for any container labelled `dockhand.update=false`.
- Claude can trigger the same thing with ha-mcp `ha_manage_updates(action="install", entity_ids=[...])`. HA's "Update all" button also exists and skips opted-out containers.

## Gluetun exception

NZBGet and Prowlarr use `network_mode: service:gluetun`, which pins them to Gluetun's container ID. If Gluetun were recreated alone, its ID would change and both would be left without a network. `gluetun-watchdog` only runs `docker restart`, which can't reattach them. So Gluetun carries `dockhand.update=false` (repo commit fc7e579), and a Gluetun update means a servarr stack deploy as before. Updating NZBGet or Prowlarr alone is fine: they rejoin the current Gluetun.

## One-tap Install (2026-10-14)

Since 2026-10-14 the container-update pushes (Alert2 alert + 09:00 report) carry an **Install** button that runs this same HA Install via `automation.homelab_container_update_on_approval` (see [One-tap approval notifications](<One-tap approval notifications (updates and similar).md>)). So the next round will most likely be Aaron tapping Install on his phone. Claude should still run the checks in step 3 afterwards and record the results here.

## Test plan (next update round)

1. Note what's pending (`dockhand-api "/api/containers/pending-updates?env=1"` or HA's update list) and current image IDs.
2. Install each flagged container from HA (Aaron clicks it, or Claude uses `ha_manage_updates`). If Gluetun is flagged, deploy the servarr stack instead.
3. Check: the new image ID, the container is running/healthy, and for NZBGet/Prowlarr that `NetworkMode` still matches Gluetun's ID. Check the UIs, the Kuma monitors and any HA alerts. Check the HA entity drops back to `off` and the Dockhand pending list clears.
4. Write down how long it took, the downtime per container, and any errors (vulnerability-scan blocks, HA timeouts, stale entity state).

## Results so far

- **2026-10-16, Sonarr + Radarr (Aaron's one-tap Install):** both pulled and recreated alone about 20 s apart. Healthy afterwards (`/api/v3/health` empty), HA entities back to `off`, no errors. Downtime wasn't measured (no trace stored). See [2026-10-16 Updated Sonarr and Radarr images via HA one-tap Install](<../changes/2026-10-16 Updated Sonarr and Radarr images via HA one-tap Install.md>).
- **Still untested:** NZBGet or Prowlarr, where the `NetworkMode` check against Gluetun's ID is the real risk. NZBGet has been flagged since 2026-10-16 22:01 MDT.

## Decide afterwards

Compare with the stack deploy, which updates everything in one step (~45 s for servarr) but recreates every container in the stack even when only one has a new image. Options: HA Install as the default, stack deploy as the default, or a mix (HA for single containers, stack deploy when Gluetun or most of the stack is flagged). Record the decision in the servarr runbook.

## Changes

![[Changes.base#For this project]]
