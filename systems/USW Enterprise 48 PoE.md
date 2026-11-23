---
status: active
category: network
ip: 192.168.1.79
last_verified: 2026-11-23
---

Core switch since the 30U cutover (2026-11-23), at U29 between patch panels A and B. 48× 2.5 GbE PoE+, 4× SFP+. SFP+ 4 uplinks to UDM Pro SFP+ 11 and SFP+ 2 to Big Boi, both 10G DAC. Replaced the USW Pro Max 16 PoE, the USW Aggregation and the Basement Flex.

## Overview

UniFi USW Enterprise 48 PoE (model code US648P), bought 2026-11-15 ($851) so every port runs 2.5 GbE PoE+ for Ting's 2 Gbps ([why](<../projects/Re-terminate and label the patch panels for the 30U rack.md>)). Every house run and in-rack device patches to it through panels A and B; port numbers follow patch map v12 (A n = port 2n−1, B n = port 2n, confirmed live 2026-11-23). On a UPS 2U battery outlet per the plan.

## Access

- UniFi Network on the UDM Pro. IP 192.168.1.79 by DHCP (controller-managed, no reservation, like the other UniFi devices), MAC 0c:ea:14:b3:e6:2a. Read through `unifi-api stat/device`; Claude has no UniFi write route.
- HA (UniFi integration, non-admin, so no PoE or port controls): `sensor.usw_enterprise_48_poe_state` (labelled `homelab_watch`, so Alert2's `alert2.homelab_usw_enterprise_48_poe_offline` covers it since 2026-11-23), `_temperature`, `_cpu_utilization`, `_memory_utilization`, `_uptime`, `update.usw_enterprise_48_poe_firmware`.

## Config (2026-11-23)

- Firmware 7.6.11.17272, no update pending.
- **STP:** RSTP, priority 32768 (the default). The retired Pro Max 16 had 4096 and the Upstairs Flex has 8192, so this core switch no longer has the lowest priority. See Open work in the patch panel project.
- Port use is in [the patch panel project](<../projects/Re-terminate and label the patch panels for the 30U rack.md>) (map v12). Port names aren't set in UniFi yet.
- Temperature 143.6 °F (62 °C) on the first read after the cutover, with 42 W of PoE out. The rack-heat question (top venting or a roof fan) is open in [the rack project](<../projects/Move the homelab into the 30U floor rack.md>); HA's history of `sensor.usw_enterprise_48_poe_temperature` is the data for it.

## Dependencies

Everything on the LAN except the UDM Pro itself depends on it: Big Boi (and so HA, Plex and this VM), every AP, the downstream Flex switches, the hubs. Single point of failure, accepted 2026-11-15 (Aaron).

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
