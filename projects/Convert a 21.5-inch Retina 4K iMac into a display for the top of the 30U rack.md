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

**Prior builds to borrow from (checked 2026-11-20):** no published dimensions exist for the A1418's rear openings or logic board port positions, so measuring stays necessary. [MakerWorld 2549010](https://www.makerworld.com/en/models/2549010), by xstranger, is a finished 2017 A1418 4K build. It uses an AliExpress 4K board on a printed `Mainboard.stl` adapter fixed to the right stand-hinge bolts, with crossovers on the left pair. The **original PSU stays in its mount** and feeds the board, the stock fan and a PWM fan controller through a mating plug on its 6-pin harness (three +12 V, three ground), unmodified. The fan tube is reused with the heat pipes removed. One commenter (PortoLAB, 2026-10-27) got a high-pitched whine from that PSU and suspected too little load. His `Mainboard.stl` holds the driver board on four M3 holes in a **56 × 106 mm** rectangle; whether it fits the R9513 depends on its holes matching, so ask the seller or measure on arrival. His full build notes, the nine STLs (on the VM at `~/project-files/imac-rack-display/xstranger-21in-4k-makerworld-2549010/`) and two 27" builds are in the change note above.

**Layout model Aaron likes (2026-11-20):** Marco Markl's [27" 2017 5K mounting system](https://makerworld.com/en/models/1390804-apple-imac-27-2017-conversion-to-5k-monitor) (read from Aaron's screenshots; MakerWorld blocks Claude): hex-vented printed cages for the driver board, controller and power supply on arms bolted to the original logic-board mounting points, edge cable ducts and a port cover, with no drilling. Notes from it: the power button is wired by splitting the controller's ribbon cable and joining the iMac button's two wires to its GND and POWER wires (labelled on the board), which keeps the controller's own button working; a special screw under the original logic board is reused for a bracket; the fan was "not strictly necessary" and noisy; speaker sound on crossovers "moderate at best"; PETG, ABS or ASA, with supports on the driver-board and controller parts. Our 21.5" parts follow the same style, anchored on the measured logic-board standoffs. His STL measurements (walls, vents, M3 holes, cage envelopes) are in the change note above.

**Housing model (2026-11-20, planning only):** a plan-view and depth model of the A1418 housing, built from iFixit's full-resolution photos, xstranger's STLs and the dimensions.com drawing. Sources, coordinates, fit checks and files are in [the change note](<../changes/2026-11-20 Modelled the A1418 housing in plan and depth from iFixit photos and public drawings.md>). The files are on the VM at `~/project-files/imac-rack-display/a1418-housing-model/`, including STLs to overlay in PrusaSlicer.

The plan view is good to about ±3 mm at the centre and ±5 mm at the edges. Coordinates are mm from the case centre, right positive, Y up from the bottom edge.
- Stand-hinge bolt pairs: X ±57, Y 163 and 187.
- Logic-board standoffs: (69, 314), (178, 252), (50, 72), (165, 83).
- Rear ports: Y 45–47.
- Old PSU board: X −155 to 46, Y 65 to 123.

The depth model uses LG's spec for the A1418 display assembly (11.05 mm, glass included). It is calibrated so every part Apple ships fits, which gives a case 43.6 mm deep, inside the drawings' 38.8–44.3 mm range. Plan against the `calibrated` files. Free depth behind the display is 31 mm at the hinge, 21–24 mm across the old PSU bay, 13–17 mm along the chin and 6–9 mm near the speakers. xstranger's plate has about 17 mm at its outer edge, which caps the R9513 stack there. The remaining ranges (4K panel thickness, rear wall, blower) close with one caliper pass, at the points listed in the change note.

