---
status: active
category: hardware
ip: 192.168.1.128
last_verified: 2026-11-23
---

UniFi PDU Pro at U22–U23 of the 30U rack, outlets facing front, in from day one of the cutover (2026-11-23). Per-outlet power readings reach HA; outlet switching doesn't (HA's UniFi user isn't an admin).

## Overview

UniFi USP PDU Pro (model code USPPDUP), ordered 2026-11-15 in place of the Tripp Lite Isobar. Fed from one of the UPS 2U's battery outlets, and everything else in the rack plugs into it (2026-11-23), so all of it rides on battery ([power plan](<../projects/Move the homelab into the 30U floor rack.md>)). Management uplink on Enterprise 48 port 28 (B14).

## Access

- UniFi Network on the UDM Pro. IP 192.168.1.128 by DHCP (controller-managed, no reservation), MAC 74:fa:29:94:02:91. Firmware 7.2.123.16565, no update pending (2026-11-23).
- HA (UniFi integration): `sensor.usp_pdu_pro_state` (labelled `homelab_watch` since 2026-11-23, alert `alert2.homelab_usp_pdu_pro_offline`), `sensor.usp_pdu_pro_ac_power_consumption`, `sensor.usp_pdu_pro_ac_power_budget` (1,875 W), and `sensor.usp_pdu_pro_outlet_<n>_outlet_power` for outlets 5–20. Outlets 1–4 are its USB outlets and have no power sensor; 5–20 are the AC outlets. No outlet switches: they need an admin UniFi user.

## Config (2026-11-23)

- Outlets aren't named in UniFi, so HA's sensors are numbered only. First read: 170.8 W total; outlet 6 102.6 W, 20 32.2 W, 5 23.1 W, 8 8.1 W, 18 2.1 W, 17 1.7 W, 15 1.1 W, the rest 0. Which device is on which outlet isn't recorded.
- **Feed (Aaron, 2026-11-23):** one UPS 2U battery outlet, and every other device in the rack plugs into the PDU, Big Boi, the UDM Pro and the Enterprise 48 included. So everything is on battery, and the PDU's 171 W against the UPS's 160 W output at the same moment is meter disagreement, not missing load. This differs from the plan (Big Boi, UDM and switch on their own battery outlets): the PDU is now a single point of failure for the whole rack, including Big Boi's power with no NUT shutdown. Outlet 6 (about 103 W) is most likely Big Boi. Whether outlets stay powered during a PDU firmware update isn't known. No reports of PDU Pro outlets dropping on their own were found (web search, 2026-11-23). The UPS 2U's outlets are relay-switchable from UniFi too but report no per-outlet power (only `name` and `relay_state`), so moving Big Boi to a UPS outlet would only move the single point of failure; the as-built layout (UPS → PDU → everything) is the standard one and stays.

## Dependencies

Fed from one UPS 2U battery outlet; feeds everything else in the rack.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
