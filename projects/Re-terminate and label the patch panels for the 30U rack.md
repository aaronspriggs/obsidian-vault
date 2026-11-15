---
type: project
status: active
priority: medium
system:
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
- '[[UniFi (UDM Pro)]]'
parent: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
next_step: '2026-11-15: Aaron reviews map v12 and rack v16 on the page, then decides on buying the Enterprise 48 and returning the Aggregation. When the map settles, redraw the doc''s two widgets; then Aaron re-terminates to the map during the 30U move.'
---

## Goal

Every house run lands on a labelled patch panel position in the 30U rack (layout v15), with one ID used on the panel, both cable ends and the UniFi port name, so nothing needs tracing.

## Status (2026-11-15)

Aaron listed every run in the house, existing and planned (inventory below). Port map v6 drafted (panel B over the UDM since v4; grouped by function since v5; APs on the Basement Flex since v6); nothing re-terminated yet. The 30U rack goes where the 12U is now, and every run has at least 6 ft of slack (Aaron 2026-11-14).

## Run inventory (Aaron, 2026-11-15)

Existing runs (14), all home-run to the basement utility room:

| Room | Runs | In use |
| --- | --- | --- |
| Aaron's office | 5 now (4 on one wall, 1 on the other); 3 planned (Aaron 2026-11-15: desk Flex, Front AP, one spare stay; two cables re-pulled elsewhere) | Single run feeds the USW Flex 2.5G 5 under the desk. Of the 4, one feeds the U7-Pro-Wall-Front AP; 3 dark (old desk position) |
| Living room | 2 | TV area (PS5 now; will feed the spare USW Flex for PS5, Switch 2, Apple TV, maybe the Denon); wall-mounted Raspberry Pi panel |
| Kitchen | 3 (above cabinets) | 2 for the Sonos pair; 1 dark |
| Bar alcove | 1 | U7-Pro-Wall-Back AP |
| Front hallway | 1 | PoE converter for the Ring keypad |
| Basement | 1 | Future ceiling-mount AP (not installed) |
| 2nd floor | 1 | Upstairs utility room USW Flex 2.5G 8 PoE; all other 2nd-floor runs come off that switch |

Planned runs (8 or 9): front hallway UniFi Siren (PoE, near the doorbell); front hallway doorbell speaker or chime (maybe); outside entry G6 Entry doorbell (PoE+, 16 W, copper); basement guest room (desk or TV spot); basement gym/flex room; basement entertainment space (1 run to a Flex is the lean, since most AV goes in the rack); outside backyard camera; outside front camera (current Driveway Nest spot); outside side-of-house gate and walkway camera.

## Plan v12 (draft, if the Enterprise 48 is bought; 2026-11-15)

Drafted on Aaron's go-ahead to rebuild around a USW Enterprise 48 PoE (48× 2.5 GbE PoE+, 4× SFP+) that replaces the Pro Max 16, the Aggregation and the Basement Flex. Nothing is bought or returned yet; v6 below stays the plan until then. Rack layout v16 goes with it (see [[Rebuild Big Boi into a new case with an HDD pool for bulk media]]). Same-day iterations v7–v11 are in git history. v11 (Aaron) made all networking red and grouped it at the right end of panel B, moved security back to A1–A8, and turned the Kitchen 3 run into the main-floor Presence Pro; v12 starts the rack gear at B1 and makes UPS and PDU management red, since they're UniFi networking gear.

Cord colours (Aaron, v12): orange security, red UniFi networking (APs, downstream switches, UPS and PDU management, WAN), green other hardware inside the rack, blue everything else. DACs are whatever colour they ship in.

Rules (networking practice): panel, switch, panel. Panel A (U30) sits over the switch's top row and panel B (U28) under its bottom row, position n over/under column n, so every patch cord is 6". Port numbers assume the UniFi odd-top / even-bottom convention (A n = port 2n−1, B n = port 2n), unconfirmed until the switch is in hand; a correction changes only the port labels. Groups are by function with a spare at the end. The UDM only routes: WAN in, one 10G DAC from the switch's bottom-right SFP+ cage to UDM SFP+ 11, LAN 1–8 unused. Rack gear enters panel B from the rear. Switch SFP+ cages (numbering unconfirmed): Big Boi DAC up through pass-through A22, second server via A23, Mac Studio via A24 (SFP+ RJ45 module, Cat6a through a coupler). Switch ports behind A22–A24 and B23–B24 stay free.

