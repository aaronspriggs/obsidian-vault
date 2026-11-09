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

## Status (2026-11-09)

Idea stage. Hardware: an Intel Arc A380 in Big Boi for AV1 encoding (the 3080 Ti can't encode AV1), decided 2026-11-09 after confirming the Designare's BIOS F9+ has Resizable BAR. Ordered 2026-11-09 from Newegg (about $200; A380 street price had risen from ~$169 on 2026-10-28 as stock runs out), ahead of the 2026-11-13 Apple TV AV1 check. Test passthrough, Plex AV1 decode + tone mapping and HandBrake QSV AV1 inside the return window.

## Plan

1. Buy an Arc A380 (new, with a return window; about $169 on 2026-10-28; the A310 has the same AV1 encoder but cost more then). Board prep: flash F11a, CSM off, Above 4G Decoding and Re-Size BAR on; verify a large BAR with `lspci -vv`.
2. After the rebuild: the A380 stays with the TrueNAS host for containers (`/dev/dri`); the UHD 630 iGPU stays passed through to the Plex VM.
3. Pick the automation (see Open questions), deploy it through the repo and Dockhand.
4. Watch folder on the HDD pool → encode → output into the Plex library.

## Decisions

- **2026-11-09 (Aaron):** card is the Arc A380; Nvidia/AMD dropped (see the Arc and non-Arc notes under Open questions).
- **2026-10-28 (Aaron):** AV1 card is for re-encoding rips, not Plex streaming transcodes; ripping stays on the Workstation.
- **2026-10-28 (Aaron):** don't keep the original rips. Consequence: whatever the encode drops (Dolby Vision, HDR10+, lossless audio if transcoded) is gone for good unless the disc is re-ripped; the pipeline must check the output before deleting the source.
- **2026-10-28 (Aaron):** keep Atmos: pass through the TrueHD Atmos track (HandBrake Auto Passthru, MKV output, HandBrake 1.3.2+).

## Open questions

- **Dolby Vision vs hardware speed.** Per [HandBrake's HDR docs](https://handbrake.fr/docs/en/1.9.0/technical/hdr.html), every 10-bit encoder including Intel QuickSync keeps HDR10, but Dolby Vision and HDR10+ are kept only by the software encoders x265, SVT-AV1 and Apple VideoToolbox HEVC; QSV, NVENC and AMD VCN drop them. With SVT-AV1, Dolby Vision is written as profile 10. Hardware AV1 on the A310 = fast, HDR10 only; SVT-AV1 on the i9-9900 = keeps DV/HDR10+, much slower for 4K. Does Dolby Vision matter, and do Plex and the Apple TV play DV profile 10 in AV1 (unchecked)? Aaron (2026-10-28): DV is nice-to-have, not worth much extra money. No GPU fixes this in HandBrake (it's an encoder-software limit). On the A310 itself, rigaya's QSVEncC can hardware-encode AV1 and carry the DV RPU as profile 10 (`--dolby-vision-rpu`, `--dolby-vision-profile 10.x`, per its [version history](https://www.videohelp.com/software/QSVEnc/version-history)); dovi_tool itself doesn't handle AV1. That path is a CLI to script, not HandBrake. Plan: start with HandBrake QSV AV1 (HDR10); revisit QSVEncC if DV matters later.
- **Arc on the Z390 Designare + i9-9900 (researched 2026-11-09).** The "Arc needs 10th gen" rule is Intel's validation list for Resizable BAR, not a hardware limit; Gigabyte, MSI, ASRock and EVGA added ReBAR to Z390 boards by BIOS ([TechPowerUp](https://www.techpowerup.com/forums/threads/gigabyte-z390-resizable-bar-now-supported.277578), [Wccftech](https://wccftech.com/msi-adds-resizable-bar-support-intel-300-series-motherboard-lineup-z390-h370-b360-h310/)). Confirmed by Aaron from Gigabyte's [Designare support page](https://www.gigabyte.com/Motherboard/Z390-DESIGNARE-rev-10/support) (2026-11-09): **F9** (2021-11-28) added the Resizable-BAR option, capsule BIOS and microcode SA-00295, and blocks rollback to anything older; F10 (2024-01-10) fixes LogoFAIL; **F11a** (2025-06-10, latest) fixes CVE-2025-7026/7027/7029. Check when the board arrives: BIOS version, then flash F11a, CSM off, Above 4G Decoding on, Re-Size BAR on; on TrueNAS, `lspci -vv` on the Arc should show a large BAR (not 256 MB). Without ReBAR, Arc media encode reportedly still works with more CPU load ([no-ReBAR A380 test](https://kovasky-github-io.pages.dev/blogs/intel_arc_no_rebar)); B-series needs it.
- **Non-Arc fallback (2026-11-09):** the cheapest AV1-encode cards are the RTX 4060 / RTX 5050 (about $300-420 street) and the RX 7600; AMD is a poor fit because HandBrake's VCN encoder on Linux needs AMD's proprietary AMF stack ([HandBrake VCN docs](https://handbrake.fr/docs/en/latest/technical/video-vcn.html)), and the official jlesage/handbrake image has no NVENC (a fork such as zocker160/handbrake-nvenc or Tdarr would be needed).
- **Arc Pro B50 with SR-IOV, to share one GPU between host containers and the Plex VM (researched 2026-11-09): not viable yet; A380 stays.** On TrueNAS 25.04 (kernel 6.12) B-series cards aren't supported on the host without out-of-tree xe modules ([forum](https://forums.truenas.com/t/intel-arc-b50-vf-xe-driver-on-truenas-25-10/58130), [forum](https://forums.truenas.com/t/intel-arc-pro-b50-16-gb-for-ollama-ai-on-truenas-feasible-or-not/51907)). TrueNAS 26 (beta, kernel 6.18, renamed 27 from 27-RC.1) has the Battlemage driver ([Phoronix](https://www.phoronix.com/news/TrueNAS-26-Beta)) and one user ran Tdarr QSV on a B50 in Docker; a B60 user on the beta needed newer GuC firmware and `pci=nocrs` ([forum](https://forums.truenas.com/t/intel-arc-b60-battlemage-issues-on-truenas-26-beta/66470)). No report of B50 VFs created on TrueNAS and attached to a VM. Intel's production SR-IOV is 2 VFs per card and needs Arc Pro driver 32.0.101.8306+ firmware ([Intel](https://www.intel.com/content/www/us/en/support/articles/000103382/graphics/intel-arc-pro-dedicated-graphics-family.html)); the VF guest driver needs kernel 6.17+ per community guides, while the Plex VM runs 6.8. Revisit once TrueNAS 27 is released and someone reports a VF in a VM.
- **Feasibility check of the VM plan (A380 passed to the Plex VM, jlesage/handbrake in Docker inside it), researched 2026-11-09.** Plex: Arc is not officially supported on Linux; staff (ChuckPa, 2025-11-12) say support waits on the FFmpeg 6.1 upgrade and then Intel compute-runtime and media-driver updates ([forum](https://forums.plex.tv/t/plex-to-support-battlemage-gpus/933451)). Users run A310/A380 with Plex's bundled drivers, including an Ubuntu 24.04 VM on Proxmox with tone mapping on PMS 1.41.3 (2024-12), but HDR tone mapping broke in 1.40.3 and 1.40.4 and a 4K HDR tone-mapping crash was reported in 2025-03 ([forum](https://forums.plex.tv/t/intel-arc-gpu-transcoding-discussion/881952), [forum](https://forums.plex.tv/t/intel-media-driver-update-for-plexserver-on-linux/904601)); AV1 decode on Arc is only indirectly reported (2024-04, [forum](https://forums.plex.tv/t/intel-arc-av1-hw-transcoding-on-linux/875363)). So homelab-update's weekly Plex upgrade needs a transcode check or a pin once the A380 is in. Passthrough: works on Proxmox/KVM with Ubuntu 24.04 (kernel 6.8); ReBAR inside the guest is reported both ways; no TrueNAS-specific success report found ([Proxmox](https://forum.proxmox.com/threads/pci-passthrough-arc-a380-into-vm.146964/), [Proxmox](https://forum.proxmox.com/threads/reduced-bar-on-8-1-with-intel-arc-a380.144193/)). jlesage/handbrake: README covers QSV for Intel iGPUs only; [issue #382](https://github.com/jlesage/docker-handbrake/issues/382) (Arc A310, QSV missing in the GUI while HandBrakeCLI sees it; host chmod on /dev/dri works around it) is open and unanswered since 2024-11. It has a `/config/hooks/post_conversion.sh` hook (args: status, output, source, preset); plan: `AUTOMATED_CONVERSION_KEEP_SOURCE=1` and the hook deletes the source only after its checks pass. Latest image v26.09.1 (HandBrake 1.11.2 on master). Plan: buy the A380 with a return window and test all three (passthrough + BAR, Plex AV1 decode + tone mapping, HandBrake QSV AV1) before the window closes.
- **Atmos playback path:** Apple has not announced TrueHD bitstream passthrough on Apple TV 4K; Atmos there arrives as Dolby Digital Plus (E-AC-3 JOC), and open-source encoders can't create E-AC-3 Atmos from TrueHD ([Zeera](https://zeerawireless.com/blogs/news/apple-tv-4k-2026-audio-passthrough-truehd-dts-plex), [HandBrake forum](https://forum.handbrake.fr/viewtopic.php?p=183145)). The TrueHD Atmos tracks are kept for any client that can bitstream them; check which device plays to the Atmos system.
- **Automation tool** (all existing, no custom build): HandBrake in a container with a watch folder ([jlesage/handbrake](https://hub.docker.com/r/jlesage/handbrake): drop into /watch, output to /output; QSV support flagged with a caveat, issue #459) is the simplest. Tdarr does library-wide flows with QSV/NVENC/CPU switching ([community AV1 flow](https://redlib.hbubli.cc/r/Tdarr/comments/1fz0c77/unified_av1_qsvnvenccpu_flow)) but is heavier. HandBrake has encoded AV1 on Arc via QSV since 1.6.0 ([Tom's Hardware](https://www.tomshardware.com/news/handbrake-160-debuts-av1-transcoding-support-for-the-masses)).

## Changes

![[Changes.base#For this project]]
