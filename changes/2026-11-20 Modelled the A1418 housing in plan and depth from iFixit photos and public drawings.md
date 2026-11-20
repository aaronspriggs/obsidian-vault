---
date: 2026-11-20
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
---

# Modelled the A1418 housing in plan and depth from iFixit photos and public drawings

For [Convert a 21.5-inch Retina 4K iMac into a display for the top of the 30U rack](<../projects/Convert a 21.5-inch Retina 4K iMac into a display for the top of the 30U rack.md>). Aaron asked for a model of the 2017 21.5" Retina 4K (A1418, iMac18,2) housing to plan the printed parts against, then for its depth: how much room there is behind the display and whether each component fits. Nothing has been measured on a real unit yet; the donor isn't bought. The plan view is good to about ±3 mm at the centre. The depth model doesn't fit the parts Apple ships in the case, so it is off by a few millimetres or more somewhere, and calipers on the donor have to settle it.

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

Z runs from the front glass face toward the back. Free depth at a point is the external depth, minus the rear wall, minus the display stack (or minus the chin's front wall below Y 64).

External depth. Apple publishes only the 5 mm edge. The [dimensions.com 21.5" iMac (2019) drawing](https://www.dimensions.com/element/apple-imac-21-5-inch-2019) was parsed from its SVG, at about 0.867 units per mm. Its side view gives 38.8 mm deepest, at Y about 180, near the hinge. Its plan view gives 44.3 mm at the centre. iFixit's 2012 teardown says "over 4 cm" at the thickest point. Working range: 41.5 ±3 mm. Each silhouette is the maximum over the hidden axis, so the drawings bound the surface but don't fix it. Depth is at most the smaller of the two profiles at every point. The upper bound is `min(gx, gy)`, the smooth low guess is the product `gx·gy`, and the nominal case averages them.

Display stack. No outline drawing exists for the LM215UH1 (SD)(B1). The LM215WF3-SDA1 datasheet (same housing, 2012 non-Retina) gives 12.95 mm typical and 16.3 mm max. LG's LM215UH1-SPA1 (standalone 4K) is 13.8 mm. Modelled at 12.95–14.5 mm. The rear aluminium wall wasn't measured; it is modelled at 1.2–2.0 mm.

Component heights and their sources:

- Stock PSU: an open board, solder side to the display, parts facing the rear wall ([PSU guide 95634](https://www.ifixit.com/Guide/iMac+Intel+21.5-Inch+Retina+4K+Display+(2017)+Power+Supply+Replacement/95634)).
  - Tall zone (400 V bulk capacitors lying flat, plus the transformer, about X −75 to 5): 20 ±2 mm, scaled from the 8 mm capacitors in the component-side photo. An aftermarket listing gives 25 mm overall.
  - Rest of the board: 14 ±2 mm. The edge photo shows parts about 12 mm under the board, using its 1500 µF capacitor as the scale.
- HDD in bracket: 13 mm (drive label 9.5 mm).
- xstranger's plate plus R9513: 21 ±3 mm. `Mainboard.stl` is 5.7 mm; a standoff, the PCB and HDMI-height connectors were estimated.
- `Crossovers.stl`: 9.2 mm.
- Blower: about 18 mm, not published or measured.
- Mean Well LRS-150-12: 159 × 97 × 30 mm (datasheet).

Results, nominal case (41.5 mm max, display 13.5, wall 1.5). Free depth peaks at about 26 mm near (0, 170), the hinge. It is about 19 mm at the old PSU bay's middle (Y 95), 13–14 mm along its bottom edge (Y 70), and under 10 mm outside X ±150 and above Y 320. Fit checks give the minimum free depth over each footprint, tight / nominal / loose:

- Stock PSU tall zone, 20 mm: 8 / 12 / 16. **Fails in every case**, though the real one fits.
- Stock PSU rest of board, 14 mm: 2 / 9 / 15.
- HDD in bracket, 13 mm: 8 / 12 / 16.
- Blower, 18 mm: 12 / 17 / 22.
- xstranger plate plus R9513, 21 mm: 8 / 13 / 18. His finished build fits, so this fails too.
- `Crossovers.stl`, 9.2 mm: 11 / 15 / 18. Fits.
- LRS-150 at its best footprint-clear spot (upright in the old logic-board area, X 44 to 141, Y 108 to 267), 30 mm: 9 / 14 / 19. Fails.
- LRS-150 at the centre (Y 140 to 237, on top of the kept blower duct), 30 mm: 17 / 22 / 26. Fails.

The speakers fail the same way: the model leaves about 6 mm at X ±200, and the speaker enclosures are clearly deeper than that.

**What this means.** Parts Apple ships in the case don't fit the model, so the public inputs leave it too shallow by roughly 4 to 13 mm. The shortfall is everywhere, not just at the bottom. The likeliest cause is the display stack: the 13–14 mm figures are LG datasheet numbers for unlaminated modules, while the 2012-on iMac panel is laminated to its glass. In the display-lift photo (teardown step 3) its edge looks only about 5 mm thick. The drawing's profiles come next. Below is the uniform correction the model needs before every stock part clears by 1 mm over 95% of its footprint, for a range of stock PSU heights, and what the LRS-150 checks become with it:

| Stock PSU tall zone | Correction | LRS-150, best clear spot (min free) | LRS-150, centre (min free) |
|---|---|---|---|
| 16 mm | +3.8 mm | 17.9, no | 25.6, no |
| 20 mm | +7.8 mm | 21.9, no | 29.6, no |
| 25 mm | +12.8 mm | 26.9, no | 34.6, yes |

**The LRS-150-12 doesn't fit while the stock blower stays.** This rests mostly on the footprint. `place_lrs150()` tried every 159 × 97 mm placement, both ways round in 4 mm steps, against the kept speakers, blower, duct and exhaust grille. The old PSU bay is only about 58 mm tall above the chin, so the box can't sit there flat. The left bay is 99 mm wide between the speaker and the duct, and the blower blocks it upright. The only clear spots are upright in the old logic-board area, which is where the driver board goes. There, even the most generous calibration in the table (a 25 mm stock PSU) leaves at least 3 mm too little depth: 26.9 mm free for a 30 mm box. The centre is deep enough only if the stock PSU is 22 mm or more, and that is the blower's duct and exhaust path. So the choice is the external 12 V brick or the stock PSU.

**Calibrated model.** The `calibrated` case is the nominal shell with the display stack thinned to 5.7 mm. That is the +7.8 mm needed for a 20 mm stock PSU, applied where the likeliest error is. In it, every stock part clears over its whole footprint:

- PSU tall zone and rest of board: 20.0 and 16.5 mm minimum free, against 20 and 14 mm needed.
- HDD: 19.7 against 13.
- Blower: 24.7 against 18.
- xstranger's plate and board: 20.8 against 21. It clears across 100% of the sampled footprint; the corner sample is within its ±3 mm estimate.

Use it for planning until the donor is measured. The `raw-public-data` files are the uncorrected model, kept for comparison.

## Other builds' parts, measured for reference

Marco Markl's 27" set ([MakerWorld 1390804](https://makerworld.com/en/models/1390804-apple-imac-27-2017-conversion-to-5k-monitor)). Measured from his STLs (Aaron uploaded nine plus the USDZ, 2026-11-20; kept on the ClaudeCode VM at `~/project-files/imac-rack-display/markl-27in-5k-makerworld-1390804/`, not backed up and re-downloadable from MakerWorld; the measuring script is `stl_analyze.py` one level up): walls 2.0 mm (some 1.5 mm); hex vents 6.5 mm across flats (7.5 mm across corners); feet are 10.3 mm rings with 7.3 mm bores over the iMac's mounting points; M3 holes at 3.0 mm (self-tapping) and 3.4 mm (clearance), M2 at about 2.1 mm for the crossovers. Envelopes: driver-board cage 146 × 171 × 41 mm, controller-and-fan 135 × 125 × 40 mm, power-supply cage 174 × 112 × 24 mm (all 27"; the 21.5" case is shallower, so ours will be lower). The port cover is a 2.4 mm plate 123 × 19 mm with four 3.8 × 11.7 mm openings in a row plus a 25 × 1.7 mm slot; check whether the 21.5" port row matches before reusing its spacing. Cable ducts are 30 × 30 mm clips with a 6.8 × 12.4 mm channel.

[KevDoy's 27" 2014 set on Printables](https://www.printables.com/model/311111-apple-imac-27-2014-5k-monitor-conversion) has an I/O door replacing the RAM door, mounted with the original screws (27" only; also blocks Claude). A community [iFixit guide](https://www.ifixit.com/Guide/Turn+Your+iMac+2015+into+a+monitor/181638) (a 27" Retina) reused original openings: HDMI, DP and camera cables through two USB openings joined into one, audio out through the Ethernet opening, and the power button's own two wires, kept from the bottom left, soldered to the control module's power button pins. Its author dropped the speakers on crossovers as "too nasal".

## Measurements that close the model

With the display off, lay a straightedge across the rim and measure, with a depth gauge or ruler, from the rim plane to the inner rear wall at about ten points:

- centre at Y 70, 100, 170, 250 and 320
- the PSU bay's two ends
- X ±150 and ±200 at Y 170

Also measure the display assembly's thickness at its centre and edges, the stock PSU's height at the bulk capacitors and the transformer, the blower's height, and one speaker's depth. Those replace every estimated input above. The model takes them as table edits in `src/model3d.py`.

## Files

All are on the ClaudeCode VM under `~/project-files/imac-rack-display/a1418-housing-model/`, not backed up, and rebuilt by the scripts.

- Plan view: `a1418-housing-model.svg`, `a1418-model-on-ifixit-photo.jpg` and `features.json` (coordinates, features 1 to 25). The source photos are in `ifixit-originals/`.
- Depth: `model3d/`.
  - Fit checks: `fit-report.json` (every case), `calibration.json`, `lrs150-placements.json`, and `clearance-calibrated.json` and `clearance-raw-public-data.json` (a 50 × 25 mm grid).
  - Sections: `section-<case>-<Y or X><value>.svg` and `.png` for tight, nominal, loose and calibrated, at Y 70, 100, 165 and 250 and at X 0, 100 and −75.
  - Closed binary STLs, each in a calibrated and a raw-public-data version, for overlaying in PrusaSlicer: `a1418-rear-shell-*`, `a1418-display-*`, `a1418-stock-parts-*` and `a1418-proposed-parts-*` (xstranger's plates and the two LRS-150 test spots). The frame is X right, Y = −depth, Z up.
- Scripts: `src/build.py` (plan view) and `src/model3d.py` (depth, `python3 -I src/model3d.py`).
