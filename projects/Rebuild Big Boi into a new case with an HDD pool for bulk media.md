---
type: project
status: active
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
next_step: 2026-10-26 Aaron buys a used Z390 Designare (BIOS F6 or newer); then pick the HDDs, order 3× 0.5 m SFF-8643 cables, check 7U of free rack space.
notion_id: 3fa7ae76-22ba-811b-9baa-c2e05b8e9c2e
---

Decided by Aaron 2026-10-15; replaces the UNAS Pro plan. Case ordered 2026-10-26.

## Goal

Rebuild Big Boi (TrueNAS SCALE) into a new case with new hardware, so it runs two pools. The existing **SSD pool** holds VMs, containers, apps and configs. A new **HDD pool** holds the Plex media library and any future bulk data. Later, a second box hosted **offsite** could receive ZFS replication from Big Boi.

## Status (2026-10-26)

**Case ordered** (JMCD 12S4, base 950 bundle with no cables or fans, via Alibaba.com with Trade Assurance, 2026-10-26). Price, order number and delivery estimate not yet recorded. HBA chosen (9305-16i); board chosen (Gigabyte Z390 Designare, Aaron sourcing a used one); PSU stays the SF750 with one extra Molex cable; HDDs not chosen.

![Proposed layout](<../attachments/Big Boi rebuild - proposed layout.svg>)

## Plan: parts

| Part | Choice | State |
|---|---|---|
| Case | JMCD 12S4, 12-bay, base bundle (no cables, no fans) | **Ordered 2026-10-26** |
| HBA | Broadcom SAS 9305-16i | Chosen, not bought |
| Backplane cables | 3× SFF-8643 ↔ SFF-8643, 0.5 m | To buy (base bundle has none) |
| Board | Gigabyte Z390 DESIGNARE, used, BIOS F6 or newer | **Chosen 2026-10-26**; Aaron sourcing |
| CPU | Intel i9-9900 | Keep |
| RAM | 2× 32 GB existing + 2× 32 GB to buy = 128 GB | To buy |
| NIC | 10Gtek Intel 82599EN in PCIEX4 | Keep |
| Boot | NVMe in M2P (disables SATA3 0) | To buy |
| PSU | Corsair SF750 (keep) + 1× Corsair Type 4 Molex cable | Cable to buy |
| Case fans | Aaron's own, right sizes (120 × 25 / 92 × 25), 4-pin PWM | Have (confirmed by Aaron 2026-10-26) |
| HDDs | Count, size and pool layout | Open |
| GPU | Future, Nvidia | Later |

## Ordered: JMCD 12S4 case (2026-10-26)

Ordered through Alibaba.com (checkout on biz.alibaba.com, Trade Assurance). Same model as this [AliExpress listing](https://www.aliexpress.us/item/3256807353540875.html) (sold as "12 bay NAS chassis ... Qunhui AIO", $336.29 for the standard set on 2026-10-25). Specs from the listing's parameter images and the seller's English screenshots:

- **Size:** 432 W × 306 D × 262 H mm (482 mm wide with ears; 310 mm deep with handles). 262 mm = 6U. Fits the 370 mm rack depth limit with about 60 mm to spare; 6U still has to be checked against free rack space.
- **Material:** 1.0 mm galvanized steel, black.
- **Bays:** 12× tool-free hot-swap 3.5" trays (2.5" fits), each with a status LED; plus 4 internal 2.5" positions.
- **Backplanes:** 3× 4-bay boards, 12 Gb/s SAS/SATA, no expander. Each board has one SFF-8643 (4 lanes), one 4-pin Molex power input, fan headers, a temperature probe and DIP switch SW1 for fan control: ON/ON (default) auto = 50% under 30 °C, ramping 30–50 °C, 100% above 50 °C; ON/OFF 50%, OFF/ON 75%, OFF/OFF 100%.
- **Backplane power (seller):** 3 separate Molex cables, or 2 separate cables (one feeding two backplanes); a single cable for all three is marked incorrect.
- **Data (seller):** suggests an LSI HBA; SFF-8643 ↔ SFF-8643 (or ↔ SFF-8087) to the HBA; reverse SFF-8643-to-4-SATA breakout only for motherboard or SATA-card ports.
- **Board:** ATX, pull-out motherboard tray, 8 full-height expansion slots. Card length ≤ 250 mm, PSU length ≤ 170 mm, CPU cooler height ≤ 135 mm.
- **Cooling:** drive wall 4× 92 mm (9225); upper fan rack 3× 120 mm (12025) + 1× 92 mm, quick-release.
- **Bundles** (price list in RMB per the images): 950 = case, 3 backplanes, 12 trays, ears; 1050 adds 3× "8643" cables; 1085 adds 5× 92 mm PWM (dual ball bearing) + 3× 120 mm PWM fans instead; 1185 adds both. PSU, drives and board not included.

