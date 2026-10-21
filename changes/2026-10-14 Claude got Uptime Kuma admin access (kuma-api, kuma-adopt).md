---
date: 2026-10-14
type: install
system:
- '[[Uptime Kuma]]'
- '[[Home Assistant OS (VM)]]'
project:
- '[[AutoKuma - Uptime Kuma monitors as code, managed by Claude]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/75e52e9ce760877a875e4d02fee9a8ed1bd59c84
notion_id: 3f97ae76-22ba-8131-9138-ebdc2873c430
---

# Claude got Uptime Kuma admin access (kuma-api, kuma-adopt); removed arr health monitor devices; prepared AutoKuma

What: Aaron added Kuma's admin login to 1Password (item 'Uptime Kuma', Claude vault) and deleted the Sonarr/Radarr/Prowlarr Health JSON monitors in Kuma (Kuma IDs 18-20). Claude: (1) installed AutoKuma's kuma CLI v2.1.0-rc.2 (sha256-checked) and wrappers kuma-api (read-only unless --write) and kuma-adopt on the ClaudeCode VM (repo uptime-kuma/, deployed.tsv); (2) wrote the 17 monitors as repo files stacks/uptime-kuma/monitors/*.toml + render script + compose with an AutoKuma service (commit 75e52e9, not deployed: Dockhand stack secrets for the Kuma login were denied by the auto-mode classifier); (3) rehearsed AutoKuma adoption from the VM: 17 adopted, no changes; (4) removed the three orphaned HA devices 'Sonarr/Radarr/Prowlarr Health' (11 entities each, incl. the homelab_watch-labelled *_health_status), via ha_remove_device with HA-MCP approval. Incident (Claude-caused, fixed same hour): tagging monitors for adoption hit a Kuma 2.5.6 bug: tags become Prometheus labels and the label set is fixed at Kuma start, so a new tag made metrics updates for tagged monitors throw ('Added label "AutoKuma" is not included in initial labelset'). HA lost sensor.truenas_alert_relay_status (unavailable 13:08-13:42, heartbeat alert blind for that window; pushes themselves were accepted). Fix: deleted the tag, restarted the uptime-kuma container via Dockhand at 13:40; all 14 non-weekly monitors up in HA by 13:43. Weekly heartbeats (Plex VM updates, ClaudeCode VM updates, KB export) are unavailable in HA until their next push, as after any Kuma restart (also since this morning's 08:48 recreate). Procedure updated (commit 7fc4f29): tag only right before AutoKuma's first start, then restart Kuma. Verify: kuma-api monitor list shows 17, tag list empty; homelab_watch has 24 entities.
