---
date: 2026-10-17
type: install
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Scrypted — UniFi Camera HomeKit Bridge]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/fc7bd6f
notion_id: 3fc7ae76-22ba-81f9-b346-ec7778d2f062
---

# Installed Scrypted as an HA app (HomeKit + UniFi Protect plugins); Kuma monitor

Placement changed to the HA app after the mDNS research: TrueNAS mDNS stays on for Finder and Time Machine (Aaron). Removed the unused Big Boi stack (7510fa6). Added repository koush/scrypted and installed 09e60fb6_scrypted v0.147.0 (boot auto, watchdog on, auto-update off), with the HomeKit and UniFi Protect plugins installed via ingress. Verified _hap._tcp: Scrypted and all five of HA's HomeKit accessories announce from .218. Kuma monitor 'Scrypted' (fc7bd6f, deployed via Dockhand), sensor.scrypted_status labelled homelab_watch; update.scrypted_update labelled ha_update_approval. Backups include all apps (checked).
