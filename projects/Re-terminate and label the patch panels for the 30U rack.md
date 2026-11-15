---
type: project
status: active
priority: medium
system:
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
- '[[UniFi (UDM Pro)]]'
parent: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
next_step: '2026-11-15: map v5 agreed; during the 30U move Aaron re-terminates, colours and labels to v5 (6-inch cords for panels A and B, 1–1.5 ft for F1–F8), then Claude moves each re-patched port''s UniFi settings (name, VLAN, PoE) to its new port, after checking HA automations for port-specific PoE entities.'
---

## Goal

Every house run lands on a labelled patch panel position in the 30U rack (layout v15), with one ID used on the panel, both cable ends and the UniFi port name, so nothing needs tracing.

## Status (2026-11-15)

Aaron listed every run in the house, existing and planned (inventory below). Port map v5 agreed (panel B over the UDM since v4; both panels grouped by function since v5); nothing re-terminated yet. The 30U rack goes where the 12U is now, and every run has at least 6 ft of slack (Aaron 2026-11-14).

## Run inventory (Aaron, 2026-11-15)

Existing runs (14), all home-run to the basement utility room:

| Room | Runs | In use |
| --- | --- | --- |
| Aaron's office | 5 (4 on one wall, 1 on the other) | Single run feeds the USW Flex 2.5G 5 under the desk. Of the 4, one feeds the U7-Pro-Wall-Front AP; 3 dark (old desk position) |
| Living room | 2 | TV area (PS5 now; will feed the spare USW Flex for PS5, Switch 2, Apple TV, maybe the Denon); wall-mounted Raspberry Pi panel |
| Kitchen | 3 (above cabinets) | 2 for the Sonos pair; 1 dark |
| Bar alcove | 1 | U7-Pro-Wall-Back AP |
| Front hallway | 1 | PoE converter for the Ring keypad |
| Basement | 1 | Future ceiling-mount AP (not installed) |
| 2nd floor | 1 | Upstairs utility room USW Flex 2.5G 8 PoE; all other 2nd-floor runs come off that switch |

Planned runs (8 or 9): front hallway UniFi Siren (PoE, near the doorbell); front hallway doorbell speaker or chime (maybe); outside entry G6 Entry doorbell (PoE+, 16 W, copper); basement guest room (desk or TV spot); basement gym/flex room; basement entertainment space (1 run to a Flex is the lean, since most AV goes in the rack); outside backyard camera; outside front camera (current Driveway Nest spot); outside side-of-house gate and walkway camera.

## Plan: port map (v5, 2026-11-15)

