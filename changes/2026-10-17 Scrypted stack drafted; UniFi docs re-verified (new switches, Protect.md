---
date: 2026-10-17
type: doc
system:
- '[[UniFi (UDM Pro)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Home Assistant OS (VM)]]'
project:
- '[[Scrypted — UniFi Camera HomeKit Bridge]]'
- '[[Identify two unmanaged switches on USW Pro Max ports 12 and 13]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/2e60b6b
notion_id: 3fc7ae76-22ba-81fe-aabd-ca27e14d3120
---

# Scrypted stack drafted; UniFi docs re-verified (new switches, Protect, HA integration)

Added stacks/scrypted/compose.yaml (not deployed): host networking, SCRYPTED_DOCKER_AVAHI=true, ./volume, no watchtower, json-file logs. Scrypted project set to Blocked on Aaron's steps; decisions recorded (HKSV on, UniFi Protect into HA now via API key only, TrueNAS mDNS to be turned off). UDM page: 10 adopted devices incl. the newly adopted Flex 2.5G Basement and Aaron's Desk switches (were the 'unmanaged' switches on Pro Max ports 12/13; task closed Done), Protect section (G6 Instant), HA UniFi Network integration details and the alerting gap for the two new switches.
