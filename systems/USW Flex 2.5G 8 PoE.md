---
status: active
category: network
ip: 192.168.1.24
last_verified: 2026-09-28
notion_id: 3087ae76-22ba-81b9-a191-ebeeb66ad5df
---

Secondary switch. Uplinked to USW Pro Max Port 15 via 2.5 GbE. Hosts U7 Pro AP.

## Overview

Secondary switch that feeds the U7 Pro AP. Uplinked to the USW Pro Max 16 PoE. Physical location not yet recorded.

## Hardware

- **Model:** UniFi USW Flex 2.5G 8 PoE
- **IP Address:** 192.168.1.24
- **Uplink:** its port 9 (2.5 GbE) to USW Pro Max port 15
- **Firmware:** 2.1.8.971. IP by DHCP (controller-managed). Total PoE draw 8.6 W.

## Port Assignments (verified via UniFi API 2026-09-28)

- Port 1: link up at 100 Mb, no PoE draw, no client identified (a device without an IP, or a dumb device)
- Port 3: U7 Pro AP, 2.5 GbE, 8.6 W PoE
- Port 9: uplink
- Other ports unused

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
