---
date: 2026-10-26
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
---

## What changed

No system changes. Specs of the JMCD 12S4 case ordered on 2026-10-26, another owner's build log, and the checks on the case's height (2026-11-02 and 2026-11-12). Moved here on 2026-11-15 from the [project](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

The base bundle comes with no documentation Claude can read later, and the listing's and the owner's measurements disagree on height (262 mm against 272 mm), which decides whether the case takes 6U or 7U.

## How

### Ordered: JMCD 12S4 case (2026-10-26)

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

### Build log from another owner (bytepursuits.com)

[12-bay homelab NAS: JMCD 12S4 from Taobao](https://bytepursuits.com/12-bay-homelab-nas-jmcd-12s4-from-taobao-upgrading-my-truenas-scale-server-optionally-rack-mountable), read 2026-10-26 (via a summarizer, so spot-check before relying on a detail):

- **Measured** 432 W × 295 D × 272 H mm (6.11U), 12 kg packed. Height differs from the listing's 262 mm.
- **Cables:** SFF-8643 ↔ SFF-8643; 0.8 m was "somewhat long", 0.5 m recommended; a commenter says 0.5 m works with the HBA in slot 4.
- **Power:** author warns against daisy-chaining the backplane Molex; one 12 V run per backplane socket if possible. Matches the seller's guidance.
- **PSUs used:** EVGA SuperNOVA 450 GM (SFX with ATX adapter; one daisy-chained 4-pin cable with connectors at 300/410/520/630 mm powering the backplanes), later an ASRock Steel Legend SL-750G (June 2025). Author: "advised to not use daisy chained 4 pin cables – or at least check your PSU rated power"; use separate 12 V runs per backplane if available. **The PSU mounts right above the opening to the backplane power connectors, so the cable doesn't need to be long** (the SF750's 330 mm Molex reach is likely fine).
- **PSU fit:** the SFX unit "fit right in". A commenter with an SF750 had to temporarily remove a front panel and the internal 2.5" rack to install it.
- **Fans:** stock layout 3× 120 mm intake + 4× 92 mm exhaust; backplane jumper curves 37 / 42 / 59 / 100%. Stock JMCD fans have non-standard ridges that needed trimming for one board. With IPMI boards, low fan RPM (≈400) tripped BMC low-RPM thresholds until lowered with ipmitool (relevant to the X11SCA-F).
- **Limits:** mini-ITX, mATX and ATX boards, not EATX/CEB; cooler 135 mm; card 250 mm per the listing. Corrected 2026-11-09 from a verbatim read of the page: no one reports a card that didn't fit (267 mm appears only as an unanswered question and as CEB board depth). A commenter relays the manufacturer: "without the fans, the max depth is 275mm (250mm + 25mm for fan)", so 250 mm is with the 25 mm-thick 120 mm fans fitted; a 15 mm slim fan would give about 260 mm. Secondhand and given for board depth, so measure bracket-to-fan when the case arrives.
- **Other:** JMCD's USB 3 header is flimsy and needed a right-angle adapter; HBA can block fan headers on small boards; replacement backplanes available from the seller; TrueNAS imported existing pools without issue; drives fine after a year.

### Case height: 262 mm or 272 mm (checked 2026-11-02 and 2026-11-12)

the listing says 262 mm (6U), the build log above measured 272 mm (6.11U), which takes 7U in a rack. Spot-checked 2026-11-02: the post gives "height: 272mm (or 6.11U)" without saying whether that includes the 6 optional stick-on feet (left off when racked), and the author never rack-mounted it. 6U is 266.7 mm, so the listing's 262 mm fits 6U and 272 mm doesn't. Measure without feet on arrival. **Re-checked 2026-11-12:** no report found of anyone rack-mounting a 12S4 or measuring it without feet. Figures: 262 mm in the seller manual on manuals.plus (per search snippet; the page refused direct reads), 271 mm in Alibaba listings (306 × 432 × 271), 272 mm/6.11U in [Byte Pursuits](https://bytepursuits.com/12-bay-homelab-nas-jmcd-12s4-from-taobao-upgrading-my-truenas-scale-server-optionally-rack-mountable), whose author fitted the 6 stick-on feet and never racked it ('you don't need to attach them if you install in the rack'). 262 mm body + ~10 mm feet would explain 272, but nothing confirms it. Unraid's '12S4 arrived' thread and the TrueNAS forum post have no measurements. No photo of a 12S4 in a rack found either (searched 2026-11-12). Byte Pursuits' photos of the case with its rack ears fitted show the ears running the full height of the front, reaching slightly past the body at top and bottom in the side view: a weak hint the body is under the ear height (≤ 6U), not proof. Still: measure the case without feet on arrival before mounting the U20 brush plate.

## How to verify / roll back

Nothing to roll back. Measure the case without its feet when it arrives; 6U is 266.7 mm.