**Wiring:** the iMac power button's two wires joined to the GND and POWER wires of the button strip's ribbon (Markl's method); speakers on the 4-pin header, simplest in series without crossovers ([jorycz](https://github.com/jorycz/iMac-5K-display-convert) lists the 27" speaker pinout and a crossover option); set the OSD before sealing.

**Budget:** donor $190 + board $88 + brick ~$30 + extensions, adhesive and wire ~$40. Selling the donor's logic board, i7-7700, RAM, PSU and drives (estimated $100-150 net) and the 2011 iMac (estimated $80-150, boxed) covers most of it.

## Decisions

- **2026-11-20 (Aaron): 21.5", not 27".** The 21.5" is about the rack's width on top; the 27" (65 cm) would overhang. A 27" 5K conversion stays a possible desk project.
- **2026-11-20 (Aaron): Retina 4K donor, not the 2011 he owns.** The 2011 (MC812LL/A, 1080p, magnetic glass) was the cheaper build, with LM215WF3 kits at $30-60 and Juicy Crumb's DockLite at about $300; Aaron chose the sharper 4K panel and is comfortable opening glued iMacs from a past job. The 2011 gets sold whole with its box rather than parted out. Upgrading the 2011 instead (i7-2600S, 16 GB, SSD, Kepler GPU, about $210-330) was rejected: about a third of an M1's CPU for M1-mini money.
- **2026-11-20 (Aaron): must-haves are a display input and the original power button;** speakers optional; camera, USB hub and Ethernet dropped.
- **2026-11-20 (Aaron): reuse as many rear openings as possible,** rather than one loose cable hole. Draft port map above; it supersedes the earlier plan of two video inputs through both Thunderbolt openings.
- **2026-11-20: not two video ports in the AC inlet.** Nobody has published the inlet opening's size, and two screw-ear panel mounts need about 60 mm; the Thunderbolt and Ethernet openings carry the other inputs instead.
- **2026-11-20: external 12 V brick rather than USB-C power.** USB-C would need a 20 V PD trigger plus a 20-to-12 V buck converter inside a case with no room for a PSU; reconsider only if measured draw is well under 60 W.
- **2026-11-20 (Claude): the depth model is checked against the parts Apple ships.** Both views of the dimensions.com drawing are silhouettes, so they only bound the rear surface; averaging the side and plan views (38.8 and 44.3 mm deep) was rejected. The display thickness comes from LG's spec for the A1418 assembly, and the skin is deepened, with its 5 mm edge fixed, until the stock PSU, HDD and blower fit. LG's unlaminated-panel thickness (13.5 mm) was rejected, as were the retail listings' 25 mm PSU height, which would need a 58 mm deep case.

## Open questions

- Power: the MakerWorld build shows the original PSU can stay, but Aaron (2026-11-20) is wary of the whine one builder reported and leans to the external 12 V brick. An internal Mean Well LRS-150-12 (159 × 97 × 30 mm) is out while the stock blower stays. The only places its footprint clears the kept parts are in the old logic-board area, where the driver board goes, and even there it has at most 18 mm of the 30 it needs, 20 mm even in a case deeper than any source allows (see the change note above). So the choice is the external brick or the stock PSU. Decide before ordering. Aaron's LRS-200 end brackets ([MakerWorld 2305588](https://makerworld.com/en/models/2305588), copy at `~/project-files/imac-rack-display/meanwell-lrs-200-brackets/`) are out with it.
- Cooling: Aaron doesn't want a manual fan knob (2026-11-20). Proposed: keep the stock blower and its intake-bottom, exhaust-behind-stand path, driven by a temperature-controlled 4-wire PWM module with an NTC probe on the board heatsink; a Noctua 40 mm on the heatsink only if testing shows hot spots. Apple fans swap 12 V and ground against the standard pinout (aiwipro).
- Board: xstranger's AliExpress link opens a MacPanel Store listing (LM215UH1 SDA1/SDB1/SDC1 variants, $83.26, 1 review at 1.0 stars, 2 sold, seen 2026-11-20), not the R9513 listing; his `Mainboard.stl` fits his board. Compare the two boards' mounting holes before choosing.

- What it displays and from which machine (a server console through a KVM, a dashboard source, or a Mac). The rack plan has room for a possible Mac Studio, not one in hand.
- Measurements, taken at teardown: AC inlet opening size and edge thickness, recess depth, clearance to the stand hinge, how the inlet is held, Thunderbolt, USB-A and Ethernet opening sizes and spacing, port positions against the screw holes on the removed logic board, SD slot size, chin underside and intake slot, speaker connector and impedance. For the depth model: rim-plane-to-inner-rear-wall depth at the ten points listed in the change note, display assembly thickness (centre and edge), stock PSU height at the bulk capacitors and transformer, blower height and one speaker's depth.
- The rack's outside width on top, once the 30U rack arrives.
- Whether the board restores its input after a power cut.