## Build log from another owner (bytepursuits.com)

[12-bay homelab NAS: JMCD 12S4 from Taobao](https://bytepursuits.com/12-bay-homelab-nas-jmcd-12s4-from-taobao-upgrading-my-truenas-scale-server-optionally-rack-mountable), read 2026-10-26 (via a summarizer, so spot-check before relying on a detail):

- **Measured** 432 W × 295 D × 272 H mm (6.11U), 12 kg packed. Height differs from the listing's 262 mm.
- **Cables:** SFF-8643 ↔ SFF-8643; 0.8 m was "somewhat long", 0.5 m recommended; a commenter says 0.5 m works with the HBA in slot 4.
- **Power:** author warns against daisy-chaining the backplane Molex; one 12 V run per backplane socket if possible. Matches the seller's guidance.
- **PSUs used:** EVGA SuperNOVA 450 GM (SFX with ATX adapter; one daisy-chained 4-pin cable with connectors at 300/410/520/630 mm powering the backplanes), later an ASRock Steel Legend SL-750G (June 2025). Author: "advised to not use daisy chained 4 pin cables – or at least check your PSU rated power"; use separate 12 V runs per backplane if available. **The PSU mounts right above the opening to the backplane power connectors, so the cable doesn't need to be long** (the SF750's 330 mm Molex reach is likely fine).
- **PSU fit:** the SFX unit "fit right in". A commenter with an SF750 had to temporarily remove a front panel and the internal 2.5" rack to install it.
- **Fans:** stock layout 3× 120 mm intake + 4× 92 mm exhaust; backplane jumper curves 37 / 42 / 59 / 100%. Stock JMCD fans have non-standard ridges that needed trimming for one board. With IPMI boards, low fan RPM (≈400) tripped BMC low-RPM thresholds until lowered with ipmitool (relevant to the X11SCA-F).
- **Limits:** mini-ITX, mATX and ATX boards, not EATX/CEB; board depth about 275 mm; cooler 135 mm; card 250 mm (a 267 mm card didn't fit).
- **Other:** JMCD's USB 3 header is flimsy and needed a right-angle adapter; HBA can block fan headers on small boards; replacement backplanes available from the seller; TrueNAS imported existing pools without issue; drives fine after a year.

## Decisions

- **2026-10-15 (Aaron):** two pools inside a rebuilt Big Boi; replaces the UNAS Pro plan.
- **2026-10-25 (Aaron):** all 12 front bays on one HBA → a 16-port card.
- **2026-10-25:** HBA = Broadcom SAS 9305-16i over the 9300-16i (one chip, 16.2 W, no aux power vs two chips, 26.9 W, 6-pin aux).
- **2026-10-25 (Aaron):** board must support 128 GB, the HBA, the NIC and a future GPU; keep the i9-9900. A future GPU is Nvidia (Intel supports Arc only on 10th gen and newer).
- **2026-10-25:** SSDs stay on board SATA, HDDs on the HBA.
- **2026-10-25:** keep the SF750, power the backplanes with 2 Molex cables (seller's method 2), not one.
- **2026-10-26 (Aaron):** JMCD 12S4 ordered, base bundle; fans from Aaron's stock.
- **2026-10-26 (Aaron):** board = Gigabyte Z390 Designare over the Supermicro X11SCA-F: i9-9900 and 128 GB documented in its manual, keeps the 82599EN, XMP for the 3600 kit, same consumer-board iGPU passthrough path as today. Trade-off accepted: no IPMI, exactly 5 usable SATA ports.

## Open questions

- Case order details: price paid, order number, ETA.
- Case height: the listing says 262 mm (6U), the build log below measured 272 mm (6.11U), which takes 7U in a rack. Measure on arrival.
- Used Designare's BIOS: i9-9900 needs **F6 or newer** per [Pangoly's compatibility table](https://pangoly.com/en/compatibility/gigabyte-z390-designare/cpu) (third-party; Gigabyte's CPU list wouldn't load). The manual lists DualBIOS but no BIOS update without a CPU, so a board on older firmware needs a supported older CPU to flash it. Ask the seller.
- HDD count, size and pool layout (RAIDZ2 vs mirrors); spin-up current from the chosen drive's datasheet.
- Where SSD #5 mounts (4 internal 2.5" positions for 5 SSDs) and powers (crimped Molex-to-SATA off the second Molex cable is the fallback).
- 6U of free rack space; UPS runtime with spinning drives.
- Whether the offsite box happens, where it would live, and how it connects (WireGuard/Tailscale).
- Migration order: build new → move the SSD pool → create the HDD pool → replicate media across.

## Reference: HBA (from vendor documents, 2026-10-25)

- **Broadcom SAS 9305-16i:** one SAS3216 chip, PCIe 3.0 x8, 16 internal ports on 4× SFF-8643, SATA 3/6 Gb/s, 16.2 W typical, low profile with a full-height bracket, FreeBSD and Linux listed, minimum airflow 200 LFM, no auxiliary power connector listed. [Broadcom 9305-16i user guide, pub-005245](https://docs.broadcom.com/doc/pub-005245)
- **Rejected, SAS 9300-16i:** two SAS3008 chips behind a PCIe switch, 26.9 W nominal, 6-pin PCIe auxiliary power. [Broadcom 9300-16i user guide](https://docs.broadcom.com/doc/12353308)
- **Alternative, HBA 9400-16i:** SAS3416, tri-mode, 4× SFF-8643, about 12 W per a reseller listing; not checked against a Broadcom document.
- **TrueNAS:** names Broadcom/LSI SAS HBAs as the most widely used controllers and ships `sas3flash`/`storcli` for 9300/9400/9500 cards. [TrueNAS hardware guide](https://www.truenas.com/docs/scale/gettingstarted/tnhardwareguide/)
- **Counterfeits** are common at the cheap end; buy from a seller with a record of genuine cards.

## Reference: boards for the i9-9900 (from manuals, 2026-10-25)

LGA1151 9th gen has 16 CPU lanes, so the HBA and GPU share x8/x8 and the NIC needs a chipset slot.

- **Gigabyte Z390 DESIGNARE** (used, about $80–360 on eBay, wide spread). [Manual](https://download.gigabyte.com/FileList/Manual/mb_manual_z390-designare_1001_190219_e.pdf): 9th/8th gen Core i9 listed, 128 GB (32 GB DIMMs), XMP, PCIEX16 + PCIEX8 (x8/x8 when both used), PCIEX4 x16-length at x4 (PCH), 2× x1, 6 SATA, HDMI/DP/Thunderbolt. M2P with a PCIe SSD disables SATA3 0; M2M disables SATA3 4/5. Layout: HBA in PCIEX8, GPU in PCIEX16, 82599EN in PCIEX4, NVMe boot in M2P, 5 SSDs on SATA3 1–5 (no spare). No IPMI. Board photos (Aaron, 2026-10-26, rev 1.0): slot order from the CPU is PCIEX16, x1, M2M, PCIEX8, M2P, x1, PCIEX4; all three long slots are x16-length and steel-reinforced, and the back of the board shows pins populated only for the wired lanes (x16 / x8 / x4).
- **Supermicro X11SCA-F** (C246, EOL, used about $150–210 on eBay). [Product page](https://www.supermicro.com/en/products/motherboard/X11SCA-F): 8th/9th gen Core i9, up to 128 GB DDR4-2666 UDIMM, 8 SATA, 2× M.2, AST2500 IPMI. [Manual](https://inquirecontent2.ingrammicro.com/User-Manual/1049448249.pdf) (rev 1.0, predates the 128 GB and Core i9 support): SLOT4 x8 (CPU), SLOT6 x16 or x8 with SLOT4 used (CPU), SLOT2 x4 (PCH, shared with M.2 #1), SLOT7 x1, one PCI; BIOS has Internal Graphics enable and Primary Display options; rated 2666, no XMP listed. [ServeTheHome](https://www.servethehome.com/supermicro-x11sca-f-review-for-intel-xeon-e-2100-and-core-i3-8300/2/): x1/x4 slots clear a double-width card in the x16 slots. SLOT2 may not take the x8 82599EN, hence the [ConnectX-3 MCX311A-XCAT](https://network.nvidia.com/related-docs/user_manuals/ConnectX-3_Ethernet_Single_and_Dual_SFP+_Port_Adapter_Card_User_Manual.pdf) (single SFP+, PCIe 3.0 x4, 3.47 W). Unverified: minimum BIOS for the i9-9900 and 32 GB DIMMs; iGPU passthrough with the BMC video active.
- **Gigabyte C246-WU4** (about $280–360). [Manual](https://download.gigabyte.com/FileList/Manual/server_manual_c246-wu4_sc_0417.pdf): 128 GB, x16 + x8 + two x16-length x4, 10 SATA, no IPMI. i9-9900 support unconfirmed (manual says "9th/8th gen Core"; listings say i7/i5/i3).
- **Ruled out:** ASRock Z390 Pro4 (64 GB max, [manual](https://download.asrock.com/Manual/Z390%20Pro4.pdf)); ASRock Rack E3C246D4U / C246M WS (64 GB, [manual](https://download.asrock.com/Manual/C246M%20WS.pdf)); ASUS PRIME Z390-A (third slot x2, about 8 Gb/s for the PCIe 2.0 NIC, or x4 only by disabling SATA 5/6, [manual](https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/PRIME_Z390-A/F15017_PRIME_Z390-A_UM_V2_WEB.pdf); manual says 64 GB, BIOS 0805 reportedly adds 32 GB DIMMs). Fallback only if much cheaper: x4 mode, 4 SSDs on SATA, SSD #5 on the HBA's spare port via a forward breakout. ASUS WS C246 PRO not checked (manual downloads failed).
- **GPU platform:** Intel lists Arc B-series support only for 10th gen and newer on 400-series and newer boards, with Resizable BAR on "for optimal performance". [Intel Arc system requirements](https://www.intel.com/content/www/us/en/support/articles/000091128.html)

## Reference: power (2026-10-25)

- **SF750 stock kit** per [Corsair](https://www.corsair.com/us/en/p/psu/cp-9020186-na/sf-series-sf750-750-watt-80-plus-platinum-certified-high-performance-sfx-psu-cp-9020186-na): 24-pin (300 mm), 2× EPS 4+4 (400 mm), 2× PCIe with two 6+2 each (500 mm), 2× SATA with 4 connectors each (445 mm), 1× Molex with 3 connectors (330 mm); SFX-to-ATX bracket included; 125 mm long. 3 "Peripheral & SATA" sockets (System note).
- **Layout (seller's method 2):** socket 1 stock Molex → backplanes A+B; socket 2 second Corsair Type 4 Molex → backplane C; socket 3 SATA → 4 SSDs. Board: 24-pin, 8 + 4-pin CPU (Designare). Future GPU: the PCIe cables. The 330 mm Molex cable's reach to the lowest backplane is unchecked.
- **Why not one cable:** a daisy-chained Molex cable has one +12 V wire. Each backplane connector carries only its own 4 drives (about 8 A at spin-up, using IronWolf Pro's 2.0 A at 12 V as quoted by retailers), within the Molex 8981 contact rating (TTI quotes 15 A max). The shared first wire segment and PSU-side plug would carry all 12 (about 24 A); no rated limit found for those.
- **Replacement PSU search (2026-10-26, max length 160 mm per Aaron).** Socket counts from [HWBusters](https://hwbusters.com) rear-panel photos and cable tables:
  - **FSP Vita GM 850 (pick if replacing):** 140 mm, Cybenetics Platinum, noise A (20–25 dB[A]), 10-year warranty, MSRP $139. 3 peripheral sockets, but the stock cables are 1× SATA (4) and 2× mixed SATA + Molex (500 + 150 mm to 2 SATA, then +155 + 100 mm to 2 Molex). Out of the box: mixed cable 1 → backplanes A+B + 2 SSDs, mixed cable 2 → backplane C + 2 SSDs, SATA cable → SSD #5. Seller's method 2 with every SSD powered natively and long reach. [Review](https://hwbusters.com/psus/fsp-vita-gm-850w-atx-v3-1-psu-review/2/)
  - **Montech Titan PLA 750:** 160 mm, Seasonic OEM, Cybenetics Platinum, A+, MSRP $159. **4** peripheral sockets, but only 1 Molex cable (4 connectors) in the box and no Montech spare cable found, so it needs a cable that isn't available. [Review](https://hwbusters.com/psus/montech-titan-pla-750w-atx-v3-1-psu-review/2/)
  - **Corsair RM750x (2024):** 160 mm, 3 "SATA / PATA" sockets (rear photo), stock 2× SATA + 1× Molex. Same as the SF750. [Review](https://hwbusters.com/psus/corsair-rm750x-atx-v3-1-psu-review/)
  - **be quiet! Pure Power 13 M 850:** 160 mm, FSP OEM, Platinum, A++; only 6 SATA + 2 Molex in the box. [Review](https://hwbusters.com/Peripherals/be-quiet-pure-power-13-m-850w-atx-v3-1-psu-review/)
- **Other PSUs checked:** Seasonic Focus GX-750 ATX 3 (140 mm, 3 peripheral sockets per [HWBusters photos](https://hwbusters.com/psus/seasonic-focus-gx-750-v4-atx-v3-1-psu-review/2/)); Corsair RM750x 2024 (160 mm, socket count not found, [Corsair](https://www.corsair.com/us/en/p/psu/cp-9020285-na/rm750x-fully-modular-low-noise-atx-power-supply-cp-9020285-na)). Neither beats the SF750 here.

## Reference: constraints carried over

- **Rack depth:** 14.6" (370 mm) maximum mountable depth, per the UNAS Pro project; the Sliger CX3702 (18") was rejected on that basis.
- **Network:** Big Boi is on the USW Pro Max 16 PoE over a 10 GbE SFP+ DAC.
- **UPS:** the UPS 2U carries Big Boi plus the network core (110 W now, about 1 h runtime); spinning drives add load. See [Rack Infrastructure — UPS + Power Management](<Rack Infrastructure — UPS + Power Management.md>).
- **Current SSD pool:** RAIDZ1, 5× Samsung 870 EVO 4 TB, 2.36 TB used (2.11 TB Plex media), as of 2026-10-15.
- **Backup** (from [Plan backup strategy for TrueNAS and VMs](<Plan backup strategy for TrueNAS and VMs.md>)): B2 keeps only the small irreplaceable set; bulk media never goes to paid cloud (14 TB on B2 ≈ $97/month), its offsite copy if any is ZFS replication to a box Aaron owns. Groundwork: split datasets by protection class via [Reorganize BIGBOI dataset structure under plex- and personal-](<Reorganize BIGBOI dataset structure under plex- and personal-.md>).
- **Superseded plan:** [Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier](<Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier.md>).

## Changes

![[Changes.base#For this project]]