| Panel A (top row) | Run / device | Panel B (bottom row) | Run / device |
| --- | --- | --- | --- |
| A1–A7 | Security: cam front, cam backyard, cam side gate, doorbell, siren, chime, Ring keypad | B1–B5 | Rack gear (green): Hue, Lutron, HDHomeRun, Sonos Amp, Denon |
| A8 | Spare (security) | B6 | Spare (rack) |
| A9–A14 | Endpoints: wall Pi, Kitchen Sonos 1–2, basement guest, gym, office spare (dark) | B7–B12 | Free |
| A15–A16 | Spare (endpoints) | B13–B14 | UPS, PDU Pro mgmt (red) |
| A17–A18 | Presence Pro: main floor (the old Kitchen 3 run), basement (to pull); 2nd floor's is on the Upstairs Flex | B15–B17 | APs: Front, Back, Basement |
| A19 | Spare (sensor) | B18 | Spare (AP) |
| A20–A21 | Free for new house runs | B19–B21 | Switches: Upstairs Flex (own 210 W adapter), desk Flex 2.5G 5, Living TV Flex |
| A22–A24 | Server links over the SFP+ cages: Big Boi, second server, Mac Studio | B22 | Spare (switch) |
| | | B23–B24 | WAN1 CenturyLink → UDM 9, WAN2 Ting ONT → UDM SFP+ 10 |

## Plan: port map (v6, 2026-11-15; current until the Enterprise 48 is bought)

Working copy for collaborating on placement: the Claude artifact [30U rack — patch panels and layout](https://claude.ai/artifact/4y1iZZLXsEYS9URxmAcKwp) (2026-11-15); changes agreed there get copied back here. Diagram: the "Patch panels — front view" section at the bottom of ![30U rack layout](<../attachments/Rack - 30U floor rack proposed layout.svg>).

Rules: each panel position sits over the switch port with the same number, and devices are grouped by function so cord colours run in blocks and UniFi port profiles can cover a range. Each switch gets the gear that uses what it's good at: the Basement Flex (8× 2.5 GbE PoE, 196 W, own adapter; off battery in the 30U until the PDU Pro arrives, since the 4 UPS battery outlets go to Big Boi, UDM, Pro Max and Aggregation) is the 2.5 GbE PoE switch, taking the APs and the desk Flex through its mount keystones F1–F4 (F5–F8 spare for future APs or 2.5G PoE gear), with a 10G SFP+ uplink to the Aggregation. The Pro Max takes the 1 GbE gear through panel A (U30): security A1–A7, everything else A8–A12, infra A13–A15 on its 2.5 GbE PoE++ ports (Living TV Flex, basement entertainment Flex, and the Upstairs Flex, which runs off PM 15's PoE), A16 a spare 2.5G port. A17–A20 hold dark runs (Kitchen 3, office spares 1–3) with no switch port; A21–A24 are free. Panel B (U28) holds rack gear and WAN: B15–B24 sit directly above the UDM Pro's ports and patch down to them (B15–B22 = UDM LAN 1–8, so LAN port = position − 14: infra B15–B19, AV B20–B21, spare B22; B23 = WAN 9; B24 = SFP+ WAN, port 10), B9–B14 are rear-port gear and DAC pass-throughs (keystone pass-through plates) to the Aggregation, B1–B8 are free for future house runs. Security gear goes on the Pro Max (on the UPS). The Aggregation's 8 SFP+ cages are identical (any cage can take any link), so they're picked to keep the DACs from crossing: top row left to right Big Boi (via B9), second server (B10), Mac Studio (B11), Pro Max; bottom row Basement Flex at the far left, UDM SFP+ LAN (port 11) at the far right straight below it, middle two spare.

