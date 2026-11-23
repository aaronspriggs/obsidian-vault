---
type: project
status: active
priority: medium
system:
- '[[USW Enterprise 48 PoE]]'
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
- '[[UniFi (UDM Pro)]]'
parent: '[[Move the homelab into the 30U floor rack]]'
next_step: '2026-11-23: re-terminated and patched during the cutover (Aaron). Port numbering confirmed live: A n = port 2n-1, B n = port 2n. Next: Aaron answers the findings under Open questions; then Claude sets the UniFi port names (needs a UniFi write route or Aaron in the UI) and checks HA automations for port-specific PoE entities.'
---

## Goal

Every house run lands on a labelled patch panel position in the 30U rack ([layout v17](<Move the homelab into the 30U floor rack.md>)), with one ID used on the panel, both cable ends and the UniFi port name, so nothing needs tracing.

## Status (2026-11-15)

Map v12 is agreed and the USW Enterprise 48 PoE it is built around is ordered. Nothing is re-terminated yet. Aaron listed every run in the house, existing and planned (inventory below). Slimmed 2026-11-15: how the map got from v4 to v12 is in [the design change note](<../changes/2026-11-15 Designed the patch panel map for the 30U rack (v4 to v12, Enterprise 48).md>).

## Run inventory (Aaron, 2026-11-15)

Existing runs (14), all home-run to the basement utility room:

| Room | Runs | In use |
| --- | --- | --- |
| Aaron's office | 5 now (4 on one wall, 1 on the other); 3 stay (desk Flex, Front AP, one spare), two cables get re-pulled elsewhere | Single run feeds the USW Flex 2.5G 5 under the desk. Of the 4, one feeds the U7-Pro-Wall-Front AP; 3 dark (old desk position) |
| Living room | 2 | TV area (PS5 now; will feed the spare USW Flex for PS5, Switch 2, Apple TV, maybe the Denon); wall-mounted Raspberry Pi panel |
| Kitchen | 3 (above cabinets) | 2 for the Sonos pair; 1 dark, becoming the main-floor Presence Pro |
| Bar alcove | 1 | U7-Pro-Wall-Back AP |
| Front hallway | 1 | PoE converter for the Ring keypad |
| Basement | 1 | Future ceiling-mount AP, a U7 Pro (not installed) |
| 2nd floor | 1 | Upstairs utility room USW Flex 2.5G 8 PoE; all other 2nd-floor runs come off that switch |

Planned runs: front hallway UniFi Siren (PoE, near the doorbell); front hallway indoor chime (maybe); outside entry G6 Entry doorbell (PoE+, 16 W, copper); basement guest room (desk or TV spot); basement gym/flex room; a basement Presence Pro; outside backyard camera; outside front camera (current Driveway Nest spot); outside side-of-house gate and walkway camera.

## Plan v12 (agreed 2026-11-15)

Built around a USW Enterprise 48 PoE (48× 2.5 GbE PoE+, 4× SFP+) that replaces the Pro Max 16, the Aggregation and the Basement Flex.

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

### Drawings and pages

