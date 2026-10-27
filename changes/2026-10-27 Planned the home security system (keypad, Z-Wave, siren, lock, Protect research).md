---
date: 2026-10-27
type: research
system:
- '[[Home Assistant OS (VM)]]'
- '[[UniFi (UDM Pro)]]'
project:
- '[[Plan a home security system (Alarmo, door-window sensors, siren)]]'
---

# Planned the home security system (keypad, Z-Wave, siren, lock, Protect research)

**What changed:** KB only; nothing in HA was changed. The security project moved from backlog idea to an active project (priority medium) with a phased plan from Aaron's answers: Ring Keypad (2nd gen) over Z-Wave via a Home Assistant Connect ZWA-2, the three Aeotec door sensors as zones, phone arming with an "everyone left, arm?" push, the Aqara U400 lock over Matter, and a UniFi Protect Siren PoE driven by HA's native unifiprotect `siren` entity (30 s max per play, verified in uiprotect source). Added a dated reference section on UniFi Protect integration (Local vs Global Alarm Manager mode, detections as Alarmo zones, webhooks, doorbell fingerprint/NFC, community tools). New task: [Add Aaron's wife to Home Assistant (account, Companion app, person)](<../projects/Add Aaron's wife to Home Assistant (account, Companion app, person).md>). The Big Boi rebuild project now notes that both USB radios need re-mapping after the move.

**Verified live:** HA 2026.10.4; ZHA only, no Z-Wave; door sensors reporting; Protect Alarm Manager entity present (Local mode); only the G6 Instant is on Protect; no lock, siren or Alarmo.

**Later the same day:** Aaron confirmed Alarmo as the alarm brain (UniFi only for siren and cameras) and that the U400 is in Apple Home and the Aqara app, so the plan shares it to HA via Matter multi-admin. Aaron then shared the U400 to HA (Matter multi-admin from Apple Home): `lock.aqara_smart_lock_u400` is live and reads locked; battery 22%.