Cord colours (Aaron, 2026-11-15): orange security, red WAN, black infrastructure (switch uplinks, hubs, UPS, PDU, DACs), white APs, blue everything else.

### Panel A

| Pos | Run / device | Switch port | Cord | Status |
| --- | --- | --- | --- | --- |
| A1 | Cam front (G5 Turret) | PM 1 | orange | to pull |
| A2 | Cam backyard (G5 Turret) | PM 2 | orange | to pull |
| A3 | Cam side gate (G5 Bullet) | PM 3 | orange | to pull |
| A4 | Doorbell G6 Entry | PM 4 | orange | to pull |
| A5 | Siren (hallway) | PM 5 | orange | to pull |
| A6 | Chime (hallway) | PM 6 | orange | to pull |
| A7 | Ring keypad PoE | PM 7 | orange | in place |
| A8 | Living wall Pi | PM 8 | blue | in place |
| A9 | Kitchen Sonos 1 | PM 9 | blue | in place |
| A10 | Kitchen Sonos 2 | PM 10 | blue | in place |
| A11 | Basement guest room | PM 11 | blue | to pull |
| A12 | Basement gym / flex room | PM 12 | blue | to pull |
| A13 | Living TV → USW Flex | PM 13 · 2.5G | black | in place |
| A14 | Basement entertainment → Flex (PoE) | PM 14 · 2.5G | black | to pull |
| A15 | 2nd fl → Upstairs Flex (PoE-powered) | PM 15 · 2.5G | black | in place |
| A16 | Spare | PM 16 · 2.5G | — | spare |
| A17 | Kitchen 3 | — | blue | dark |
| A18 | Office spare 1 | — | blue | dark |
| A19 | Office spare 2 | — | blue | dark |
| A20 | Office spare 3 | — | blue | dark |
| A21–A24 | Future house runs | — | — | spare |

### Flex mount keystones (U25)

The Basement Flex's 1U mount has its own keystone holes beside the switch (Aaron 2026-11-15). Since v6 they carry the 2.5 GbE PoE gear and patch sideways to the switch with 1–1.5 ft cords.

| Pos | Run / device | Switch port | Cord | Status |
| --- | --- | --- | --- | --- |
| F1 | Office → U7-Pro-Wall-Front | Flex 1 | white | in place |
| F2 | Bar → U7-Pro-Wall-Back | Flex 2 | white | in place |
| F3 | Basement AP (U7 Pro) | Flex 3 | white | run in, AP not yet |
| F4 | Office → desk Flex 2.5G 5 | Flex 4 | black | in place |
| F5–F8 | Spare (future APs, 2.5G PoE gear) | Flex 5–8 | — | spare |

### Panel B

| Pos | Run / device | Switch port | Cord | Status |
| --- | --- | --- | --- | --- |
| B1–B8 | Future house runs | — | — | spare |
| B9 | Big Boi 10G DAC | Agg top row (pass-through) | black | rack gear |
| B10 | Second server | Agg top row (DAC or RJ45 mod) | blue | not bought |
| B11 | Mac Studio (future) | Agg top row (RJ45 mod) | blue | not bought |
| B12 | Pass-through | Agg | — | spare |
| B13 | Pass-through | Agg | — | spare |
| B14 | Pass-through | Agg | — | spare |
| B15 | PDU Pro mgmt | UDM 1 | black | not bought |
| B16 | Hue Bridge | UDM 2 | black | rack gear |
| B17 | Lutron hub | UDM 3 | black | rack gear |
| B18 | HDHomeRun | UDM 4 | black | rack gear |
| B19 | UPS 2U | UDM 5 | black | rack gear |
| B20 | Sonos Amp (U11) | UDM 6 | blue | rack gear |
| B21 | Denon AVR (U3) | UDM 7 | blue | rack gear |
| B22 | Spare | UDM 8 | — | spare |
| B23 | WAN1 CenturyLink | UDM 9 | red | in place |
| B24 | WAN2 Ting ONT | UDM SFP+ port 10 (RJ45 mod) | red | not bought |

## Artifacts (2026-11-15)