Working copy for collaborating on placement: the Claude artifact [30U rack — patch panels and layout](https://claude.ai/artifact/4y1iZZLXsEYS9URxmAcKwp) (2026-11-15); changes agreed there get copied back here. Diagram: the "Patch panels — front view" section at the bottom of ![30U rack layout](<../attachments/Rack - 30U floor rack proposed layout.svg>).

Rules: each panel position sits over the switch port with the same number, and devices are grouped by function so cord colours run in blocks and UniFi port profiles can cover a range. Panel A (U30) holds house runs. A1–A16 patch straight down to Pro Max ports 1–16 (6" cords): security A1–A7, everything else A8–A11, infra A12–A14, APs A15–A16 (ports 13–16 are the 2.5 GbE ones). That fills the Pro Max's twelve 1 GbE ports, so A17–A24 (free for future house runs) have no Pro Max port behind them: a new run goes to UDM LAN 8, Basement Flex 8 or a bigger switch; basement drops use the Flex mount keystones F1–F8 (below). Panel B (U28) holds rack gear and WAN: B15–B24 sit directly above the UDM Pro's ports and patch down to them (B15–B22 = UDM LAN 1–8, so LAN port = position − 14: infra B15–B19, AV B20–B21, spare B22; B23 = WAN 9; B24 = SFP+ WAN, port 10), B9–B14 are rear-port gear and DAC pass-throughs (keystone pass-through plates) to the Aggregation, B1–B8 are free for future house runs. Security and PoE-powered gear go on the Pro Max (on the UPS). The Basement Flex (every port 2.5 GbE PoE on its own adapter) takes the 2.5G-capable basement and spare drops; its uplink moves to SFP+ → Aggregation, freeing Pro Max port 12. The Aggregation's top row of SFP+ cages takes the uplinks (UDM SFP+ LAN port 11, Pro Max, Basement Flex), the bottom row the hosts (Big Boi via B9, second server and Mac Studio via B10–B11).

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
| A11 | Kitchen 3 | PM 11 | blue | dark |
| A12 | Living TV → USW Flex | PM 12 | black | in place |
| A13 | Office → desk Flex | PM 13 · 2.5G | black | in place |
| A14 | 2nd fl → Upstairs Flex | PM 14 · 2.5G | black | in place |
| A15 | Office → Front AP | PM 15 · 2.5G | white | in place |
| A16 | Bar → Back AP | PM 16 · 2.5G | white | in place |
| A17–A24 | Future house runs | — | — | spare |

### Flex mount keystones (U25)

The Basement Flex's 1U mount has its own keystone holes beside the switch (Aaron 2026-11-15), so basement drops land there and patch sideways with short cords instead of crossing the UDM and Aggregation from panel A.

| Pos | Run / device | Switch port | Cord | Status |
| --- | --- | --- | --- | --- |
| F1 | Basement AP (U7 Pro) | Flex 1 | white | run in, AP not yet |
| F2 | Bsmt ent. → Flex (PoE) | Flex 2 | black | to pull |
| F3 | Guest room | Flex 3 | blue | to pull |
| F4 | Gym / flex room | Flex 4 | blue | to pull |
| F5 | Office spare 1 | Flex 5 | blue | dark |
| F6 | Office spare 2 | Flex 6 | blue | dark |
| F7 | Office spare 3 | Flex 7 | blue | dark |
| F8 | Spare | Flex 8 | — | spare |

### Panel B

| Pos | Run / device | Switch port | Cord | Status |
| --- | --- | --- | --- | --- |
| B1–B8 | Future house runs | — | — | spare |
| B9 | Big Boi 10G DAC | Agg (pass-through) | black | rack gear |
| B10 | Second server | Agg (DAC or RJ45 mod) | blue | not bought |
| B11 | Mac Studio (future) | Agg (RJ45 mod) | blue | not bought |
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
- Physical patching view (2026-11-15): ![Top of rack patching](<../attachments/Rack - 30U top of rack patching front view.svg>), U30–U24 with every cord drawn; also on the HTML page. Generated by [unifi/rack-patching.py](https://github.com/aaronspriggs/spriggs-homelab/blob/main/unifi/rack-patching.py), which hard-codes the map, so regenerate it and re-splice the page (between the `patching:start`/`patching:end` markers, which sit between the panel front view and port map figures) when the map changes. Under v5 it shows panels A and B both taking 6-inch cords (lean of 2.2 in or less) and F1–F8 spanning 9–11 in sideways to the Flex's ports.

## Decisions

- **2026-11-14 (Aaron):** Panel A is a UniFi 24-port keystone panel; all labels get redone. Cameras can land on the Pro Max (on UPS); the Basement Flex is acceptable once it's on battery.
- **2026-11-15 (Aaron):** basement entertainment space gets 1 run feeding a PoE-powered switch, since most AV gear goes in the rack.
- **2026-11-15 (Aaron):** cord colours as above. The hallway "doorbell speaker" run is for an indoor chime. In-rack gear (Lutron, Hue, HDHomeRun and so on) also patches through the keystone panels, and keystone pass-through plates (arrived) carry 10G DACs where needed.
- **2026-11-15 (Aaron):** the Basement Flex 2.5G 8 PoE runs on the official UniFi adapter, so all 8 ports give 2.5 GbE with PoE; use it more. The basement ceiling AP is a U7 Pro on 2.5 GbE PoE like the other three (Ubiquiti lists the U7 Pro as PoE+, 21 W max: [techspecs](https://techspecs.ui.com/unifi/wifi/u7-pro)), so it goes on Flex 1.

- **2026-11-15 (Aaron):** the Basement Flex mount's keystones take the basement drops (F1–F8), patched sideways.
- **2026-11-15:** the existing "30U rack layout" artifact is not a doc type, so this VM session can't read or edit it; the doc artifact above is the working copy.
- **2026-11-15 (Aaron): map v5.** Since everything moves from the 12U to the 30U anyway, keeping live cables on their current ports no longer matters; regroup both panels by function so cord colours run in blocks (Aaron flagged the wall Pi sitting among the security runs). Pro Max ports that change: Ring keypad 4 → 7, wall Pi 6 → 8, Sonos 8/9 → 9/10, Living TV Flex 10 → 12, Upstairs Flex 15 → 14, Front AP 14 → 15; UDM: UPS 8 → 5. Each port's UniFi settings move with its cable.
- **2026-11-15 (Aaron):** the USW Aggregation is bought. Its 8 SFP+ cages are on the right of the front panel, 4 on top and 4 below (the drawings showed one row; port numbering within the 2×4 block not yet checked).
- **2026-11-15 (Aaron): map v4.** The physical drawing showed v3's B1–B10 sitting at the left of panel B while the UDM Pro's LAN, WAN and SFP+ ports are at the far right (8–12 in sideways cords). Aaron approved moving the UDM positions to B15–B24 above those ports, pass-throughs to B9–B14 and free slots to B1–B8; each device keeps its UDM port. Port positions came from the 2026-11-12 12U photo; UI's quick start guide gives UDM port 9 = RJ45 WAN, 10 = SFP+ WAN, 11 = SFP+ LAN, but not how the 2×4 LAN block is numbered.
- **2026-11-15 (Aaron), open questions answered:** (1) Pro Max port 4 is the Ring keypad's PoE converter: Aaron believes so; not verified, so A4 stays as mapped. (2) The CenturyLink ONT is outdoors; its run comes into the rack as a house run, ends on a keystone and is patched to UDM WAN (port 9), so B9 stands. (3) UPS runtime: live HA reading 2026-11-15 is 110 W with 4,040 s (67 min) left at 100% battery. Assumed new PoE load: G6 Entry 16 W, 3 cameras at up to 12 W each, basement U7 Pro up to 21 W (the Basement Flex is already on a battery outlet), siren plus chime about 10 W, plus about 10% PoE loss: about 90 W, so about 200 W total. Scaling the 123 Wh the UPS implies today gives roughly 35 min, well past the 300 s TrueNAS shutdown. These are assumed maximums, not measurements; the HDD-pool rebuild of Big Boi (separate project) adds load this doesn't include.
