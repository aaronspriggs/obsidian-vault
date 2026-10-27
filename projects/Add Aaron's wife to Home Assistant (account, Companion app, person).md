---
type: task
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
parent: '[[Plan a home security system (Alarmo, door-window sensors, siren)]]'
next_step: '2026-10-27: Aaron says what to name her HA user and whether she should be an admin; Claude creates it on his explicit yes (Tier 3, users).'
---

## Goal

Give Aaron's wife her own Home Assistant user, the Companion app on her phone, and a `person` entity tracked by that phone. The alarm's "everyone left, arm?" push needs her presence as well as Aaron's (decided 2026-10-27).

## Status / next step

2026-10-27: not started. Only `person.aaron_spriggs` exists. Their infant daughter doesn't need tracking yet.

## Plan

1. Create her HA user (non-admin unless Aaron says otherwise), with a person entity.
2. She installs the Companion app, signs in, and allows location (Always) and notifications, including Critical Alerts so alarm and leak pushes break through Do Not Disturb.
3. Attach her phone's `device_tracker` to her person; confirm home/away flips.
4. Decide which pushes she gets: alarm, leak, maybe not homelab alerts.

## Open questions

- Admin or regular user?
- Which alerts go to her phone?