- Doc artifact (editable from any VM session via the Claude Docs connector): [30U rack — patch panels and layout](https://claude.ai/artifact/4y1iZZLXsEYS9URxmAcKwp).
- HTML page [30U floor rack, draft v15](https://claude.ai/artifact/WGjYYkQUgNJvS256sGvmDG): republished 2026-11-15 from `attachments/Rack - 30U rack layout page.html` with patch panel map v4 and the physical patching view (same link). Republishing needs a session that has the `Artifact` tool (not every VM session gets it); edit the vault file first, then publish it to that URL.
- The diagram source of truth is `attachments/Rack - 30U floor rack proposed layout.svg`.
- Physical patching view (2026-11-15): ![Top of rack patching](<../attachments/Rack - 30U top of rack patching front view.svg>), U30–U24 with every cord drawn; also on the HTML page. Generated by [unifi/rack-patching.py](https://github.com/aaronspriggs/spriggs-homelab/blob/main/unifi/rack-patching.py), which hard-codes the map; the panel front view and port map in the rack SVG and on the page come from [unifi/rack-panels.py](https://github.com/aaronspriggs/spriggs-homelab/blob/main/unifi/rack-panels.py), which rewrites both files. Both scripts hold the map, so regenerate it and re-splice the page (between the `patching:start`/`patching:end` markers, which sit between the panel front view and port map figures) when the map changes. Under v6 it shows panels A and B both taking 6-inch cords (lean of 2.2 in or less) and F1–F8 spanning 9–11 in sideways to the Flex's ports.

## Open questions

- **Pro Max 16 → Pro Max 24 PoE? (raised 2026-11-15)** The 16-port Pro Max is the root of the layout squeeze: panel A has 24 positions but only 16 switch ports behind it, the twelve 1 GbE PoE+ ports can't hold all 14 1 GbE runs, and the APs went to the Basement Flex, which is off battery until the PDU Pro arrives. UI lists the [USW Pro Max 24 PoE](https://techspecs.ui.com/unifi/switching/usw-pro-max-24-poe) as 16× 1 GbE (8 PoE+, 8 PoE++) + 8× 2.5 GbE PoE++, 2× SFP+, 400 W, 1U, versus the [Pro Max 16 PoE](https://techspecs.ui.com/unifi/switching/usw-pro-max-16-poe)'s 12× 1 GbE PoE+ + 4× 2.5 GbE PoE++, 180 W. It would match panel A port for port and put the APs back on a battery-backed switch. Aaron decides. Also considered (2026-11-15): the [USW Enterprise 48 PoE (Vintage)](https://techspecs.ui.com/unifi/switching/usw-enterprise-48-poe) at $799 on the UI store (Aaron's screenshot): 48× 2.5 GbE PoE+ (32 W/port, no PoE++), 4× SFP+, 720 W, L3, 150 W draw without PoE, 400 mm deep. It would replace the Pro Max, the Basement Flex and the Aggregation, and the current APs are PoE+ (U7 Pro 21 W, U7 Pro Wall 22 W max per UI), but on PoE+ input the Upstairs Flex's budget drops from 46 W to 16 W (UI spec), the idle draw adds about 110 W to the UPS, and it is 400 mm deep against the 30U's 18" (457 mm, Aaron 2026-11-15), so the rear power cord needs the remaining clearance. Aaron's variant (2026-11-15): return the Aggregation, buy the Enterprise 48, move the Basement Flex 2.5G 8 PoE to his desk on PoE, keep the desk Flex 2.5G 5 for the basement entertainment space, and move the 210 W adapter to the Upstairs Flex (which then leaves the UPS). Its 4 SFP+ would all be used (UDM, Big Boi, second server, Mac Studio). Cost (Aaron 2026-11-15): Enterprise 48 $851 with shipping and tax; Aggregation return $297 before tax; Aaron would also sell the Pro Max 16 with its rack mount and adapter, and the Basement Flex with its 210 W adapter, keeping the desk Flex 2.5G 5 at the desk. UI US list prices: Pro Max 16 PoE $399, Pro Max 16 rack mount $49, Flex 2.5G 8 PoE $199, 210 W adapter $79. Estimated net: roughly break-even to $150 out of pocket depending on resale. Noise: UI publishes no acoustic figure and no measured review was found (2026-11-15); owner reports say it is quiet at light load and loud when the fans ramp. Without the 210 W adapter the Upstairs Flex runs on PoE+ from the Enterprise 48 with a 16 W budget (U7 Pro max 21 W). UniFi gear that needs PoE++ per UI spec pages: E7 and U7 Pro XGS APs, the Access/Door/Gate hubs, and the Alarm Hub.
- Which switch goes in the basement entertainment space (1 GbE Flex keeps A14; a Flex 2.5G 5 moves it to F5).
- Interim AP battery gap: buy the PDU Pro before the move, put one AP on A16, or accept it.

## Decisions

- **2026-11-14 (Aaron):** Panel A is a UniFi 24-port keystone panel; all labels get redone. Cameras can land on the Pro Max (on UPS); the Basement Flex is acceptable once it's on battery.
- **2026-11-15 (Aaron):** basement entertainment space gets 1 run feeding a PoE-powered switch, since most AV gear goes in the rack.
- **2026-11-15 (Aaron):** cord colours as above. The hallway "doorbell speaker" run is for an indoor chime. In-rack gear (Lutron, Hue, HDHomeRun and so on) also patches through the keystone panels, and keystone pass-through plates (arrived) carry 10G DACs where needed.
- **2026-11-15 (Aaron):** the Basement Flex 2.5G 8 PoE runs on the official UniFi adapter, so all 8 ports give 2.5 GbE with PoE; use it more. The basement ceiling AP is a U7 Pro on 2.5 GbE PoE like the other three (Ubiquiti lists the U7 Pro as PoE+, 21 W max: [techspecs](https://techspecs.ui.com/unifi/wifi/u7-pro)), so it goes on Flex 1.

- **2026-11-15 (Aaron):** the Basement Flex mount's keystones take the basement drops (F1–F8), patched sideways.
- **2026-11-15:** the existing "30U rack layout" artifact is not a doc type, so this VM session can't read or edit it; the doc artifact above is the working copy.
- **2026-11-15 (Aaron): map v12.** Rack gear starts at B1; UPS and PDU management turn red (UniFi networking gear), so red runs B13–B24 and B7–B12 are free.
- **2026-11-15 (Aaron): map v11.** All networking red (APs, downstream switches, WAN), grouped at the right end of panel B: APs B15–B18 beside UPS/PDU management, switches B19–B22, WAN B23–B24. Security back to A1–A8. The Kitchen 3 run becomes the main-floor Presence Pro, grouped with the basement sensor at A17–A19.
- **2026-11-15 (Aaron): map v10 and new cord colours.** Orange security, red Wi-Fi and WAN, green in-rack hardware, blue everything else; replaces the earlier scheme (black infrastructure, white APs). APs to B19–B22 next to WAN, server links to A22–A24 over the switch's SFP+ cages, UPS and PDU management beside the APs. Confirmed: the 2nd-floor Presence Pro goes on the Upstairs Flex; the PDU Pro plugs into the 4th UPS battery outlet, so everything on it (hub shelf, second server, Sonos Amp) is on battery and no battery outlet is spare.
- **2026-11-15 (Aaron): map v9.** Office runs cut from 5 to 3 (desk Flex, Front AP, one spare); the other two office cables come out for pulls elsewhere (destinations not set). Planned: a hardwired Presence Pro sensor on each floor; the main-floor and basement ones home-run to panel A, the 2nd-floor one is assumed to plug into the Upstairs Flex like the other upstairs runs. Security moves to panel B (bottom row) so panel A has room: each group now fills one 8-column switch block with a spare.
- **2026-11-15 (Aaron): map v8.** Every house run on panel A (switch top row) and every rack connection on panel B (bottom row); one AP spare, not two. Answers: keep the 210 W adapter and move it to the Upstairs Flex (its switch port then carries data only; upstairs Wi-Fi is off the UPS); the 4th UPS battery outlet stays spare; the PDU Pro is ordered and will be in the rack on day one; the 30U's 18" is front-to-back rail-to-rail depth, so the 400 mm switch fits with its power cord just past the rear rail; no basement entertainment switch (the basement won't be finished for years), so that run leaves the map.
- **2026-11-15 (Aaron): map v7 and rack v16 drafted.** Aaron chose to refactor around the Enterprise 48 (2.5 GbE on every port for Ting's 2 Gbps), return the Aggregation, sell the Pro Max 16 and the Basement Flex, keep the desk Flex 2.5G 5, give the hub shelf 2U and move the rest of the rack up; asked for networking best practice and room for expansion. Pending the purchase.
- **2026-11-15 (Aaron): map v6.** The Basement Flex's 2.5 GbE PoE ports and 196 W budget were going to basement desk drops while the APs sat on the Pro Max; it becomes the 2.5 GbE PoE switch instead (APs, desk Flex; F5–F8 spare), and 1 GbE runs go to the Pro Max, including the basement guest, gym and entertainment runs. The Upstairs Flex stays on a Pro Max PoE++ port because it is powered from it (15.5 W, which caps its own budget at 46 W); the Basement Flex's ports report the same PoE++ capability as the Pro Max's 2.5G ports, so it could likely power it, but keeping it on the Pro Max keeps second-floor Wi-Fi on battery while the Basement Flex is off battery (until the PDU Pro arrives). Kitchen 3 joins the dark runs on A17–A20 since it has no device. Open: if the basement entertainment switch turns out to be 2.5 GbE (a Flex 2.5G 5), it moves from A14 to F5.
- **2026-11-15 (Aaron): map v5.** Since everything moves from the 12U to the 30U anyway, keeping live cables on their current ports no longer matters; regroup both panels by function so cord colours run in blocks (Aaron flagged the wall Pi sitting among the security runs). Pro Max ports that change: Ring keypad 4 → 7, wall Pi 6 → 8, Sonos 8/9 → 9/10, Living TV Flex 10 → 12, Upstairs Flex 15 → 14, Front AP 14 → 15; UDM: UPS 8 → 5. Each port's UniFi settings move with its cable.
- **2026-11-15 (Aaron):** the USW Aggregation is bought. Its 8 SFP+ cages are on the right of the front panel, 4 on top and 4 below (the drawings showed one row; port numbering within the 2×4 block not yet checked).
- **2026-11-15 (Aaron): map v4.** The physical drawing showed v3's B1–B10 sitting at the left of panel B while the UDM Pro's LAN, WAN and SFP+ ports are at the far right (8–12 in sideways cords). Aaron approved moving the UDM positions to B15–B24 above those ports, pass-throughs to B9–B14 and free slots to B1–B8; each device keeps its UDM port. Port positions came from the 2026-11-12 12U photo; UI's quick start guide gives UDM port 9 = RJ45 WAN, 10 = SFP+ WAN, 11 = SFP+ LAN. UI's front-panel image (from Aaron, 2026-11-15) shows the 2×4 LAN block numbered odd on top (1, 3, 5, 7) and even below (2, 4, 6, 8), WAN 9 alone to its right, and SFP+ 10 stacked above 11 at the far right; the drawing follows it.
- **2026-11-15 (Aaron), open questions answered:** (1) Pro Max port 4 is the Ring keypad's PoE converter: Aaron believes so; not verified, so A4 stays as mapped. (2) The CenturyLink ONT is outdoors; its run comes into the rack as a house run, ends on a keystone and is patched to UDM WAN (port 9), so B9 stands. (3) UPS runtime: live HA reading 2026-11-15 is 110 W with 4,040 s (67 min) left at 100% battery. Assumed new PoE load: G6 Entry 16 W, 3 cameras at up to 12 W each, basement U7 Pro up to 21 W (the Basement Flex is already on a battery outlet), siren plus chime about 10 W, plus about 10% PoE loss: about 90 W, so about 200 W total. Scaling the 123 Wh the UPS implies today gives roughly 35 min, well past the 300 s TrueNAS shutdown. These are assumed maximums, not measurements; the HDD-pool rebuild of Big Boi (separate project) adds load this doesn't include.
