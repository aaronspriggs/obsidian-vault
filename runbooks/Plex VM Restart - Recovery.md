---
kind: recovery
status: deprecated
system:
- '[[Plex Media Server]]'
notion_id: 2ff7ae76-22ba-81ad-8cc9-d3df01ad4173
---

# Plex VM Restart / Recovery

**Deprecated 2026-09-28:** a generic stub that was never filled in or tested (KB governance decision 3). See [Updating the Plex VM (OS + Plex)](<Updating the Plex VM (OS + Plex).md>) and the [Plex Media Server](<../systems/Plex Media Server.md>) page.

## Preconditions

- TrueNAS SCALE (Big Boi) is online and storage pools are healthy.
- Network connectivity to Plex clients is available.

## Procedure

1. Log into TrueNAS SCALE UI and navigate to Virtualization → Virtual Machines.
2. Gracefully stop the Plex VM if it is running.
3. Start the Plex VM and wait for guest OS boot completion.

## Verification

- Confirm Plex web UI loads and libraries are accessible.
- Test playback from at least one client.

## Failure Modes & Recovery

- If Plex UI does not load, verify VM IP and guest OS services.
