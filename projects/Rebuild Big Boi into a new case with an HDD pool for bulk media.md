---
type: project
status: active
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
next_step: 2026-11-08 Order 3× 0.5 m SFF-8643 cables and 1× Corsair Type 4 Molex cable (third backplane on the RM1000x); then pick the HDDs; rack plan is the 12S4 as 6U with 1U open or blanked above it (Aaron 2026-11-02).
notion_id: 3fa7ae76-22ba-811b-9baa-c2e05b8e9c2e
---

## Goal

Rebuild Big Boi (TrueNAS SCALE) into a new case with new hardware, so it runs two pools. The existing **SSD pool** holds VMs, containers, apps and configs. A new **HDD pool** holds the Plex media library and any future bulk data.

## Status (2026-11-15)

Ordered or bought: the case (2026-10-26), HBA and board (2026-10-28), second RAM kit (2026-11-07), PSU (2026-11-08) and GPU (2026-11-09). What has arrived isn't recorded. Still to buy: backplane cables, one Molex cable, a CPU cooler and the HDDs. Slimmed 2026-11-15: research is in the change notes linked below, the rack move is its own project, the earlier text is in git history.

![Proposed layout](<../attachments/Big Boi rebuild - proposed layout.svg>)

## Plan

### Parts

| Part | Choice | State |
|---|---|---|
| Case | JMCD 12S4, 12-bay, base bundle (no cables, no fans). Limits: ATX board, card ≤ 250 mm with 25 mm fans fitted, PSU ≤ 170 mm, cooler ≤ 135 mm | **Ordered 2026-10-26** |
| HBA | Broadcom SAS 9305-16i, used, full-height bracket | **Ordered 2026-10-28**; verify on arrival |
| Backplane cables | 3× SFF-8643 ↔ SFF-8643, 0.5 m | To buy |
| Board | Gigabyte Z390 DESIGNARE, used | **Ordered by 2026-10-28** |
| CPU | Intel i9-9900 | Keep |
| CPU cooler | Candidate: Noctua NH-U9S | Open (see Open questions) |
| RAM | 4× 32 GB = 128 GB: the existing CMK64GX4M2D3600C18 kit plus a second identical one | Bought 2026-11-07 |
| NIC | 10Gtek Intel 82599EN in PCIEX4 | Keep |
| Boot | Patriot P300 128 GB NVMe (today's boot drive, moves over with the boot pool) in M2P | Have (Aaron 2026-11-08) |
| PSU | Corsair RM1000x ATX 3.1 (2024, non-Shift); add 1× Corsair Type 4 Molex cable (CP-8920199 or CP-8920196) to its stock 2 | **Bought** (Aaron, 2026-11-08); Molex cable to buy |
| Case fans | Aaron's own, 120 × 25 and 92 × 25, 4-pin PWM | Have (Aaron 2026-10-26) |
| HDDs | RAIDZ2, start with 4, one size for every drive | Size open |
| GPU | ASRock Challenger A380 ITX 6GB OC (Arc A380, 190 mm long, 2-slot, one 8-pin from the RM1000x), for AV1 encode on the host for containers ([[Automated AV1 re-encode pipeline for UHD Blu-ray rips on Big Boi]]) | **Arrived** (Aaron, 2026-11-15: "early this week"; ordered 2026-11-09, Newegg, about $200). Return window date not recorded |

Slots: GPU in PCIEX16 and HBA in PCIEX8 (x8/x8), NIC in PCIEX4, NVMe boot in M2P (disables SATA3 0), the 5 SSDs on SATA3 1–5, none spare. Power: one Molex cable per backplane and 2 SATA cables for the SSDs, filling the RM1000x's 5 peripheral sockets (counted by Aaron, 2026-11-08).

### On arrival and first boot

1. Case: measure its height without feet (for the rack plan) and the bracket-to-fan card clearance.
2. HBA: check the label part number; once installed, `storcli` reports SAS9305-16i.
3. Board: flash the latest BIOS (F11a) first. The i9-9900 needs F6 or newer, Resizable BAR for the A380 needs F9, and some Z390 boards need an update for 32 GB DIMMs. The seller says the BIOS was updated (Aaron, 2026-11-02), version unknown; a board older than F6 can only be flashed with an older CPU fitted.
4. Before turning CSM off for the A380, check Big Boi boots UEFI (`[ -d /sys/firmware/efi ]`).
5. RAM: XMP 3600 first, then voltage, then 3466 or 3200; a long memtest pass either way.

### Migration

Build new, move the SSD pool, create the HDD pool, replicate the media across. During the media move (Aaron, 2026-11-08): put the self-ripped discs in their own `rips` dataset on the HDD pool, add it as a Plex library path and give it a B2 Cloud Sync task (backup project phase 2; 11 folders, 616 GB on 2026-11-08, listed in [Plan backup strategy](<Plan backup strategy for TrueNAS and VMs.md>), Aaron to confirm). Also move `Movies/DJI_0001.MP4` (personal drone clip, on no backup) to Media Library. Afterwards re-map the HA VM's USB passthrough: the Zigbee dongle and the Z-Wave stick for [the security system](<Plan a home security system (Alarmo, door-window sensors, siren).md>) are bound to the USB bus and port path.

### Sub-projects

- [Move the homelab into the 30U floor rack](<Move the homelab into the 30U floor rack.md>): layout v17, power, weight; the patch panel and gear-sale projects hang off it.
- [[Automated AV1 re-encode pipeline for UHD Blu-ray rips on Big Boi]] (backlog).

## Decisions

- **2026-10-15 (Aaron): two pools inside a rebuilt Big Boi,** replacing the [UNAS Pro plan](<Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier.md>) ([change](<../changes/2026-10-15 Recorded storage direction - Big Boi rebuild with HDD pool replaces UNAS Pro.md>)).
- **2026-10-26 (Aaron): JMCD 12S4 case, base bundle, fans from his own stock.** Ordered through Alibaba.com with Trade Assurance. Specs, seller guidance and another owner's build log: [change](<../changes/2026-10-26 Recorded the JMCD 12S4 case specs and an owner's build log.md>).
- **2026-10-25 (Aaron): all 12 front bays on one HBA, so a 16-port card; SSDs stay on board SATA.** Broadcom SAS 9305-16i over the 9300-16i: one chip, 16.2 W and no auxiliary power, against two chips, 26.9 W and a 6-pin plug. Ordered used on 2026-10-28 (eBay seller Electronic Sister, 6,536 feedback at 99.9%, $64.99). [Research](<../changes/2026-10-25 Researched the HBA and boards for the Big Boi rebuild.md>).
- **2026-10-26 (Aaron): board is the Gigabyte Z390 Designare, over the Supermicro X11SCA-F.** His requirements (2026-10-25): 128 GB, the HBA, the NIC and a future GPU, keeping the i9-9900. Its manual documents the i9-9900 and 128 GB, and it keeps the 82599EN, XMP for the 3600 kit and today's iGPU passthrough path. Accepted: no IPMI and exactly 5 usable SATA ports. Also ruled out: ASRock Z390 Pro4 and the ASRock Rack C246 boards (64 GB), ASUS PRIME Z390-A (third slot x2), Gigabyte C246-WU4 (i9-9900 support unconfirmed). Used board ordered 2026-10-28. Same research note as the HBA.
- **2026-10-29 (Aaron): HDD pool is one RAIDZ2 vdev, started 4-wide and grown 1–2 drives at a time by RAIDZ expansion up to 12-wide,** every drive the same size. At full width, rewrite the data once (`zfs rewrite` on 25.10) so old blocks move to the 10+2 ratio; expire the media dataset's snapshots first. Mirrors rejected (50% forever), RAIDZ1 rejected (expansion can't change parity later). [Math and sources](<../changes/2026-10-29 Worked out the HDD pool layout for the Big Boi rebuild (RAIDZ2 grown by expansion).md>).
- **2026-11-07 (Aaron): 128 GB.** A second identical kit was bought, replacing his 2026-10-28 decision to buy no RAM and move the existing 64 GB (that week ARC averaged about 17 GiB and available memory never fell below 5 GiB; more RAM mainly helps ARC hold metadata for the HDD pool). 4× 32 GB at 3600 isn't guaranteed on the i9-9900 (rated DDR4-2666), hence the fallback speeds above.
- **2026-11-08 (Aaron): stay with the Designare, the i9-9900 and 128 GB; the LGA1700 or AM4 platform swap is dropped.** He explored it on 2026-11-07 on these terms: keep the DDR4 kits, Plex stays a VM (the earlier TrueNAS app had problems), TrueNAS apps can still use a GPU, CPU headroom but nothing near 200 W. Considered: an i7-14700 non-K with power limits on a DDR4 Z790 or B760 board, and an AM4 Ryzen 9. Why not: over 30 days CPU averaged 5% and peaked at 20%, so RAM is the constraint; a swap doesn't improve the odds of 3600 on four sticks, needs an Arc card for the Plex VM (iGPU passthrough is proven on the UHD 630, unreliable on LGA1700), and is itself end-of-line. Revisit on a DDR5 platform if ECC, Arc B-series or more PCIe becomes a real need. Possible later: the gaming PC's Ryzen 9 5900X when that PC is upgraded (needs an AM4 board that passes the slot check and an Arc card for the Plex VM). [Working-out](<../changes/2026-11-08 Compared a platform swap (LGA1700, AM4) with keeping the Designare and i9-9900.md>).
- **2026-11-08 (Aaron, decided earlier in conversation): PSU is the Corsair RM1000x (2024, non-Shift), not the SF750,** because the SF750 has 3 peripheral sockets for 3 backplanes plus 5 SSDs. This replaces the 2026-10-25 plan to keep the SF750 and feed the backplanes from 2 Molex cables. One cable for all three was never an option: the seller marks it incorrect, and 12 drives starting together would pull about 23 A through one 12 V wire. Rejected on the way: the RM1000x Shift (Aaron, 2026-11-01: a standard ATX PSU only just fits the 12S4 top to bottom, so there's no room for side connectors), and five smaller units with 3 or 4 peripheral sockets (named in the research note). The SF750 stays with the old box. [Research](<../changes/2026-11-01 Researched backplane power and PSUs for the Big Boi rebuild.md>).
- **2026-11-09 (Aaron): GPU is an Intel Arc A380, for AV1 encode.** On 2026-10-25 a future GPU was to be Nvidia, because Intel supports Arc only on 10th gen and newer. On 2026-10-28 he set the rule for the AV1 card: Nvidia only if one with AV1 encode costs about $200, otherwise an A380; the cheapest Nvidia encoders cost more. For an LLM card he said on 2026-10-28 that about $700 was more than he wanted to spend (an RTX 3060 12 GB at about $290, or deferring, were the options), and on 2026-11-07 it went out of scope. On 2026-11-09 the last objection went: the 10th-gen floor is Intel's Resizable BAR validation, and the Designare has ReBAR from BIOS F9 (Gigabyte's support page). It was ordered that day, ahead of the planned check that the 4th-gen Apple TV (2026-11-13) direct-plays AV1 in Plex. [Research, including the LLM cards](<../changes/2026-10-28 Researched GPUs for the Big Boi rebuild (AV1 encode and local LLMs).md>).
- **2026-11-08 (Aaron): the old box (ASRock Z390M-ITX/ac, i5-9400, 8 GB, 256 GB SATA SSD, SF750) won't host Home Assistant or the ClaudeCode VM.** HA downtime isn't a big concern, the box is overkill for it, and Big Boi's 128 GB is meant to carry the VMs. It stays intact as known-good spare parts until the rebuild is stable, then gets sold unless another use turns up. Its 2U case stays in the rack as a second server (2026-11-12, rack project).
- **2026-11-08 (Aaron): no offsite box for now.** The old box's MyElectronics 2U Mini-ITX case has no 3.5" bays. Only `plex_content` (2,111 GB; `vmstore` is 309 GB, everything else under 2 GB, TrueNAS API 2026-11-08) would justify one, what's irreplaceable is already in B2 ([B2 runbook](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>)), and re-ripping is an acceptable worst case.

