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

## Candidate case: JMCD 12S4 (found 2026-10-25, from the AliExpress listing; not bought)

[AliExpress listing](https://www.aliexpress.us/item/3256807353540875.html) (sold as "12 bay NAS chassis ... Qunhui AIO"; $336.29 for the standard set on 2026-10-25). Specs from the listing's parameter images:

- **Size:** 432 W × 306 D × 262 H mm (482 mm with ears; 310 mm deep with handles). 262 mm is 6U. Fits the 370 mm depth limit with about 60 mm to spare; the 6U height still has to be checked against free rack space.
- **Bays:** 12× hot-swap 3.5" trays (2.5" fits) plus 4 internal 2.5" positions. Backplane is 3× 4-bay boards, 12 Gb SAS/SATA, **one SFF-8643 each, no expander**, so 12 drives need 12 lanes: an 8-port HBA plus 4 SATA ports from the board, or a 16-port HBA.
- **Board:** ATX (smaller should fit), pull-out motherboard tray, 8 full-height expansion slots. Limits: card length 250 mm, **PSU length 170 mm** (the SF750 SFX needs a bracket; an ATX PSU has to be a short one), cooler height 135 mm.
- **Cooling:** 4× 92 mm positions on the drive wall, plus 3× 120 mm and 1× 92 mm on the upper fan rack. Fans are only included in the 1085 and 1185 variants.
- **Variants** (the price list is in RMB, per the images): 950 case, 3 backplanes, 12 trays, ears; 1050 adds 3× SFF-8643 cables; 1085 adds 5× 92 mm and 3× 120 mm fans instead; 1185 adds both.

Open on this case: noise and cooling with 12 HDDs behind 92 mm fans, cable choice (reverse breakout for the SATA-port lanes), and whether the $336 US price is for the bare case or a bundle.

## HBA and board (researched 2026-10-25, from vendor documents)

Aaron wants all 12 front bays on one HBA (2026-10-25). The JMCD 12S4 has three SFF-8643 backplane ports and no expander, so the card needs 12+ lanes, i.e. a 16i with 4× SFF-8643.

