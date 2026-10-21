---
type: task
status: done
priority: low
system:
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
completed: 2026-10-17
notion_id: 3e97ae76-22ba-8125-81db-c73a82d4119a
---

Both were unadopted UniFi Flex 2.5G switches, now adopted: Basement (port 12) and Aaron's Desk (port 13). Confirmed by MAC 2026-10-17.

## Goal

Name the two switches the USW Pro Max sees over LLDP but UniFi doesn't manage, and record where they are:
- Port 12 (1 GbE, no PoE): chassis `74:f9:2c:26:d1:73`, its "Port 9".
- Port 13 (2.5 GbE, 3.6 W PoE): chassis `74:f9:2c:96:b6:fe`, its "Port 5"; Aaron's MacBook `mbp-017446` is behind it.
Also: the physical location of the USW Flex 2.5G 8 PoE, and what's on its port 1 (100 Mb, no IP seen).
If they're UniFi gear that was never adopted, adopting them would put them in the API.

## Outcome (2026-10-17)

They were unadopted UniFi switches and are now adopted (matched by MAC via the read-only API): port 12 `74:f9:2c:26:d1:73` is **USW Flex 2.5G 8 PoE - Basement** (192.168.1.76, 1 GbE uplink), port 13 `74:f9:2c:96:b6:fe` is **USW Flex 2.5G 5 - Aaron's Desk** (192.168.1.6, 2.5 GbE). The original Flex 2.5G 8 PoE is now named "- Upstairs". Recorded on UniFi (UDM Pro). What sits on the Upstairs switch's port 1 wasn't chased.

## Changes

![[Changes.base#For this project]]
