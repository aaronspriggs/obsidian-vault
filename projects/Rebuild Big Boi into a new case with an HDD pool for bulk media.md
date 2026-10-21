---
type: project
status: backlog
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 3fa7ae76-22ba-811b-9baa-c2e05b8e9c2e
---

Decided by Aaron 2026-10-15; replaces the UNAS Pro plan. Hardware details were discussed in other Claude threads but never recorded in the KB; fill them in here.

## Goal

Rebuild Big Boi (TrueNAS SCALE) into a new case with new hardware, so it runs two pools. The existing **SSD pool** holds VMs, containers, apps and configs. A new **HDD pool** holds the Plex media library and any future bulk data. Later, a second box hosted **offsite** could receive ZFS replication from Big Boi.

## Status (2026-10-15)

The direction is decided (Aaron, 2026-10-15). It replaces the UniFi UNAS Pro plan in [Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier](<Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier.md>). Case, board, HBA and drive choices were discussed in other Claude threads but never recorded, so they're **missing here**: add them before planning the build.

## Constraints carried over (from earlier projects; re-check)

- **Rack depth:** 14.6" (370 mm) maximum mountable depth, per the UNAS Pro project. On that basis the Sliger CX3702 (18") was rejected as too deep. The new case has to fit, or the rack changes.
- **Network:** Big Boi is on the USW Pro Max 16 PoE over a 10 GbE SFP+ DAC (10Gtek Intel 82599EN, low-profile). The current board is Mini-ITX with one PCIe slot, which the NIC uses. An HBA for the HDDs needs a board with more slots, or onboard SATA.
- **Power:** the UPS 2U carries Big Boi plus the network core (110 W now, about 1 h runtime). Spinning drives add load and shorten that runtime; re-check against the [Rack Infrastructure — UPS + Power Management](<Rack Infrastructure — UPS + Power Management.md>).
- **Current SSD pool:** RAIDZ1, 5× Samsung 870 EVO 4 TB, 2.36 TB used (2.11 TB of it Plex media), as of 2026-10-15.

## Backup implications (from the [Plan backup strategy for TrueNAS and VMs](<Plan backup strategy for TrueNAS and VMs.md>))

- B2 keeps only the small irreplaceable set (photos, configs, TrueNAS config, Plex DB), which stays near free at any pool size.
- Bulk media never goes to paid cloud: 14 TB on B2 would be about $97/month. Its offsite copy, if any, is ZFS replication to a TrueNAS box that Aaron owns at another site.
- **Groundwork now:** split datasets by protection class (configs / Servarr media / self-ripped rips / personal). The whole media tree can then move to the HDD pool with one local replication, and each dataset gets the right snapshot, cloud and replication policy. The backlog item [Reorganize BIGBOI dataset structure under plex- and personal-](<Reorganize BIGBOI dataset structure under plex- and personal-.md>) is the vehicle for this. It's unblocked, since snapshots were verified 2026-10-15.

## Open questions

- Case, motherboard, CPU/RAM carry-over, HBA, HDD count and size, and HDD pool layout (RAIDZ2 vs mirrors).
- Whether the offsite box happens, where it would live, and how it connects (WireGuard/Tailscale).
- Migration order: build new → move the SSD pool → create the HDD pool → replicate media across.

## Changes

![[Changes.base#For this project]]