- **Pick: Broadcom SAS 9305-16i.** One SAS3216 chip, PCIe 3.0 x8, 16 internal ports on 4× SFF-8643, SATA 3/6 Gb/s, 16.2 W typical, low profile with a full-height bracket included, FreeBSD and Linux listed, minimum airflow 200 LFM. No auxiliary power connector is listed. Source: [Broadcom 9305-16i user guide, pub-005245](https://docs.broadcom.com/doc/pub-005245).
- **Rejected: SAS 9300-16i.** Two SAS3008 chips behind a PCIe switch, 26.9 W nominal, with a 6-pin PCIe auxiliary power connector. More heat and more parts for the same ports. Source: [Broadcom 9300-16i user guide](https://docs.broadcom.com/doc/12353308).
- **Alternative: HBA 9400-16i** (SAS3416, tri-mode, 4× SFF-8643, about 12 W per a reseller listing). Not checked against a Broadcom document yet.
- **TrueNAS:** its hardware guide names Broadcom/LSI SAS HBAs as the most widely used controllers, and the 9400/9500 for newer builds; TrueNAS ships `sas3flash` and `storcli` for 9300/9400/9500 cards. [TrueNAS hardware guide](https://www.truenas.com/docs/scale/gettingstarted/tnhardwareguide/)
- **Board requirements (Aaron, 2026-10-25):** 128 GB RAM support, slots for the HBA, the 10 GbE NIC, and a future GPU. **The Z390 Pro4 below is ruled out** (64 GB max). On LGA1151 (9th gen, 16 CPU lanes) that means x8/x8 for HBA + GPU plus a chipset slot that physically fits the x8 NIC. Intel lists Arc B-series support only for 10th gen and newer on 400-series and newer boards, and says Resizable BAR must be on "for optimal performance" ([Intel Arc system requirements](https://www.intel.com/content/www/us/en/support/articles/000091128.html)), so an Arc Pro B50 is not a supported pairing on LGA1151. Platform choice (keep the i9-9900 or move to a newer platform) is open with Aaron.
- **Platform: keep the i9-9900** (Aaron, 2026-10-25). GPU brand open; Arc is out on this platform, so a future GPU means Nvidia.
- **Board pick: Supermicro X11SCA-F** (C246, ATX 12" × 9.6", EOL, used about $150–210 on eBay 2026-10-25). Per the [Supermicro product page](https://www.supermicro.com/en/products/motherboard/X11SCA-F): 8th/9th gen Core i9 supported, up to 128 GB DDR4-2666 UDIMM (32 GB DIMMs), 8× SATA3, 2× M.2 PCIe x4, AST2500 BMC (IPMI). Per the [manual](https://inquirecontent2.ingrammicro.com/User-Manual/1049448249.pdf) (rev 1.0, predates the 128 GB and Core i9 support): CPU SLOT4 x8 (x16 length), CPU SLOT6 x16 or x8 when SLOT4 is used, PCH SLOT2 x4 (shared with M.2 #1), PCH SLOT7 x1, one PCI slot; BIOS has Internal Graphics enable and Primary Display (IGFX/PEG) options. [ServeTheHome review](https://www.servethehome.com/supermicro-x11sca-f-review-for-intel-xeon-e-2100-and-core-i3-8300/2/): the x1 and x4 slots don't interfere with a double-width card in the x16 slots.
  - Layout: HBA in SLOT4 (x8), GPU later in SLOT6 (x8), NIC in SLOT2 (x4), boot NVMe in M.2 #2 (M.2 #1 is shared with SLOT2), 5 SSDs on board SATA.
  - **NIC swap:** SLOT2 is an x4 slot and the current 82599EN card is x8; open-ended or not is unconfirmed, so plan on a Mellanox ConnectX-3 MCX311A-XCAT (single SFP+, PCIe 3.0 x4, 3.47 W typical, per the [NVIDIA ConnectX-3 manual](https://network.nvidia.com/related-docs/user_manuals/ConnectX-3_Ethernet_Single_and_Dual_SFP+_Port_Adapter_Card_User_Manual.pdf)).
  - **RAM speed:** the existing DDR4-3600 kit works but won't run at 3600. The manual rates the board at 2666 and lists no XMP; BIOS "Maximum Memory Frequency" offers 1333–3200, default auto-detected. Expect 2666 at most (or the kit's JEDEC default if lower). Negligible for this workload.
  - Unverified: minimum BIOS for the i9-9900 and 32 GB DIMMs, and iGPU passthrough to the Plex VM with the BMC video active.
- **Rejected: ASUS PRIME Z390-A.** Its third x16-length slot runs x2 by default, or x4 only with SATA6G_5/6 disabled ([manual](https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/PRIME_Z390-A/F15017_PRIME_Z390-A_UM_V2_WEB.pdf)), which leaves 4 SATA ports for 5 SSDs.
- **Board candidate: ASRock Z390 Pro4** (ATX, Z390, LGA1151, keeps the i9-9900 and 2×32 GB DDR4). Per the [ASRock manual](https://download.asrock.com/Manual/Z390%20Pro4.pdf): PCIE2 is x16 from the CPU, PCIE4 is x16-length but runs x4 when both are used; 3× PCIe x1; 6× SATA3; two M.2 (M2_1 SATA-type disables SATA3_5; M2_2 SATA-type disables SATA3_1, PCIe-type disables SATA3_0); memory max 64 GB, non-ECC. Layout: HBA in PCIE2, the 10 GbE NIC (82599EN, PCIe 2.0 x8 card) in PCIE4 at x4 (about 16 Gb/s usable, enough for one 10 GbE port), NVMe boot in M2_1, the 5 SSDs on SATA3_0–4.
- **Cables:** with the 16i, all three backplanes take SFF-8643↔SFF-8643 cables (the HBA's fourth port stays free). The listing's bundle says "8643 cable ×3" but its wiring diagrams pair two straight cables with one reverse breakout, so confirm with the seller or buy three straight cables.
- **Airflow:** the 9305-16i needs 200 LFM minimum; budget case fans (1085/1185 variant or own) rather than the bare 950.
- **Board caveats:** 64 GB is both the board's maximum and what Big Boi already has, so no RAM growth on this board. i9-9900 support and the minimum BIOS are **not verified**: ASRock's CPU list wouldn't load (bot wall), and a third-party site says the Z390M Pro4 needs BIOS P4.00. A used board on older firmware may not POST with the i9-9900; check the BIOS version with the seller.
- **Gap:** the case has 4 internal 2.5" positions and the SSD pool has 5 drives. Either one SSD takes a front bay on the HBA (11 HDD bays left) or it needs another mount.

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