- The vault files hold map v12 and rack v17 (checked 2026-11-15): `attachments/Rack - 30U floor rack proposed layout.svg` (the diagram source of truth), `Rack - 30U rack layout page.html`, and the physical patching view ![Top of rack patching](<../attachments/Rack - 30U top of rack patching front view.svg>)
- Generators, which hard-code the map: [unifi/rack-panels.py](https://github.com/aaronspriggs/spriggs-homelab/blob/main/unifi/rack-panels.py) (panel front view and port map, in the SVG and the page), [unifi/rack-patching.py](https://github.com/aaronspriggs/spriggs-homelab/blob/main/unifi/rack-patching.py) (patching view; re-splice the page between its `patching:start`/`patching:end` markers) and [unifi/rack-docwidget.py](https://github.com/aaronspriggs/spriggs-homelab/blob/main/unifi/rack-docwidget.py) (the doc's widgets). When the map changes, change all three and regenerate.
- Doc artifact, the working copy, editable from any VM session through the Claude Docs connector: [30U rack — patch panels and layout](https://claude.ai/artifact/4y1iZZLXsEYS9URxmAcKwp), last redrawn to v12 / rack v16.
- HTML page [30U floor rack](https://claude.ai/artifact/WGjYYkQUgNJvS256sGvmDG), published from the vault's HTML file; the live page shows rack v17 and map v12 (read 2026-11-21). Republishing needs a session that has the `Artifact` tool: edit the vault file first, then publish it to that URL.

## Decisions

- **2026-11-14 (Aaron):** panel A is a UniFi 24-port keystone panel and every label gets redone. The 30U rack goes where the 12U is now, and every run has at least 6 ft of slack. Cameras were to land on a UPS-backed switch (then the Pro Max 16); under v12 they are on the Enterprise 48, which is on battery.
- **2026-11-15 (Aaron): regroup by function, not by where a cable sits today.** Everything moves to the 30U anyway, so keeping live cables on their current ports no longer matters, and grouping lets cord colours run in blocks (he flagged the wall Pi sitting among the security runs).
- **2026-11-15 (Aaron): rebuild around a USW Enterprise 48 PoE,** for 2.5 GbE on every port (Ting's 2 Gbps), following networking best practice with room for expansion. It replaces the earlier maps, which spread runs over the Pro Max 16, the Basement Flex (as the 2.5 GbE PoE switch for the APs) and the UDM's LAN ports. The Aggregation goes back, the Pro Max 16 and the Basement Flex get sold ([sale project](<Sell the network gear retired by the 30U rack move.md>)), the desk Flex 2.5G 5 stays. Ordered the same day.
- **2026-11-15 (Aaron): in-rack gear patches through the keystone panels too** (Lutron, Hue, HDHomeRun and so on), and keystone pass-through plates (arrived) carry the 10G DACs. This reversed the 2026-11-14 draft, in which in-rack devices patched direct.
- **2026-11-15 (Aaron): cord colours** orange, red, green, blue as above, replacing the first scheme (black infrastructure, white APs). From v11 all networking is red and sits at the right end of panel B; from v12 UPS and PDU management are red too, since they are UniFi networking gear, and rack gear starts at B1.
- **2026-11-15 (Aaron): security on A1–A8.** v9 had moved it to panel B to make room on A; v11 moved it back.
- **2026-11-15 (Aaron): the Upstairs Flex gets the 210 W adapter** from the Basement Flex, so its switch port carries data only. Cost: upstairs Wi-Fi is off the UPS.
- **2026-11-15 (Aaron): office runs go from 5 to 3,** and the other two cables come out for pulls elsewhere (destinations not set).
- **2026-11-15 (Aaron): a hardwired Presence Pro on each floor.** Main floor on the old Kitchen 3 run and the basement one home-run to panel A; the 2nd floor's plugs into the Upstairs Flex.
- **2026-11-15 (Aaron): no basement entertainment run for now.** He first chose one run feeding a PoE-powered switch, since most AV gear goes in the rack; then dropped it because the basement won't be finished for years.
- **2026-11-15 (Aaron):** the hallway "doorbell speaker" run is for an indoor chime. The basement ceiling AP is a U7 Pro on 2.5 GbE PoE+ like the other three ([21 W max](https://techspecs.ui.com/unifi/wifi/u7-pro)).
- **2026-11-15 (Aaron): the CenturyLink ONT is outdoors;** its run comes in as a house run, ends on a keystone (B23) and is patched to UDM WAN port 9.
- **2026-11-15 (Aaron): v12 agreed,** after a review against practice: panel-switch-panel 1:1, the UDM only routing, function groups with spares, 33 of 48 positions used. Caveats he accepted: placement follows function and colour, not house-versus-rack, so the labels should say so; one switch is a single point of failure, and he will still sell the Pro Max 16, not keep it as a cold spare. The switch's heat at U29 is an open question in the rack project.
- **2026-11-15: UPS runtime with the new PoE load.** HA read 110 W and 67 min at 100% battery. Assumed new load (G6 Entry 16 W, 3 cameras at up to 12 W, basement U7 Pro up to 21 W, siren and chime about 10 W, 10% PoE loss) is about 90 W, so about 200 W and roughly 35 min, well past the 300 s TrueNAS shutdown. Assumed maximums, not measurements, and without the HDD pool's load.

## Open questions

- **Confirmed 2026-11-23 (Claude, UniFi API):** odd ports on the top row, even on the bottom, as the map assumed. The clients on each port matched v12: Hue, Lutron and HDHomeRun on 2, 4 and 6 (B1–B3), the wall Pi on 17 (A9), Kitchen Sonos 2 on 21 (A11), UPS and PDU Pro on 26 and 28 (B13–B14), the Front and Back APs on 30 and 32 (B15–B16), the Upstairs and desk Flexes on 38 and 40 (B19–B20). Big Boi's DAC is on SFP+ 2 (port 50) and the UDM's on SFP+ 4 (port 52, the switch's uplink to UDM SFP+ 11). Which physical cages those are isn't confirmed. If the cages follow the same odd-top, even-bottom rule as the copper ports (SFP+ 1 top left, 2 bottom left, 3 top right, 4 bottom right), the live state already matches the patching drawing (Big Boi bottom left, UDM bottom right); Aaron checks the labels on the bezel.
- Kitchen Sonos 1 is on port 33 (A17, the main-floor Presence Pro's position), and port 19 (A10) is empty: either the run or the patch cord is in the wrong place.
- The Upstairs Flex draws 17 W of PoE (Class 4) from port 38 (15.4 W on a second read the same day). v12 has it on its own 210 W adapter with the port carrying data only.
- Ring keypad, port 13 (A7): no link, 0.5 W of PoE (Class 3). It was the same on the Pro Max before the move (port 4: down, 0.63 W), so the move didn't cause it.
- Not on the switch yet: Sonos Amp (B4, port 8) and Denon (B5, port 10).
- Redraw the doc artifact to rack v17.
- **STP (Claude, 2026-11-23):** the Enterprise 48 runs at the default priority 32768, while the Upstairs Flex has 8192 (set earlier, value as in Sonos's UniFi guide) and the retired Pro Max 16 had 4096. So the core switch is no longer the lowest-priority bridge, and the edge switch upstairs is. The switches also report different root bridges. Fix: set the Enterprise 48 to 4096 in UniFi (Devices → the switch → Settings → STP priority), which makes it root as the Pro Max was. Claude has no UniFi write route. Upstairs Flex port 1 (Cheryl's Office Sonos) is still `discarding`; the Sonos Wi-Fi fix from [the STP change note](<../changes/2026-11-19 Traced the Upstairs Flex STP port-block alert to Cheryl's Office Sonos.md>) is still pending.
