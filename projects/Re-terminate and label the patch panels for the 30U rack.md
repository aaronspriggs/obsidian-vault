---
type: project
status: active
priority: medium
system:
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
- '[[UniFi (UDM Pro)]]'
parent: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
next_step: '2026-11-15: Aaron reviews the draft port map below (A1–A24) and answers the open questions; then Claude finalises it and Aaron re-terminates and labels during the 30U move.'
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

## Plan: draft port map

Rules: Panel A (U30) mirrors the Pro Max 16 below it, so A1–A16 patch straight down to ports 1–16 with 6" cords; A17–A24 mirror the Basement Flex 2.5G 8 PoE ports 1–8. Panel B (U28) is left for future runs. In-rack devices patch direct, never through a panel. The Pro Max is on the UPS, so everything security-related and every PoE-powered switch or AP lands there; non-PoE drops go to the Basement Flex. Ports 13–16 are the Pro Max's 2.5 GbE ports.

| Pos | Run | Switch port | Cord | Notes |
| --- | --- | --- | --- | --- |
| A1 | Outside front camera (G5 Turret Ultra) | Pro Max 1 | yellow | CCA ok |
| A2 | Outside backyard camera (G5 Turret Ultra) | Pro Max 2 | yellow | CCA ok |
| A3 | Outside side gate/walkway camera (G5 Bullet) | Pro Max 3 | yellow | Narrow FOV suits the walkway |
| A4 | Outside entry doorbell (G6 Entry) | Pro Max 4 | yellow | PoE+, copper run |
| A5 | Hallway UniFi Siren | Pro Max 5 | yellow | |
| A6 | Living wall Pi panel | Pro Max 6 | blue | Already on port 6 |
| A7 | Hallway Ring keypad PoE converter | Pro Max 7 | yellow | |
| A8 | Hallway doorbell speaker/chime (if pulled) | Pro Max 8 | yellow | |
| A9 | Living TV → spare USW Flex | Pro Max 9 | blue | USW Flex is PoE-powered |
| A10 | Basement entertainment → Flex | Pro Max 10 | blue | PoE lets a Flex there run without an adapter |
| A11 | Basement ceiling AP | Pro Max 11 | white | 1 GbE until a 2.5G port frees up |
| A12 | Spare | Pro Max 12 | | Basement Flex uplink moves to its SFP+ port → Aggregation |
| A13 | Office single run → desk Flex 2.5G 5 | Pro Max 13 | blue | 2.5 GbE, already port 13 |
| A14 | Office → U7-Pro-Wall-Front | Pro Max 14 | white | 2.5 GbE, already port 14 |
| A15 | 2nd floor → upstairs Flex 2.5G 8 PoE | Pro Max 15 | black | 2.5 GbE, PoE-powered, already port 15 |
| A16 | Bar → U7-Pro-Wall-Back | Pro Max 16 | white | 2.5 GbE, already port 16 |
| A17 | Kitchen Sonos 1 | Basement Flex 1 | blue | Moves off the Pro Max (no PoE, no UPS need) |
| A18 | Kitchen Sonos 2 | Basement Flex 2 | blue | |
| A19 | Kitchen 3 | Basement Flex 3 | blue | Dark |
| A20 | Basement guest room | Basement Flex 4 | blue | |
| A21 | Basement gym/flex room | Basement Flex 5 | blue | |
| A22 | Office spare 1 | Basement Flex 6 | blue | Dark |
| A23 | Office spare 2 | Basement Flex 7 | blue | Dark |
| A24 | Office spare 3 | Basement Flex 8 | blue | Dark |

Cord colors: blue room and wall drops, white APs, yellow cameras and security, red WAN/ISP (UDM WAN ports, Ting ONT), black infrastructure (uplinks, in-rack devices). Label every run with its position ID (A01–A24, B01–B24) on the panel, on a wrap label behind the keystone, at the far end, and as the UniFi port name (Aaron sets those; Claude's UniFi account is read-only).

## Decisions

- **2026-11-14 (Aaron):** Panel A is a UniFi 24-port keystone panel; all labels get redone. Cameras can land on the Pro Max (on UPS); the Basement Flex is acceptable once it's on battery.
- **2026-11-15 (Aaron):** basement entertainment space leans to 1 run feeding a small switch, since most AV gear goes in the rack.

## Open questions

- Is the "doorbell speaker" an indoor chime (e.g. Ubiquiti's PoE chime)? Pull the run either way while walls are open.
- The 4th 2.5 GbE need (basement AP) has no 2.5G port: fine on 1 GbE for now; once Big Boi moves to the Aggregation, a Pro Max SFP+ frees up for a 10GBASE-T module if needed.
- UPS runtime: the new PoE load (doorbell 16 W, cameras ~12 W, AP, siren) all sits on the UPS through the Pro Max.
