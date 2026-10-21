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
- **Firmware:** 7.5.15.17146. IP by DHCP (controller-managed). Total PoE draw 44.6 W; temperature 48 °C.

## Port Assignments (verified via UniFi API 2026-09-28)

| Port | Link | PoE | Connected |
| --- | --- | --- | --- |
| 6 | 1 GbE | 5.0 W | Raspberry Pi wall panel `hadashboard` (192.168.1.84), PoE-powered |
| 8 | 100 Mb | 0 | Sonos (192.168.1.32) |
| 9 | 100 Mb | 0 | Sonos ×2 (192.168.1.205, .171), so something daisy-chained or a small switch |
| 10 | down | — | USW Flex (spare, offline by design) |
| 12 | 1 GbE | 0 | Unidentified non-adopted switch (LLDP chassis 74:f9:2c:26:d1:73, its "Port 9") |
| 13 | 2.5 GbE | 3.6 W | Unidentified non-adopted switch (LLDP chassis 74:f9:2c:96:b6:fe, its "Port 5"); Aaron's MacBook `mbp-017446` sits behind it |
| 14 | 2.5 GbE | 11.2 W | U7-Pro-Wall-Front AP |
| 15 | 2.5 GbE | 15.5 W | USW Flex 2.5G 8 PoE |
| 16 | 2.5 GbE | 9.3 W | U7-Pro-Wall-Back AP |
| 17 (SFP+ 1) | 10 GbE | — | Uplink to UDM Pro |
| 18 (SFP+ 2) | 10 GbE | — | Big Boi / TrueNAS `br0` (TrueNAS, HA, Plex and ClaudeCode VMs all appear here) |

Ports 1–5, 7 and 11 are unused.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
