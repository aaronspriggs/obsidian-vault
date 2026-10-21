---
date: 2026-02-24
type: fix
system:
- '[[Dockge]]'
notion_id: 3127ae76-22ba-813e-b8b6-c5a61f1e514f
---

# Discovered Dockge not resolving DATA_PATH env var — migration to Portainer planned

DATA_PATH env var not being resolved by Dockge for /data volume mounts. Radarr/Sonarr/NZBGet containers only have /config mount, missing /data entirely. Hardcoded path in compose as workaround but Dockge not writing changes back to compose.yaml on disk. Decision: migrate stack management from Dockge to Portainer. All downloads paused, stack left running overnight. Resume tomorrow with fresh Portainer install.

## Problem

Dockge is not resolving `${DATA_PATH}` environment variable for volume mounts. As a result, Radarr, Sonarr, and NZBGet containers are missing the `/data` bind mount entirely — only `/config` is mounted. This means the containers cannot see `/data/Movies`, `/data/TV Shows`, or `/data/downloads/usenet` at all.
Confirmed via `sudo docker inspect radarr | grep -A 5 Mounts` — only one mount present.

## Root Cause

Dockge appears to not pass the `.env` file correctly when substituting variables in volume paths containing spaces. `DATA_PATH=/mnt/Big Boi/BIGBOI/plex_content` (space in path) may be the trigger. Additionally, Dockge does not appear to be writing compose edits back to the compose.yaml on disk — `docker compose up --force-recreate` from the CLI did not pick up changes made in the Dockge UI.

## Current State

- Stack is running but `/data` mount missing from all relevant containers
- All downloads paused in NZBGet
- compose.yaml on disk still has `${DATA_PATH}` — Dockge UI edits did not persist
- plex_content ownership correctly set to 3000:0 (aspriggs:root)

## Plan

Migrate stack management from Dockge to Portainer tomorrow:
1. Bring stack down cleanly
2. Install Portainer
3. Recreate stack with hardcoded `/mnt/Big Boi/BIGBOI/plex_content:/data` path
4. Resume downloads
5. Verify end-to-end import works

## Updated compose.yaml (ready to deploy)

All `${DATA_PATH}:/data` replaced with `/mnt/Big Boi/BIGBOI/plex_content:/data` in nzbget, sonarr, and radarr services. VPN vars still use env substitution from .env.
