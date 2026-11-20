---
date: 2026-11-20
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
---

# Modelled the A1418 housing in plan and depth from iFixit photos and public drawings

For [Convert a 21.5-inch Retina 4K iMac into a display for the top of the 30U rack](<../projects/Convert a 21.5-inch Retina 4K iMac into a display for the top of the 30U rack.md>). Aaron asked for a model of the 2017 21.5" Retina 4K (A1418, iMac18,2) housing to plan the printed parts against, then for its depth: how much room there is behind the display and whether each component fits. Nothing has been measured on a real unit yet; the donor isn't bought. The plan view is good to about ±3 mm at the centre. The depth model uses LG's spec for the display assembly (11.05 mm). Its skin is fitted so the stock PSU, HDD and blower clear, giving a case 43.6 mm deep, inside the published 38.8–44.3 mm range. That fit assumes the stock PSU is about 16 mm, which is inferred, and the sides are unvalidated; see "What is still estimated".

## Plan view (X, Y)

Built from iFixit's full-resolution photos, pulled through the iFixit guide API. The head-on teardown shot ([teardown 92170](https://www.ifixit.com/Teardown/iMac+Intel+21.5-Inch+Retina+4K+Display+2017+Teardown/92170) step 4, 6079 × 4559 px) is the master. The board-lift shot from the [logic board guide 95631](https://www.ifixit.com/Guide/iMac+Intel+21.5-Inch+Retina+4K+Display+(2017)+Logic+Board+Replacement/95631) shows what the fan, drive and board hide. The bare-board shot (teardown step 6) gives port positions. Scale came from the 528 mm case width, with the 2.5" drive (69.85 mm) for the deeper interior plane. The second photo's scale came from xstranger's 24.0 mm stand-hinge bolt pair. Three standoffs seen in both photos agree within 1.5 mm. The SD-to-USB spacing from the board matches the exterior photo within 0.1 mm. Scaling from the bolts instead would put the case at 528.5 mm, a 0.1% change, so the print, Apple's case width and the drive agree to about 0.5%. The remaining error is picking points by eye (1–2 mm) and parts at different depths: about ±3 mm near the centre, ±5 mm at the edges.

Coordinates are mm, front view with the display removed: X from the case centre, right positive (mirror it from the back), Y up from the case bottom edge.

