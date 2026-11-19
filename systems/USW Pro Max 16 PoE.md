---
status: active
category: network
ip: 192.168.1.250
last_verified: 2026-09-28
notion_id: 3087ae76-22ba-81fb-ae83-e37beaa72a78
---

Core switch. SFP+ 1 uplink to UDM Pro (10 GbE); SFP+ 2 to Big Boi (10 GbE). Powers the wall APs, Flex 2.5G and wall panel Pi.

## Overview

Core distribution switch for the homelab network. Uplinked to the UDM Pro via SFP+ at 10 GbE.

## Hardware

- **Model:** UniFi USW Pro Max 16 PoE
- **IP Address:** 192.168.1.250
- **Uplink:** SFP+ 1 (10 GbE) to Dream Machine Pro SFP+ 2 (UDM port 11)
- **Firmware:** 7.5.15.17146. IP by DHCP (controller-managed). Total PoE draw 44.6 W (2026-09-28) of a 180 W budget; temperature 48 °C.

## Port Assignments (verified via UniFi API 2026-09-28; rows 4, 12, 13 and 15 re-checked 2026-11-15)

| Port | Link | PoE | Connected |
| --- | --- | --- | --- |
| 4 | down | 0.6 W | Ring keypad PoE converter (Aaron believes; 0.6 W with no data link) |
| 6 | 1 GbE | 5.0 W | Raspberry Pi wall panel `hadashboard` (192.168.1.84), PoE-powered |
| 8 | 100 Mb | 0 | Sonos (192.168.1.32) |
| 9 | 100 Mb | 0 | Sonos (192.168.1.171). Cheryl's Office Sonos (.205) also shows here, but it's wired upstairs: it reaches this port over SonosNet while STP blocks its own port (re-checked 2026-11-19) |
| 10 | down | — | USW Flex (spare, offline by design) |
| 12 | 1 GbE | 0 | USW Flex 2.5G 8 PoE - Basement (its port 9; adopted, on its own adapter) |
| 13 | 2.5 GbE | 3.5 W | USW Flex 2.5G 5 - Aaron's Desk (its port 5; PoE-powered); Aaron's MacBook `mbp-017446` sits behind it |
| 14 | 2.5 GbE | 11.2 W | U7-Pro-Wall-Front AP |
| 15 | 2.5 GbE | 15.5 W | [[USW Flex 2.5G 8 PoE]] - Upstairs (PoE-powered from this port) |
| 16 | 2.5 GbE | 9.3 W | U7-Pro-Wall-Back AP |
| 17 (SFP+ 1) | 10 GbE | — | Uplink to UDM Pro |
| 18 (SFP+ 2) | 10 GbE | — | Big Boi / TrueNAS `br0` (TrueNAS, HA, Plex and ClaudeCode VMs all appear here) |

Ports 1–3, 5, 7 and 11 are unused.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
