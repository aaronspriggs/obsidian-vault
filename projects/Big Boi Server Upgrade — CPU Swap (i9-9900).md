---
type: project
status: done
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
completed: 2026-03-04
notion_id: 30a7ae76-22ba-817a-834e-d7fe5db07098
---

## Outcome

Done 2026-03-04: swapped the i5-9400 for the already-owned i9-9900 on the existing ASRock Z390M-ITX/ac board. Confirmed live 2026-09-28 via the TrueNAS API (16 threads; the Plex VM gets all 16). Nothing else was bought. Full hardware list: [TrueNAS SCALE (Big Boi)](<../systems/TrueNAS SCALE (Big Boi).md>) → Config → Hardware.

## Decisions (2026-03-04)

- **No new case** (Sliger CX2130 cancelled): Big Boi is already in a rack-mounted MyElectronics 2U Mini-ITX case.
- **No new board** (ASUS TUF Z390M-Pro Gaming mATX cancelled): the extra PCIe slots were for a GPU, HBA and NIC. The 10 GbE NIC was already installed, the HBA isn't needed because bulk storage goes to a network UNAS Pro ("Rack Storage Expansion" project), and the GPU was dropped. ASRock Rack E3C246D4U2-2T was ruled out (Xeon-only).
- **No discrete GPU for now:** the i9-9900 keeps the UHD 630, which handles Plex transcoding via passthrough. AV1 encode and local LLMs were only forward-looking; the workstation's RTX 3080 Ti covers experiments. If either becomes real, go straight to a 16 GB+ low-profile card that does both (Intel Arc Pro B50, 16 GB, 70 W, was the pick) rather than a media-only Arc A310/A380 LP. Only Arc/Battlemage or RTX 40+ encode AV1, and there's no affordable low-profile RTX 40.

## Links

Pre-collapse research (GPU pricing, A380 LP availability, PCIe notes): KB export commit 4ac914e, branch `kb-export`.
