---
type: project
status: active
priority: medium
system:
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
- '[[UniFi (UDM Pro)]]'
parent: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
next_step: '2026-11-15: Aaron and Claude adjust drop placement on the A/B diagram (draft v2); then Aaron re-terminates, colours and labels during the 30U move and sets matching UniFi port names.'
---

## Goal

Every house run lands on a labelled patch panel position in the 30U rack (layout v15), with one ID used on the panel, both cable ends and the UniFi port name, so nothing needs tracing.

## Status (2026-11-15)

Aaron listed every run in the house, existing and planned (inventory below). Draft port map written; nothing re-terminated yet. The 30U rack goes where the 12U is now, and every run has at least 6 ft of slack (Aaron 2026-11-14).

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

## Plan: port map (draft v3, 2026-11-15)

Working copy for collaborating on placement: the Claude artifact [30U rack — patch panels and layout](https://claude.ai/artifact/4y1iZZLXsEYS9URxmAcKwp) (2026-11-15); changes agreed there get copied back here. Diagram: the "Patch panels — front view" section at the bottom of ![30U rack layout](<../attachments/Rack - 30U floor rack proposed layout.svg>).

Rules: Panel A (U30) holds house runs. A1–A16 patch straight down to Pro Max ports 1–16 (6" cords); A17–A24 are free for future house runs; basement drops use the Flex mount keystones F1–F8 (below). Panel B (U28) holds rack gear and WAN: B1–B10 patch down to the UDM Pro (B1–B8 = UDM LAN 1–8, B9 = WAN1, B10 = SFP+1 WAN2), B11–B16 are rear-port gear and DAC pass-throughs (keystone pass-through plates) to the Aggregation, B17–B24 are free for future house runs. Security and PoE-powered gear go on the Pro Max (on the UPS). The Basement Flex (every port 2.5 GbE PoE on its own adapter) takes the 2.5G-capable basement and spare drops; its uplink moves to SFP+ → Aggregation, freeing Pro Max port 12. Live ports that already match (PM 4, 6, 8, 9, 13–16; UDM 2–4, 8, 9) don't move.

Cord colours (Aaron, 2026-11-15): orange security, red WAN, black infrastructure (switch uplinks, hubs, UPS, PDU, DACs), white APs, blue everything else.

### Panel A

| Pos | Run / device | Switch port | Cord | Status |
| --- | --- | --- | --- | --- |
| A1 | Cam front (G5 Turret) | PM 1 | orange | to pull |
| A2 | Cam backyard (G5 Turret) | PM 2 | orange | to pull |
| A3 | Cam side gate (G5 Bullet) | PM 3 | orange | to pull |
| A4 | Ring keypad PoE | PM 4 | orange | in place |
| A5 | Doorbell G6 Entry | PM 5 | orange | to pull |
| A6 | Living wall Pi | PM 6 | blue | in place |
| A7 | Siren (hallway) | PM 7 | orange | to pull |
| A8 | Kitchen Sonos 1 | PM 8 | blue | in place |
| A9 | Kitchen Sonos 2 | PM 9 | blue | in place |
| A10 | Living TV → USW Flex | PM 10 | black | in place |
| A11 | Chime (hallway) | PM 11 | orange | to pull |
| A12 | Kitchen 3 | PM 12 | blue | dark |
| A13 | Office → desk Flex | PM 13 · 2.5G | black | in place |
| A14 | Office → Front AP | PM 14 · 2.5G | white | in place |
| A15 | 2nd fl → Upstairs Flex | PM 15 · 2.5G | black | in place |
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
| B1 | Sonos Amp (U11) | UDM 1 | blue | rack gear |
| B2 | Hue Bridge | UDM 2 | black | rack gear |
| B3 | Lutron hub | UDM 3 | black | rack gear |
| B4 | HDHomeRun | UDM 4 | black | rack gear |
| B5 | Denon AVR (U3) | UDM 5 | blue | rack gear |
| B6 | PDU Pro mgmt | UDM 6 | black | not bought |
| B7 | Spare | UDM 7 | — | spare |
| B8 | UPS 2U | UDM 8 | black | rack gear |
| B9 | WAN1 CenturyLink | UDM 9 | red | in place |
| B10 | WAN2 Ting ONT | UDM SFP+1 (RJ45 mod) | red | not bought |
| B11 | Big Boi 10G DAC | Agg (pass-through) | black | rack gear |
| B12 | Second server | Agg (DAC or RJ45 mod) | blue | not bought |
| B13 | Mac Studio (future) | Agg (RJ45 mod) | blue | not bought |
| B14 | Pass-through | Agg | — | spare |
| B15 | Pass-through | Agg | — | spare |
| B16 | Pass-through | Agg | — | spare |

B17–B24: free for future house runs.

## Decisions

- **2026-11-14 (Aaron):** Panel A is a UniFi 24-port keystone panel; all labels get redone. Cameras can land on the Pro Max (on UPS); the Basement Flex is acceptable once it's on battery.
- **2026-11-15 (Aaron):** basement entertainment space gets 1 run feeding a PoE-powered switch, since most AV gear goes in the rack.
- **2026-11-15 (Aaron):** cord colours as above. The hallway "doorbell speaker" run is for an indoor chime. In-rack gear (Lutron, Hue, HDHomeRun and so on) also patches through the keystone panels, and keystone pass-through plates (arrived) carry 10G DACs where needed.
- **2026-11-15 (Aaron):** the Basement Flex 2.5G 8 PoE runs on the official UniFi adapter, so all 8 ports give 2.5 GbE with PoE; use it more. The basement ceiling AP is a U7 Pro on 2.5 GbE PoE like the other three (Ubiquiti lists the U7 Pro as PoE+, 21 W max: [techspecs](https://techspecs.ui.com/unifi/wifi/u7-pro)), so it goes on Flex 1.

- **2026-11-15 (Aaron):** the Basement Flex mount's keystones take the basement drops (F1–F8), patched sideways.
- **2026-11-15:** the existing "30U rack layout" artifact is not a doc type, so this VM session can't read or edit it; the doc artifact above is the working copy.

## Open questions

- Pro Max port 4 draws ~0.6 W with no link (2026-11-14): is that the Ring keypad's PoE converter? The map assumes yes.
- Does the CenturyLink WAN (UDM port 9) come in as a house run from the outdoor ONT? The map puts it on B9.
- UPS runtime: the new PoE load (doorbell 16 W, cameras ~12 W, AP, siren) all sits on the UPS through the Pro Max.