- Case 528 × 377 mm (height measured; Apple's VESA model spec gives 37.9 cm). The chin top edge, where the open interior ends, is at Y 64.
- Stand-hinge bolt pairs: X −57 at Y 187 and 163, matching xstranger's 24.0 mm spacing. The right pair at X +57 is inferred by symmetry; 113 mm between the pairs matches his `WiresHolder.stl`.
- Logic-board standoffs (69, 314), (178, 252), (50, 72), (165, 83). PSU standoff (36, 71). HDD-bracket standoffs (−144, 213) and (−144, 122). Top fan screw (−69, 301).
- Kept parts: left speaker X −238 to −138, Y 62 to 320; right speaker X 184 to 239 at the top, widening to X 155 below Y 114; blower centre (−75, 248), Ø 71 mm; exhaust grille plate behind the stand about X −41 to 38, Y 107 to 157.
- AC inlet: round, about Ø 43 mm, at (−2, 53) behind the stand.
- Rear port centres, all at Y 45 to 47: Ethernet 72, Thunderbolt 88 and 98, USB-A 110/124/137/150 (13.1 mm pitch), SD 174, headphone about 197 (±4).
- Removed parts: PSU board about 200 × 58 mm (X −155 to 46, Y 65 to 123), HDD bracket about 116 × 100 mm, logic board about 158 × 260 mm.

Checked against xstranger's STLs ([MakerWorld 2549010](https://www.makerworld.com/en/models/2549010)), independently of the bolt spacing used for scale. His `Mainboard.stl` plate, on the right bolt pair and run outward, covers X 52 to 151, Y 107 to 221: 8 mm clear of the fan duct and 4 mm clear of the right speaker. That is consistent with his real build, but inside the tolerance, so it doesn't prove the positions. `Crossovers.stl` on the left pair sits in the empty HDD bay at X −149 to −52, Y 155 to 195. His SD-slot cover is 26.4 mm long against about 27 mm from the photo. `Plug.stl` (41.5 × 13.3 mm) most likely fills the four widened USB-A openings, where the model gives about 45 mm: either the openings are narrower than the 5.5 mm assumed or the pitch reads about 1 mm high. Check at teardown.

## Depth (Z)

Z runs from the front glass face toward the back. Free depth at a point is the external depth, minus the rear wall, minus the display assembly (or minus the chin's front wall below Y 64).

**Display assembly: 11.05 mm, sourced.** The A1418's glass-fused display is LG LM215WF3-SDD1, Apple 661-7109 ([iFixit answer](https://www.ifixit.com/Answers/View/428399/Is+there+no+way+to+replace+a+new+iMac's+glass+panel)). Its outline is 528.3 × 318.765 × 11.05 mm ([Taiwan Screen](https://www.twscreen.com/en/lcdpanel/1539/lgdisplay/lm215wf3-sdd1/21.5/1920x1080-Monitor-LCD-Panel), [lcds-screen](https://www.lcds-screen.com/products/LM215WF3-SDD1_LG-Display.html)). The 528.3 mm width is the full front glass, so this is the whole assembly. The 4K LM215UH1 (SD)(B1) sits in the same housing but its outline isn't published, so it is modelled at 11.05 ±1 mm. The 13–14 mm figures first used were for LG's unlaminated panels and were wrong for this case.

**External depth.** Apple publishes only the 5 mm edge. The [dimensions.com 21.5" iMac (2019) drawing](https://www.dimensions.com/element/apple-imac-21-5-inch-2019) was parsed from its SVG at about 0.867 units per mm. Its side view gives 38.8 mm deepest, at Y about 180 near the hinge. Its plan view gives 44.3 mm at the centre. iFixit's 2012 teardown says "over 4 cm". The model starts at 41.5 ±3 mm. Each view is a silhouette, the maximum over the hidden axis, so together they bound the surface without fixing it. The upper bound is `min(gx, gy)`, the low guess is the product `gx·gy`, and the nominal case averages them. iFixit's 2012 side photo is shot about 15° from behind (the Apple logo shows foreshortened), so it can't give an absolute depth. Its shape does agree with the drawing: the back tapers toward the bottom, and the deepest point is near the hinge. dimensions.com's separate [Retina 21.5" (2015) drawing](https://www.dimensions.com/element/apple-imac-retina-21-5-2015) is the same artist's stylised outline. Its side view measures only about 30 mm deep, give or take 3 mm of line width, so the drawings aren't independent and can't narrow the range. No CAD model of the A1418 housing was found on the free sites (searched 2026-11-20).

**Rear wall:** not published, modelled at 1.5 ±0.5 mm.

Component heights and sources:

- **Stock PSU:** an open board, solder side toward the display, parts facing the rear wall ([PSU guide 95634](https://www.ifixit.com/Guide/iMac+Intel+21.5-Inch+Retina+4K+Display+(2017)+Power+Supply+Replacement/95634)).
  - Two retail listings give 0.98 in (25 mm) overall.
  - From the photos, the tall zone (400 V bulk capacitors lying flat plus the transformer, about X −75 to 5) is about 20 mm.
  - The case bounds it tighter, as the calibration below shows: about 16 mm.
  - Rest of the board: 14 ±2 mm, from the edge photo, using its 1500 µF capacitor as the scale.
- **HDD in bracket:** 13 mm (drive label 9.5 mm).
- **Blower:** about 18 mm, not published.
- **xstranger's plate plus R9513:** about 21 mm. `Mainboard.stl` is 5.7 mm; the standoff, PCB and connector heights are estimated.
- **`Crossovers.stl`:** 9.2 mm.
- **Mean Well LRS-150-12:** 159 × 97 × 30 mm (datasheet).

**Calibration.** Parts Apple ships must fit. The model deepens the skin in proportion to the bulge, keeping the 5 mm edge fixed, until every stock part clears by 1 mm over 95% of its footprint. The case depth that requires depends on how tall the stock PSU's tall zone is:

| PSU tall zone | Max case depth needed | LRS-150 min free, best clear spot | LRS-150 min free, centre |
|---|---|---|---|
| 14 mm | 43.4 mm | 17.8 | 25.9 |
| 16 mm | 43.6 mm | 17.9 | 26.1 |
| 18 mm | 46.8 mm | 20.0 | 28.8 |
| 20 mm | 49.9 mm | 22.1 | 31.6 |
| 25 mm | 57.8 mm | 27.3 | 38.4 |

Every source puts the deepest point at 38.8–44.3 mm. If those are right, the PSU's tall zone can't be much over 16 mm.

That 16 mm is **inferred from the case depth, not sourced**. It contradicts the photo estimate (about 20 mm) and the listings (25 mm). That the 25 mm includes the end brackets is a hypothesis, not checked. So the PSU check here is a fitted parameter, not independent evidence. The PSU's real height is the weakest input and the first thing to measure. If it is 20 mm, the drawings are about 6 mm too shallow.

**The `calibrated` model:** display 11.05 mm (sourced), wall 1.5 mm (estimate), case 43.6 mm deep (inside the sourced range), PSU tall zone 16 mm (inferred). The PSU, HDD and blower clear in it. `nominal` (41.5 mm deep) is kept as `raw-public-data` for comparison.

**The sides are not validated.** All three checks sit within X ±80 of the centre, so nothing tests the profile's side-to-side shape. The speakers would, since they stay at X ±140 to 239 where the model leaves 6–9 mm, but no depth is published for them. iFixit's [left speaker guide 95629](https://www.ifixit.com/Guide/iMac+Intel+21.5-Inch+Retina+4K+Display+(2017)+Left+Speaker+Replacement/95629) shows them only front-on. Treat free depth outside about X ±120 as unvalidated, including the 17 mm limit at the R9513's outer edge. If the speakers turn out deeper, the fix is the `shape` blend toward the silhouette upper bound, which deepens the sides, not the max depth.

Calibrated free depth: 31 mm peak near (0, 170); 21–24 mm across the old PSU bay's middle (Y 95, X −100 to 0); 13–17.5 mm along its chin edge (Y 70); 6–9 mm at X ±200; under 14 mm above Y 320.

Minimum free depth per part, nominal / calibrated:

- PSU tall zone, 16 mm: 14.6 / 15.9
- PSU rest of board, 14 mm: 11.1 / 12.2
- HDD, 13 mm: 14.4 / 15.6
- Blower, 18 mm: 19.4 / 20.9
- `Crossovers.stl`, 9.2 mm: 17.3 / 18.7
- xstranger's plate plus board, 21 mm estimated: 15.4 / 16.7. Free depth is 16.7 mm at its outer edge (X 150) and about 24 mm mid-plate. His finished build fits, so its stack is at most about 17 mm out there; treat that as the R9513's limit at that edge.

**The LRS-150-12 doesn't fit while the stock blower stays, whatever the stock PSU's height.** `place_lrs150()` tried every 159 × 97 mm placement, both ways round in 4 mm steps, against the kept speakers, blower, duct and exhaust grille. The old PSU bay is only about 58 mm tall above the chin, so the box can't sit there flat. The left bay is 99 mm wide between the speaker and the duct, and the blower blocks it upright. The only clear spots are upright in the old logic-board area, where the driver board goes. Every row of the table leaves them short of the 30 mm needed: 17.8 mm at a 14 mm PSU, up to 27.3 mm at 25 mm, where the case would be 57.8 mm deep. The centre is deep enough only at an 18 mm PSU or more, and it sits on the blower's duct. So it's the external 12 V brick or the stock PSU.

## What is still estimated

These inputs are still unsourced:

- **stock PSU height:** inferred, 16 mm against estimates of 20–25
- **4K panel thickness:** taken as the same as the 2K assembly
- **rear wall:** 1.5 ±0.5 mm
- **blower and speaker depths:** the speakers mean the sides are unvalidated
- **R9513 stack**
- **skin shape between the two drawing views:** ±2 mm at the corners

One caliper pass on the donor settles all of them. None of them changes the LRS-150 result.

## Other builds' parts, measured for reference

**Markl's build notes** (read from Aaron's screenshots 2026-11-20). Marco Markl's [27" 2017 5K mounting system](https://makerworld.com/en/models/1390804-apple-imac-27-2017-conversion-to-5k-monitor) (read from Aaron's screenshots; MakerWorld blocks Claude): hex-vented printed cages for the driver board, controller and power supply on arms bolted to the original logic-board mounting points, edge cable ducts and a port cover, with no drilling. Notes from it: the power button is wired by splitting the controller's ribbon cable and joining the iMac button's two wires to its GND and POWER wires (labelled on the board), which keeps the controller's own button working; a special screw under the original logic board is reused for a bracket; the fan was "not strictly necessary" and noisy; speaker sound on crossovers "moderate at best"; PETG, ABS or ASA, with supports on the driver-board and controller parts. Our 21.5" parts follow the same style, anchored on the measured logic-board standoffs. His STL measurements (walls, vents, M3 holes, cage envelopes) are in the change note above.

Marco Markl's 27" set ([MakerWorld 1390804](https://makerworld.com/en/models/1390804-apple-imac-27-2017-conversion-to-5k-monitor)). Measured from his STLs (Aaron uploaded nine plus the USDZ, 2026-11-20; kept on the ClaudeCode VM at `~/project-files/imac-rack-display/markl-27in-5k-makerworld-1390804/`, not backed up and re-downloadable from MakerWorld; the measuring script is `stl_analyze.py` one level up): walls 2.0 mm (some 1.5 mm); hex vents 6.5 mm across flats (7.5 mm across corners); feet are 10.3 mm rings with 7.3 mm bores over the iMac's mounting points; M3 holes at 3.0 mm (self-tapping) and 3.4 mm (clearance), M2 at about 2.1 mm for the crossovers. Envelopes: driver-board cage 146 × 171 × 41 mm, controller-and-fan 135 × 125 × 40 mm, power-supply cage 174 × 112 × 24 mm (all 27"; the 21.5" case is shallower, so ours will be lower). The port cover is a 2.4 mm plate 123 × 19 mm with four 3.8 × 11.7 mm openings in a row plus a 25 × 1.7 mm slot; check whether the 21.5" port row matches before reusing its spacing. Cable ducts are 30 × 30 mm clips with a 6.8 × 12.4 mm channel.

[KevDoy's 27" 2014 set on Printables](https://www.printables.com/model/311111-apple-imac-27-2014-5k-monitor-conversion) has an I/O door replacing the RAM door, mounted with the original screws (27" only; also blocks Claude). A community [iFixit guide](https://www.ifixit.com/Guide/Turn+Your+iMac+2015+into+a+monitor/181638) (a 27" Retina) reused original openings: HDMI, DP and camera cables through two USB openings joined into one, audio out through the Ethernet opening, and the power button's own two wires, kept from the bottom left, soldered to the control module's power button pins. Its author dropped the speakers on crossovers as "too nasal".

**xstranger's build in full** (read from Aaron's screenshots 2026-11-20). no published dimensions exist for the A1418's rear openings or logic board port positions, so measuring stays necessary. [MakerWorld 2549010](https://www.makerworld.com/en/models/2549010), by xstranger, is a finished 2017 A1418 4K build (text and comments read from Aaron's screenshots 2026-11-20): an AliExpress 4K A1418 board on a printed `Mainboard.stl` adapter, fixed right of the fan tube on the two stand-hinge bolts (swapped for longer ones), crossovers on the matching bolts to its left, cables behind the fan tube; the **original PSU kept in its mount**, with a bought mating plug on its 6-pin harness (three +12 V, three ground) feeding the stock fan, a DC PWM fan controller (knob on the rear housing) and the display board; the PSU runs as soon as it's plugged in, no modification. The original fan tube reused with the heat pipes removed. USB openings slightly widened for cable passthrough, finished with a printed TPU gasket. Control buttons moved onto the stand. The iMac power button left unused; the designer says it only signalled the logic board and could be soldered in parallel with the board's power button. One commenter (PortoLAB, 2026-10-27) got a high-pitched whine from the original PSU with all lines reading 12 V and suspected too little load; the designer runs iMac PSUs in three monitors without it. A reviewer printed at 0.12 mm, 3 walls, 25% infill. Next: compare the designer's AliExpress board link with the R9513 listing; if it's the same board, use his `Mainboard.stl`. His nine STLs (Aaron uploaded them 2026-11-20) are on the VM at `~/project-files/imac-rack-display/xstranger-21in-4k-makerworld-2549010/`, measured with `stl_holes.py` one level up. `Mainboard.stl` holds the driver board on four M3 holes in a **56 × 106 mm** rectangle and fixes to the stand-hinge bolts (**24.0 mm apart**). The others hold the crossovers, the 7-button strip on the stand, the fan knob (`PWM.stl`, not needed) and small fillers. Their placement in the housing is in the plan-view section. Whether his `Mainboard.stl` fits the R9513 depends on its mounting holes matching 56 × 106 mm; ask the seller or measure on arrival. The two 27" builds are summarised in the section above.

## VESA build layout (added 2026-11-20)

Aaron wants the finished display on a monitor arm, so the layout uses Apple's VESA Mount Adapter Kit in place of the stand. Drawn by `src/layout.py` over the plan view (`layout/a1418-build-layout.svg` and `.png`, coordinates in `layout/build-layout.json`) and checked for depth by `src/model3d.py` (calibrated case).

**The kit.** Apple's kit for the 21.5" (Late 2015, 2017 and 2019) has a mechanism plate inside, a tongue through the stand slot, a 100 × 100 mm U-channel bracket outside and two Pentalobe P15 screws. Fitting it needs the logic board out, then the stand and hinge removed ([iFixit answer 581424](https://www.ifixit.com/Answers/View/581424)); the plate reuses the four hinge-mechanism screws. Part numbers differ by year. The bookyard lists the 2015 kit as tongue 923-00614, plate 923-00561, bracket 923-0421, and the 2017 kit as tongue 923-01674, plate 923-01625, bracket 923-0421; only the bracket is shared. Buy the 2017 set and confirm part numbers with the seller. Sources seen 2026-11-20: beetstech, used kit SKU 2007-U00, $86.15 ("fits 2015/2017/2019", plate year not stated); macrecycling, bracket 923-0421 alone, $44 used, no plate, tongue or screws. In the beetstech kit photo the plate's holes are 24 × 113 mm apart, consistent with the hinge bolt pairs at X ±56.7, Y 163.4 and 187.4 (feature 20 and the plan view). That photo has not been confirmed as the 2017 plate. Plate outline from the photo, about X −62 to 62, Y 150 to 200; bracket about 130 mm square centred on X 0, Y 175, VESA holes about (±50, 125) and (±50, 225). All three are estimates to ±5 mm. Apple gives its built-in-VESA 21.5" as 37.9 cm tall and 6.6 cm deep including the adapter ([Late 2015 Retina 4K specs](https://support.apple.com/en-us/112034)), so the VESA plane sits about 22 mm behind the 43.6 mm deepest point of the calibrated case.

**Why the driver board moves.** With the stand gone, the four hinge screws carry the whole cantilevered display, so nothing printed goes in that clamp stack, where it would creep. xstranger's `Mainboard.stl` and `Crossovers.stl` mount on those bolts and his `Controls.stl` mounts on the stand, so all three drop out. The R9513 goes on a printed carrier on the logic-board standoffs instead (Markl's style), and the speakers run in series without crossovers.

**Placement and depth (calibrated model).**

| Part | Plan position (mm) | Height | Free depth: min / mean | Fits |
|---|---|---|---|---|
| VESA mechanism plate (inside) | X −62..62, Y 150..200 | 4 ±2 (est.) | 28.2 / 29.9 | all of it |
| R9513 on carrier, tall parts | X 70..120, Y 100..250 | 20 ±3 (carrier 3 + standoff 5 + PCB 1.6 + connector ~9) | 20.4 / 24.9 | all of it |
| R9513 carrier, extension | X 120..150, Y 100..250 | 20 ±3 | 16.7 / 20.1 | 53%; flat parts (≤ ~16 mm) only, and unvalidated past X 120 |
| Fan PWM controller + NTC | X −135..−45, Y 68..118 (old PSU bay) | 12 ±3 | 13.8 / 20.4 | all of it |
| USB 3 hub on a printed tray (Aaron wants it if it fits) | X −135..−66, Y 120..205 (empty HDD bay) | 17 ±3 (tray 2 + standoff 3 + PCB 1.6 + USB-A socket ~7 + plug) | 19.4 / 24.6 | all of it |
| 12-to-5 V buck for the hub | X −45..−20, Y 78..105 | 12 ±3 | 18.9 / 22.2 | all of it |

The carrier zone as drawn runs from the board's standoffs at (50, 72), (69, 314), (178, 252) and (165, 83), stepping in at the right speaker's lower edge; run the board's long axis vertical so its tall connectors stay inside X 120. The fan controller stays left of X −138, the left speaker's inner edge. The DC jack and DisplayPort panel mount go on a plate in the AC inlet opening (centre (−1.8, 53), r 21.6). There the case is about 26 mm deep, so the VESA plane is about 40 mm behind the plate. The plate sits below the bracket (bottom edge about Y 110), so a straight DP plug fits and the cables drop out under the arm. The exhaust grille (Y 107 to 157) sits behind the bracket's lower half. Apple's VESA models presumably vent through the open U-channel the same way; that isn't sourced, so check airflow under load. No iFixit guide covers removing the 2017 hinge. It is spring-loaded, so keep the stand folded and held while its screws come out. The alternative to the kit was a clamp adapter on the stock stand foot ([VIVO STAND-MACB](https://www.newegg.com/p/9SIA3BG2EN8103), [Tether Tools Rock Solid](https://tethertools.com/product/imac-vesa-vu-kit-connects-to-imac-base/)); see the project note's Decisions. The power button is at about (−227, 37) ±10 mm, from the dimensions.com rear view and the left-speaker cable groove (iFixit 95629). The button pod sits under the chin at about X −215 to −145, clear of the bottom intake, which still has to be measured.

**Power and USB (Aaron, 2026-11-20).** External brick: a Mean Well GST160A12-R7B, 12 V 11.5 A, 138 W ([spec](https://www.meanwell.com/Upload/PDF/GST160A/GST160A-SPEC.PDF)). It covers the board at up to about 96 W (8 A per the Qarequ listing), the hub at up to about 20 W and the fan. Its plug is a 4-pin locking DIN (distributors list Kycon KPPX-4P), which suits 11.5 A better than a 5.5×2.1 barrel. So the inlet plate takes a matching 4-pin panel jack, wired inside to the board, the buck and the fan controller; confirm the jack part against the spec before ordering. The hub's upstream is USB-C through one Thunderbolt opening, to the same machine as the video. Four panel-mount USB-A extensions run along the bottom edge to the USB-A openings (X 110 to 150).

**Arm load.** Apple doesn't publish the built-in-VESA model's weight. The stand model weighs 5.66 kg, which bounds the converted unit from above. Taking out the stand, logic board and heatsink, PSU and drive, and adding the kit, R9513 and printed parts, puts it at roughly 4 to 4.5 kg. That estimate isn't sourced; weigh the unit before choosing the arm. Gas-spring arms have a minimum load as well as a maximum, so the arm's rated range must include roughly 3.5 to 6 kg.

## Measurements that close the model

With the display off, lay a straightedge across the rim and measure, with a depth gauge or ruler, from the rim plane to the inner rear wall at about ten points:

- centre at Y 70, 100, 170, 250 and 320
- the PSU bay's two ends
- X ±150 and ±200 at Y 170

Also measure the display assembly's thickness, the stock PSU's height at the bulk capacitors and the transformer, the blower's height, and one speaker's depth. For the VESA layout, also measure the mechanism plate's outline and thickness, the R9513's outline, hole pattern and tallest part, and weigh the finished unit. Those replace the remaining ranges. The model takes them as table edits in `src/model3d.py`.

## Files

All are on the ClaudeCode VM under `~/project-files/imac-rack-display/a1418-housing-model/`, not backed up, and rebuilt by the scripts.

- Plan view: `a1418-housing-model.svg`, `a1418-model-on-ifixit-photo.jpg` and `features.json` (coordinates, features 1 to 25). The source photos are in `ifixit-originals/`.
- Depth: `model3d/`.
  - Fit checks: `fit-report.json` (every case), `calibration.json`, `lrs150-placements.json`, and `clearance-calibrated.json` and `clearance-raw-public-data.json` (a 50 × 25 mm grid).
  - Sections: `section-<case>-<Y or X><value>.svg` and `.png` for tight, nominal, loose and calibrated, at Y 70, 100, 165 and 250 and at X 0, 100 and −75.
  - Closed binary STLs, each in a calibrated and a raw-public-data version, for overlaying in PrusaSlicer: `a1418-rear-shell-*`, `a1418-display-*`, `a1418-stock-parts-*` and `a1418-proposed-parts-*` (the VESA layout: mechanism plate, R9513 carrier zone, fan controller, plus the two LRS-150 test spots; xstranger's hinge-bolt plates were dropped from it on 2026-11-20). The frame is X right, Y = −depth, Z up.
- Build layout: `layout/a1418-build-layout.svg` and `.png`, `layout/build-layout.json`.
- Scripts: `src/build.py` (plan view), `src/model3d.py` (depth, `python3 -I src/model3d.py`) and `src/layout.py` (build layout).
