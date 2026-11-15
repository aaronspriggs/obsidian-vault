---
date: 2026-10-25
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
---

## What changed

No system changes. Research from vendor manuals for the HBA and the motherboard of the rebuilt Big Boi, 2026-10-25 and 2026-10-26, plus the CPU cooler and BIOS notes of 2026-11-02. Moved here on 2026-11-15 from the [project](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

Aaron wanted all 12 front bays on one HBA, and a board that takes 128 GB, the HBA, the 10 GbE NIC and a future GPU while keeping the i9-9900. Outcome: Broadcom SAS 9305-16i and the Gigabyte Z390 Designare (decisions in the project note).

## How

### Reference: HBA (from vendor documents, 2026-10-25)

- **Broadcom SAS 9305-16i:** one SAS3216 chip, PCIe 3.0 x8, 16 internal ports on 4× SFF-8643, SATA 3/6 Gb/s, 16.2 W typical, low profile with a full-height bracket, FreeBSD and Linux listed, minimum airflow 200 LFM, no auxiliary power connector listed. [Broadcom 9305-16i user guide, pub-005245](https://docs.broadcom.com/doc/pub-005245)
- **Rejected, SAS 9300-16i:** two SAS3008 chips behind a PCIe switch, 26.9 W nominal, 6-pin PCIe auxiliary power. [Broadcom 9300-16i user guide](https://docs.broadcom.com/doc/12353308)
- **Alternative, HBA 9400-16i:** SAS3416, tri-mode, 4× SFF-8643, about 12 W per a reseller listing; not checked against a Broadcom document.
- **TrueNAS:** names Broadcom/LSI SAS HBAs as the most widely used controllers and ships `sas3flash`/`storcli` for 9300/9400/9500 cards. [TrueNAS hardware guide](https://www.truenas.com/docs/scale/gettingstarted/tnhardwareguide/)
- **Counterfeits** are common at the cheap end; buy from a seller with a record of genuine cards.

### Reference: boards for the i9-9900 (from manuals, 2026-10-25)

LGA1151 9th gen has 16 CPU lanes, so the HBA and GPU share x8/x8 and the NIC needs a chipset slot.

- **Gigabyte Z390 DESIGNARE** (used, about $80–360 on eBay, wide spread). [Manual](https://download.gigabyte.com/FileList/Manual/mb_manual_z390-designare_1001_190219_e.pdf): 9th/8th gen Core i9 listed, 128 GB (32 GB DIMMs), XMP, PCIEX16 + PCIEX8 (x8/x8 when both used), PCIEX4 x16-length at x4 (PCH), 2× x1, 6 SATA, HDMI/DP/Thunderbolt. M2P with a PCIe SSD disables SATA3 0; M2M disables SATA3 4/5. Layout: HBA in PCIEX8, GPU in PCIEX16, 82599EN in PCIEX4, NVMe boot in M2P, 5 SSDs on SATA3 1–5 (no spare). No IPMI. Board photos (Aaron, 2026-10-26, rev 1.0): slot order from the CPU is PCIEX16, x1, M2M, PCIEX8, M2P, x1, PCIEX4; all three long slots are x16-length and steel-reinforced, and the back of the board shows pins populated only for the wired lanes (x16 / x8 / x4).
- **Supermicro X11SCA-F** (C246, EOL, used about $150–210 on eBay). [Product page](https://www.supermicro.com/en/products/motherboard/X11SCA-F): 8th/9th gen Core i9, up to 128 GB DDR4-2666 UDIMM, 8 SATA, 2× M.2, AST2500 IPMI. [Manual](https://inquirecontent2.ingrammicro.com/User-Manual/1049448249.pdf) (rev 1.0, predates the 128 GB and Core i9 support): SLOT4 x8 (CPU), SLOT6 x16 or x8 with SLOT4 used (CPU), SLOT2 x4 (PCH, shared with M.2 #1), SLOT7 x1, one PCI; BIOS has Internal Graphics enable and Primary Display options; rated 2666, no XMP listed. [ServeTheHome](https://www.servethehome.com/supermicro-x11sca-f-review-for-intel-xeon-e-2100-and-core-i3-8300/2/): x1/x4 slots clear a double-width card in the x16 slots. SLOT2 may not take the x8 82599EN, hence the [ConnectX-3 MCX311A-XCAT](https://network.nvidia.com/related-docs/user_manuals/ConnectX-3_Ethernet_Single_and_Dual_SFP+_Port_Adapter_Card_User_Manual.pdf) (single SFP+, PCIe 3.0 x4, 3.47 W). Unverified: minimum BIOS for the i9-9900 and 32 GB DIMMs; iGPU passthrough with the BMC video active.
- **Gigabyte C246-WU4** (about $280–360). [Manual](https://download.gigabyte.com/FileList/Manual/server_manual_c246-wu4_sc_0417.pdf): 128 GB, x16 + x8 + two x16-length x4, 10 SATA, no IPMI. i9-9900 support unconfirmed (manual says "9th/8th gen Core"; listings say i7/i5/i3).
- **Ruled out:** ASRock Z390 Pro4 (64 GB max, [manual](https://download.asrock.com/Manual/Z390%20Pro4.pdf)); ASRock Rack E3C246D4U / C246M WS (64 GB, [manual](https://download.asrock.com/Manual/C246M%20WS.pdf)); ASUS PRIME Z390-A (third slot x2, about 8 Gb/s for the PCIe 2.0 NIC, or x4 only by disabling SATA 5/6, [manual](https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/PRIME_Z390-A/F15017_PRIME_Z390-A_UM_V2_WEB.pdf); manual says 64 GB, BIOS 0805 reportedly adds 32 GB DIMMs). Fallback only if much cheaper: x4 mode, 4 SSDs on SATA, SSD #5 on the HBA's spare port via a forward breakout. ASUS WS C246 PRO not checked (manual downloads failed).
- **GPU platform:** Intel lists Arc B-series support only for 10th gen and newer on 400-series and newer boards, with Resizable BAR on "for optimal performance". [Intel Arc system requirements](https://www.intel.com/content/www/us/en/support/articles/000091128.html)

### CPU cooler candidates (2026-11-02)

Noctua NH-U9S, 125 mm under the 135 mm limit, 92 mm fan (a second NF-A9 can be added), mounts for LGA115x, LGA1200, LGA1700, LGA1851, AM4, AM5 ([Noctua specs](https://noctua.at/en/nh-u9s/specification)). NH-D9L (110 mm) if the measured clearance is short. Stronger option: NH-C14S in low-profile mode (140 mm fan under the fins, 115 mm tall; 142 mm with the fan on top, too tall), footprint 163 × 140 mm, so check overhang onto PCIEX16 and RAM in Noctua's compatibility centre for the Designare ([Overclockers](https://www.overclockers.co.uk/noctua-nh-c14s-top-flow-flexible-cpu-cooler-140mm-hs-030-nc.html)). A 92 mm cooler limits sustained boost on 125 W+ chips

### The used Designare's BIOS and PCPartPicker's warnings (2026-11-02)

Used Designare's BIOS: i9-9900 needs **F6 or newer** per [Pangoly's compatibility table](https://pangoly.com/en/compatibility/gigabyte-z390-designare/cpu) (third-party; Gigabyte's CPU list wouldn't load). The manual lists DualBIOS but no BIOS update without a CPU, so a board on older firmware needs a supported older CPU to flash it. Seller's listing says the BIOS was updated (Aaron, 2026-11-02), version not stated; F6 dates from 2019, so any recent update covers it. PCPartPicker (2026-11-02) also warns that some Z390 boards need a BIOS update for 32 GB DIMMs, so flash the latest BIOS, not just F6. Its "RM1000x has no −12 V" warning is generic: −12 V only fed legacy RS-232/PCI and ATX 3.x made it optional.

## How to verify / roll back

Nothing to roll back. On arrival: the HBA's label part number and `storcli` reporting SAS9305-16i; the board's BIOS version.