## Open questions

- Case order details: price paid, order number, ETA.
- CPU cooler. Candidate (2026-11-02): Noctua NH-U9S, 125 mm under the 135 mm limit ([specs](https://noctua.at/en/nh-u9s/specification)); NH-D9L (110 mm) if the measured clearance is short. Stronger: NH-C14S in low-profile mode (115 mm tall, 163 × 140 mm footprint), after checking overhang onto PCIEX16 and the RAM in Noctua's compatibility centre.
- HDD size (one size for the life of the vdev); spin-up current from the chosen drive's datasheet.
- Where SSD #5 mounts (4 internal 2.5" positions for 5 SSDs).
- UPS runtime with spinning drives ([UPS project](<Rack Infrastructure — UPS + Power Management.md>); 110 W and about 1 h today).

## Constraints carried over

- **SSD pool today:** see [Big Boi storage](<../systems/Big Boi storage (pool, datasets, shares, backups).md>); about 2.1 TB of it is Plex media, which moves to the HDD pool.
- **Backup** ([Plan backup strategy](<Plan backup strategy for TrueNAS and VMs.md>)): B2 keeps only the small irreplaceable set; bulk media never goes to paid cloud. Groundwork: split datasets by protection class via [Reorganize BIGBOI dataset structure under plex- and personal-](<Reorganize BIGBOI dataset structure under plex- and personal-.md>).

## Changes

![[Changes.base#For this project]]
