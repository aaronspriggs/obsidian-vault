---
status: active
category: hardware
notion_id: 3087ae76-22ba-81ea-8062-cc3dfa26c023
---

Personal desktop. NVIDIA RTX 3080 Ti. Used for HandBrake media encoding for Plex library. H.265 10-bit NVENC workflow.

## Overview

Personal desktop workstation used for media encoding (HandBrake) to build the Plex library.

## Hardware

- **GPU:** NVIDIA GeForce RTX 3080 Ti
    - NVENC encoder block (H.264/H.265 hardware encode)
    - AV1 hardware encode NOT supported (requires RTX 40-series or newer)
- **OS:** Windows
- **Connection:** Hardwired to network (no static IP — not always powered on, DHCP address varies)
- Other specs: document CPU, RAM here

## Media Encoding Workflow

- **Tool:** HandBrake
- **Codec:** H.265 (HEVC) 10-bit NVENC
- **Encode speed:** ~160 FPS observed during active encodes
- **GPU utilization note:** Overall GPU % will appear low (~10%) during encoding. This is normal — check the **Video Encode engine specifically** in Task Manager. NVENC runs on a dedicated fixed-function block, not CUDA/3D cores. Video Encode graph at 100% = NVENC is saturated and working correctly.

## Codec Strategy

- **Current:** H.265 10-bit NVENC — best fit for this environment due to Apple TV compatibility
- **AV1:** Deferred for now. Apple TV 4K 3rd gen does support AV1 hardware decode, so the client side is ready. Main remaining question is Plex Direct Play support end-to-end. The bottleneck is GPU — RTX 3080 Ti does not support AV1 hardware encode (requires RTX 40-series+). Revisit when upgrading GPU.
- **Re-encoding existing library to AV1:** Not required to re-rip from source, but transcoding already-compressed files introduces generational quality loss. Keep highest quality source files where possible before any future migration.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
