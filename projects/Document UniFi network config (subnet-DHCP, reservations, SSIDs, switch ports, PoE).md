---
type: task
status: done
priority: medium
system:
- '[[UniFi (UDM Pro)]]'
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
- '[[U7 Pro]]'
- '[[U7-Pro-Wall-Front]]'
- '[[U7-Pro-Wall-Back]]'
completed: 2026-09-28
notion_id: 3e97ae76-22ba-8148-a7b3-e2983901b6db
---

# Document UniFi network config (subnet/DHCP, reservations, SSIDs, switch ports, PoE)

Done 2026-09-28 via the read-only unifi-api (commits 9173a49, 80f0250): subnet/DHCP, reservations, SSID, topology, per-port links and PoE on the UDM, switch and AP pages. Leftovers (two unmanaged switches, Flex 2.5G location) moved to their own Task.

## Goal

Fill the UniFi System pages with current config: subnet and DHCP range, DHCP reservations for every static device, SSIDs and bands per AP, switch port assignments and PoE per port, and where the USW Flex 2.5G 8 PoE physically sits.

## Plan

Preferred: a read-only UniFi local account or API key for Claude (stored on the ClaudeCode VM like the TrueNAS key), so the data is read live and `Last Verified` can be set. Fallback: Aaron exports screenshots.

## Open questions

Does Aaron want Claude to have read-only UniFi access?

## Changes

![[Changes.base#For this project]]
