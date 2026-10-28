---
type: project
status: backlog
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Workstation (Desktop)]]'
- '[[Plex Media Server]]'
parent: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
---

Rip UHD Blu-rays on the Workstation, re-encode to AV1 automatically on Big Boi. Waits on the Big Boi rebuild.

## Goal

Aaron rips 4K Blu-rays on the [Workstation (Desktop)](<../systems/Workstation (Desktop).md>) (it has the Blu-ray drive), copies the rips to Big Boi, and an automated job there re-encodes them to AV1 for Plex.

## Status (2026-10-28)

Idea stage. Hardware: an Intel Arc A310 in Big Boi for AV1 encoding (the 3080 Ti can't encode AV1). Not bought.

## Plan

1. Buy an Arc A310 (new, with a return window; about $140). The A380 ($169) adds graphics cores that help tone mapping and parallel Plex transcodes, not single AV1 encodes.
2. After the rebuild: the A310 stays with the TrueNAS host for containers (`/dev/dri`); the UHD 630 iGPU stays passed through to the Plex VM.
3. Pick the automation (see Open questions), deploy it through the repo and Dockhand.
4. Watch folder on the HDD pool → encode → output into the Plex library.

## Decisions

- **2026-10-28 (Aaron):** AV1 card is for re-encoding rips, not Plex streaming transcodes; ripping stays on the Workstation.

## Open questions

- **Dolby Vision vs hardware speed.** Per [HandBrake's HDR docs](https://handbrake.fr/docs/en/1.9.0/technical/hdr.html), every 10-bit encoder including Intel QuickSync keeps HDR10, but Dolby Vision and HDR10+ are kept only by the software encoders x265, SVT-AV1 and Apple VideoToolbox HEVC; QSV, NVENC and AMD VCN drop them. With SVT-AV1, Dolby Vision is written as profile 10. Hardware AV1 on the A310 = fast, HDR10 only; SVT-AV1 on the i9-9900 = keeps DV/HDR10+, much slower for 4K. Does Dolby Vision matter, and do Plex and the Apple TV play DV profile 10 in AV1 (unchecked)? Aaron (2026-10-28): DV is nice-to-have, not worth much extra money. No GPU fixes this in HandBrake (it's an encoder-software limit). On the A310 itself, rigaya's QSVEncC can hardware-encode AV1 and carry the DV RPU as profile 10 (`--dolby-vision-rpu`, `--dolby-vision-profile 10.x`, per its [version history](https://www.videohelp.com/software/QSVEnc/version-history)); dovi_tool itself doesn't handle AV1. That path is a CLI to script, not HandBrake. Plan: start with HandBrake QSV AV1 (HDR10); revisit QSVEncC if DV matters later.
- **Keep the remuxes?** Re-encoding is lossy; the Workstation note already says keep the highest-quality sources where possible. Keeping UHD remuxes sizes the HDD pool.
- **Automation tool** (all existing, no custom build): HandBrake in a container with a watch folder ([jlesage/handbrake](https://hub.docker.com/r/jlesage/handbrake): drop into /watch, output to /output; QSV support flagged with a caveat, issue #459) is the simplest. Tdarr does library-wide flows with QSV/NVENC/CPU switching ([community AV1 flow](https://redlib.hbubli.cc/r/Tdarr/comments/1fz0c77/unified_av1_qsvnvenccpu_flow)) but is heavier. HandBrake has encoded AV1 on Arc via QSV since 1.6.0 ([Tom's Hardware](https://www.tomshardware.com/news/handbrake-160-debuts-av1-transcoding-support-for-the-masses)).

## Changes

![[Changes.base#For this project]]
