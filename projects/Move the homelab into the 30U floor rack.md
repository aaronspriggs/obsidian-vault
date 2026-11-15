---
type: project
status: active
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
- '[[UniFi UPS 2U]]'
parent: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
next_step: '2026-11-15: waiting on the 30U rack, the Enterprise 48, the PDU Pro and the 12S4 (arrivals not recorded). When the 12S4 arrives Aaron measures it without feet; then the gear moves to layout v17 and the runs are re-terminated to patch map v12.'
---

## Goal

Move everything from the full 12U wall rack into a 30U floor rack, laid out so the rebuilt Big Boi (6U), a second server, the AV receiver and the new switch all fit with room to grow. Split out of [Rebuild Big Boi](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>) on 2026-11-15, when that note was slimmed; the layout drafts v3 to v15 are in that note's git history (2026-11-11 to 2026-11-15).

## Status (2026-11-15)

Layout v17 is agreed, together with patch map v12. Ordered: the 30U rack, the USW Enterprise 48 PoE ($851 with shipping and tax), the PDU Pro and the rack accessories (2026-11-12, itemised list not recorded). Nothing has moved yet. The cabling half of the move is [Re-terminate and label the patch panels for the 30U rack](<Re-terminate and label the patch panels for the 30U rack.md>); the gear that leaves is in [Sell the network gear retired by the 30U rack move](<Sell the network gear retired by the 30U rack move.md>).

## Plan

### The racks

- **30U floor rack:** on casters, 500 lb rating, 18" (457 mm) rail to rail front to back (Aaron, 2026-11-15), so the 400 mm Enterprise 48 fits with its power cord just past the rear rail. It goes where the 12U is now; every house run has at least 6 ft of slack (Aaron, 2026-11-14).
- **12U wall rack today** (photo 2026-11-12, full): Big Boi in its 2U case, a cantilever shelf with three small boxes, about 1U open, UDM Pro, keystone patch panel, USW Pro Max 16 PoE, the Basement USW Flex 2.5G 8 PoE in a 1U keystone mount, UPS 2U, and a Tripp Lite Isobar at the bottom (what it feeds is unconfirmed). Its mountable depth is 14.6" (370 mm). ![Current 12U rack](<../attachments/Rack - 12U wall rack 2026-11-12.jpg>)

### Layout v17 (Aaron, 2026-11-15)

| U | What | Notes |
| --- | --- | --- |
| 30 | Patch panel A | UniFi 24-port keystone |
| 29 | USW Enterprise 48 PoE | 13.9 lb, 400 mm deep; the hottest device, see Open questions |
| 28 | Patch panel B | |
| 27 | UDM Pro | Routes only |
| 25–26 | Hub shelf (UniFi CLV, about 80 mm clear) | Hue Bridge, Lutron hub, HDHomeRun, Ting ONT, and the Zigbee dongle on a USB extension from Big Boi |
| 24 | Brush plate | Cords from above pass through to the PDU |
| 22–23 | PDU Pro | Outlets face front; on day one |
| 21 | Brush plate | Airflow and cables |
| 19–20 | Second server | The old 2U Mini-ITX case; hardware not chosen |
| 18 | Open | Airflow; absorbs a 272 mm 12S4; room for a 3U case later |
| 12–17 | Big Boi in the JMCD 12S4 | The heaviest server, kept low |
| 9–11 | CLV shelf plus 2U headroom | Sonos Amp for the back-patio speakers (64 mm tall); room for a possible Mac Studio (95 mm) |
| 8 | Open | Receiver heat |
| 4–7 | Denon AVR-S970H | On Aaron's StarTech SHELF-1U-12-FIXED-V (305 mm deep, 55 lb rating) |
| 3 | Open | |
| 1–2 | UPS 2U | |

The drawing is `attachments/Rack - 30U floor rack proposed layout.svg` (source of truth for the diagram; the scripts and published pages that draw from it are listed in the patch panel note): ![30U proposed layout](<../attachments/Rack - 30U floor rack proposed layout.svg>)

### Power

The UPS 2U's four battery outlets go to Big Boi, the UDM Pro, the Enterprise 48 and the PDU Pro (Aaron, 2026-11-15), so the hub shelf, second server and Sonos Amp are on battery through the PDU and no battery outlet is spare. The Denon (460 W rated) goes on a UPS surge-only outlet, not the PDU; so would a future GPU box. A second server on the UPS-fed PDU needs its own NUT client to shut down cleanly. Estimated UPS load is 350–400 W, about 15 min of runtime (an estimate, not measured); the PoE-only estimate is in the patch panel note.

