---
status: active
category: network
ip: 192.168.1.24
last_verified: 2026-11-19
notion_id: 3087ae76-22ba-81b9-a191-ebeeb66ad5df
---

Upstairs switch (UniFi name "USW Flex 2.5G 8 PoE - Upstairs"), in the upstairs utility room. Uplinked to USW Pro Max port 15 at 2.5 GbE and powered by PoE from it. Hosts the U7 Pro - Upstairs AP.

## Overview

Feeds the second floor: the U7 Pro - Upstairs AP and the other 2nd-floor runs. It takes its power from Pro Max port 15 (15.5 W drawn, 2026-11-15), which caps its own PoE budget at 46 W. A second, identical model sits in the rack: "USW Flex 2.5G 8 PoE - Basement" (verified live 2026-11-15) runs on its own adapter with a 196 W PoE budget, uplinked at 1 GbE to Pro Max port 12 with nothing else connected yet; it has no note of its own yet, and its planned use is in [[Re-terminate and label the patch panels for the 30U rack]].

## Hardware

- **Model:** UniFi USW Flex 2.5G 8 PoE
- **IP Address:** 192.168.1.24
- **Uplink:** its port 9 (2.5 GbE) to USW Pro Max port 15
- **Firmware:** 2.1.8.971. IP by DHCP (controller-managed). PoE draw 8.4 W of a 46 W budget (2026-11-15).

## Port Assignments (verified via UniFi API 2026-11-15)

- Port 1: Cheryl's Office Sonos One SL (MAC 38:42:0b:1f:31:a6, 192.168.1.205), 100 Mb. STP holds this port in `discarding`: the Sonos also links over SonosNet to the wired kitchen Sonos on Pro Max ports 8 and 9, which makes a loop, so UniFi lists the Sonos on Pro Max port 9 instead (verified 2026-11-19; see the change note of that date)
- Port 3: U7 Pro - Upstairs AP, 2.5 GbE, 8.4 W PoE
- Port 9: uplink to Pro Max port 15, 2.5 GbE
- Other ports unused

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
