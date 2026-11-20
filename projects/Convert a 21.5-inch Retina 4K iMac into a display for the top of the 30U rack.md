---
type: project
status: active
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
parent: '[[Move the homelab into the 30U floor rack]]'
next_step: '2026-11-20: Aaron reads MacRumors DIY 5K thread post 2,990 (a 21.5" 4K R9153 build) and page 17 posts 410-411 (power button wiring), which refuse Claude''s fetches; asks the AliExpress seller the four board questions below; then buys the 2017 donor (eBay listing ends about 2026-11-26) and lists the 2011 iMac for sale.'
---

## Goal

Put a 21.5" Retina 4K iMac shell on top of the 30U rack as a 4096×2304 monitor: its own panel and case driven by an aftermarket board, with a display input and the original power button working. Speakers are wanted but optional (Aaron, 2026-11-20). Aaron is treating it as a tinkering project.

## Status (2026-11-20)

Researched, nothing bought. The donor, board and layout are chosen (below). What it will display, and from which source, is open.

## Plan

**Donor:** a 2017 21.5" Retina 4K iMac (iMac18,2, panel LM215UH1 (SD)(B1)). Candidate: eBay seller Second Life Technology, i7-7700 / 16 GB / 1 TB Fusion / Radeon Pro 560, US $189.99 ($179.99 with coupon), 3 available. Before buying, get an About This Mac screenshot showing "Retina 4K" and confirm Find My is off. Apple lists the 21.5" at 52.8 cm wide, 45.0 cm tall with the stand, 17.5 cm stand depth, 5.66 kg ([specs](https://support.apple.com/en-us/112026)).

**Board:** AliExpress "For iMac A1418 21.5" 4K LM215UH1 Control Drive Board SDA1/SDB1/SPA2", silkscreen R9513 V4, $87.50 (4.8 stars, 26 sold, seen 2026-11-20). Inputs: 2× HDMI, 2× DP, 3.5 mm jack, 12 V barrel; it has a 4-pin speaker amp header (Aaron confirmed from the listing). The MacRumors DIY 5K thread calls the right chip for 21.5" 4K "R9153"; one of the two names is a transposition. It does not list the 2019 panel (SD B2), so the donor must be a 2015 or 2017. Questions for the seller: which panel cable ships (the 2015 and 2017 panels use different connectors, per [iFixit](https://ts.ifixit.com/Answers/History/673833)); whether DP and HDMI do 4096×2304 at 60 Hz; whether the 3.5 mm jack is an output; whether it supports DDC/CI (brightness from the source machine).

**Power:** 12 V, 8 A, 5.5×2.1 mm center-positive per a [Qarequ listing](https://qarequ.com/products/lcd-driver-board-for-lm215uh1-sda1-sdb1-spa1-spa2) for the same board; a MacRumors user recommends 8-10 A over 5 A for brightness. Use an external 12 V ≥8 A brick (e.g. Mean Well GST120A12; check its plug). The thread's first post says 21.5" 4K conversions have no room for an internal PSU. With the USB hub adding up to about 20 W, prefer a brick at the top of the range (10 A) or measure first. Measure real draw with an inline meter once running; it goes on a surge-only PDU outlet or the PDU, not a UPS battery outlet (none spare).

**Rear port map (draft, 2026-11-20):** every original opening gets a job, mounted on a printed carrier that screws onto the old logic board's standoffs, so connectors sit where the original ports were (measure port positions against the screw holes on the removed logic board before selling it). AC inlet: DC jack plus a DisplayPort panel mount (main input; DP rather than USB-C-to-DP for the RTX 3080 Ti workstation, since that cable failed on an RTX 3080 in [aiwipro's 27" build](https://github.com/aiwipro/5K-iMac-Studio-Display-Stock-Look)). Thunderbolt 3 opening 1: USB-C video input through a USB4 extension and a bidirectional USB-C-to-DP cable to the board's second DP input (aiwipro's method). Thunderbolt 3 opening 2: USB-C upstream for the USB hub. 4× USB-A: panel-mount extensions from an internal USB 3 hub board, powered by a 12-to-5 V buck converter (the board has no USB of its own). Ethernet: HDMI panel mount to the board's HDMI input, if an HDMI female fits the RJ45 opening (measure; otherwise file it). Headphone: 3.5 mm extension from the board's jack. SD slot: the button strip's ribbon. Kensington slot: unused.

**Printed parts (MK4, PETG or ASA):** the I/O carrier above; a removable plate in the AC inlet opening, held by keystone-style squeeze latches, carrying the DC jack and the DP panel mount; a collar for a 3.5 mm extension in the old headphone opening; a button pod under the chin, clear of the bottom air intake, with the button strip's ribbon routed out through the SD slot. Claude drafts these in parametric OpenSCAD once measured.

**Prior builds to borrow from (checked 2026-11-20):** no published dimensions exist for the A1418's rear openings or logic board port positions, so measuring stays necessary. [MakerWorld 2549010](https://www.makerworld.com/en/models/2549010) is a printed-parts set for a 2017 A1418 4K conversion (4K board, crossovers, 3 plates, about 4.5 h), from the designer of a 27" set; the page blocks Claude, so Aaron opens it and checks whether it covers rear ports. [KevDoy's 27" 2014 set on Printables](https://www.printables.com/model/311111-apple-imac-27-2014-5k-monitor-conversion) has an I/O door replacing the RAM door, mounted with the original screws (27" only; also blocks Claude). A community [iFixit guide](https://www.ifixit.com/Guide/Turn+Your+iMac+2015+into+a+monitor/181638) (a 27" Retina) reused original openings: HDMI, DP and camera cables through two USB openings joined into one, audio out through the Ethernet opening, and the power button's own two wires, kept from the bottom left, soldered to the control module's power button pins. Its author dropped the speakers on crossovers as "too nasal".

**Wiring:** the iMac power button soldered across the strip's power button; speakers on the 4-pin header, simplest in series without crossovers ([jorycz](https://github.com/jorycz/iMac-5K-display-convert) lists the 27" speaker pinout and a crossover option); set the OSD before sealing.

**Budget:** donor $190 + board $88 + brick ~$30 + extensions, adhesive and wire ~$40. Selling the donor's logic board, i7-7700, RAM, PSU and drives (estimated $100-150 net) and the 2011 iMac (estimated $80-150, boxed) covers most of it.

## Decisions

- **2026-11-20 (Aaron): 21.5", not 27".** The 21.5" is about the rack's width on top; the 27" (65 cm) would overhang. A 27" 5K conversion stays a possible desk project.
- **2026-11-20 (Aaron): Retina 4K donor, not the 2011 he owns.** The 2011 (MC812LL/A, 1080p, magnetic glass) was the cheaper build, with LM215WF3 kits at $30-60 and Juicy Crumb's DockLite at about $300; Aaron chose the sharper 4K panel and is comfortable opening glued iMacs from a past job. The 2011 gets sold whole with its box rather than parted out. Upgrading the 2011 instead (i7-2600S, 16 GB, SSD, Kepler GPU, about $210-330) was rejected: about a third of an M1's CPU for M1-mini money.
- **2026-11-20 (Aaron): must-haves are a display input and the original power button;** speakers optional; camera, USB hub and Ethernet dropped.
- **2026-11-20 (Aaron): reuse as many rear openings as possible,** rather than one loose cable hole. Draft port map above; it supersedes the earlier plan of two video inputs through both Thunderbolt openings.
- **2026-11-20: not two video ports in the AC inlet.** Nobody has published the inlet opening's size, and two screw-ear panel mounts need about 60 mm; the Thunderbolt and Ethernet openings carry the other inputs instead.
- **2026-11-20: external 12 V brick rather than USB-C power.** USB-C would need a 20 V PD trigger plus a 20-to-12 V buck converter inside a case with no room for a PSU; reconsider only if measured draw is well under 60 W.

## Open questions

- What it displays and from which machine (a server console through a KVM, a dashboard source, or a Mac). The rack plan has room for a possible Mac Studio, not one in hand.
- Measurements, taken at teardown: AC inlet opening size and edge thickness, recess depth, clearance to the stand hinge, how the inlet is held, Thunderbolt, USB-A and Ethernet opening sizes and spacing, port positions against the screw holes on the removed logic board, SD slot size, chin underside and intake slot, speaker connector and impedance.
- The rack's outside width on top, once the 30U rack arrives.
- Whether the board restores its input after a power cut.