### Weight

About 152–176 lb with 4 HDDs in Big Boi and 164–188 lb with 12, against the rack's 500 lb rating: UPS 30.9 lb ([UI specs](https://techspecs.ui.com/unifi/integrations/ups-2u-us)), Enterprise 48 plus UDM Pro about 22.5 lb, the 12S4 build 36–50 lb, Denon 21 lb.

### Denon AVR-S970H fit

434 W × 341 D mm, 167 mm tall with feet (237 mm with the antennas upright, so fold them back), 21 lb, operating 5–35 °C ([dimensions](https://manuals.denon.com/AVRS970H/NA/EN/GFNFSYzjlkmxom.php), [specs](https://manuals.denon.com/AVRS970H/NA/EN/GFNFSYbsjxinov.php)). Shelf plus receiver fit 4U. Its 288 mm body fits the 305 mm StarTech tray and is too deep for a CLV shelf. The feet sit 45 mm in from each side, so the tray's side lips shouldn't matter. No clearance figure is in the online manual.

## Decisions

- **2026-11-02 (Aaron): plan the 12S4 as 6U with 1U open above it for airflow.** The listing says 262 mm, one owner measured 272 mm (6U is 266.7 mm); the evidence is in [the case change note](<../changes/2026-10-26 Recorded the JMCD 12S4 case specs and an owner's build log.md>). v17's open U18 covers either figure.
- **2026-11-12 (Aaron): Big Boi definitely moves to the 12S4, and the old 2U case stays in the rack as a second server** for other uses, hardware not chosen. He wanted it away from Big Boi over heat concerns; v17 puts it above Big Boi with U18 open between them.
- **2026-11-12 (Aaron): only the USB radios need care.** The hubs have had no issues inside the rack. The Zigbee dongle goes up to the hub shelf on a USB extension; the ZWA-2 is too big for a shelf, so it goes on top of the rack or on the wall. The Ting ONT fits on the hub shelf; the CenturyLink ONT is outdoors in a box and stays there.
- **2026-11-12 (Aaron): the Denon goes on the existing StarTech shelf** from the 12U rack, reused, and on a surge-only outlet.
- **2026-11-12 (Aaron): layout v15 settled,** accounting for every current and planned piece of hardware; replaced by v17 on 2026-11-15. Still standing from it: room for a 3U Sliger GPU case for the second server (now U18–U20). Before buying one, check its depth against the rack's 18" (the CX3702 is 18"; it was rejected earlier because of the 12U's 370 mm limit) and power it from a surge-only outlet.
- **2026-11-12 (Aaron): rack accessories for v15 ordered, except the PDU Pro.** The Tripp Lite Isobar (IBAR12ULTRA, 1U) was to stand in for the PDU, fed from the wall and not from a UPS outlet, because Tripp Lite's UPS manuals advise against surge suppressors on a UPS output; the battery outlets were to go to Big Boi, the UDM Pro, the Pro Max 16 and the Aggregation, with everything else off battery. Replaced on 2026-11-15: the PDU Pro is ordered and goes in on day one, so the Isobar isn't used. Cost accepted: no manual UPS bypass.
- **2026-11-15 (Aaron): USW Enterprise 48 PoE ordered,** replacing the Pro Max 16, the Aggregation and the Basement Flex, which leave the rack (reasons in the patch panel note).
- **2026-11-15 (Aaron): layout v17,** agreed with patch map v12. v16, drafted the same day for the Enterprise 48, had Big Boi at U15–U20 under the U21 brush plate and the second server at U9–U10. v17 swaps the servers: Big Boi sits lower because it is the heaviest, and the open U18 above it removes the clash with the brush plate if the case is 272 mm.

## Open questions

- The 12S4's height without feet, measured on arrival.
- Rack top venting or a roof fan: the Enterprise 48 (150 W before PoE) sits at U29.
- The StarTech tray's inside width against the Denon's 434 mm.
- What the three small boxes on the 12U's shelf are, and what the Isobar feeds today.

## Changes

![[Changes.base#For this project]]
