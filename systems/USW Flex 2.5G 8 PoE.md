---
status: active
category: network
ip: 192.168.1.24
last_verified: 2026-11-23
notion_id: 3087ae76-22ba-81b9-a191-ebeeb66ad5df
---

Upstairs switch (UniFi name "USW Flex 2.5G 8 PoE - Upstairs"), in the upstairs utility room. Uplinked to [USW Enterprise 48 PoE](<USW Enterprise 48 PoE.md>) port 38 (patch B19) at 2.5 GbE since the 30U cutover (2026-11-23), powered by its 210 W adapter since 2026-11-23 (on an extension cord until the utility room gets an outlet), with PoE from port 38 as an automatic fallback. Hosts the U7 Pro - Upstairs AP.

## Overview

Feeds the second floor: the U7 Pro - Upstairs AP and the other 2nd-floor runs. Until 2026-11-22 it took PoE++ from Pro Max port 15 (15.5 W drawn, 2026-11-15), which left it a 46 W PoE budget. Since the cutover it takes 802.3at (Class 4) from Enterprise 48 port 38, which leaves 16 W total and 12 W effective for its own ports: too little for the U7 Pro (up to 21 W), which has been rebooting on it (2026-11-23). On its 210 W adapter the budget is 196 W. A second, identical model sits in the rack: "USW Flex 2.5G 8 PoE - Basement" (verified live 2026-11-15) runs on its own adapter with a 196 W PoE budget, uplinked at 1 GbE to Pro Max port 12 with nothing else connected yet; it has no note of its own yet, and its planned use is in [[Re-terminate and label the patch panels for the 30U rack]].

## Hardware

- **Model:** UniFi USW Flex 2.5G 8 PoE
- **IP Address:** 192.168.1.24
- **Uplink:** its port 9 (2.5 GbE) to USW Pro Max port 15
- **Firmware:** 2.1.8.971. IP by DHCP (controller-managed). PoE draw 8.6 W of a 196 W budget on the adapter (2026-11-23).

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
