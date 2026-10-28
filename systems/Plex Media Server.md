---
status: active
category: vm
ip: 192.168.1.116
url: http://192.168.1.116:32400/web
runs_on:
- '[[TrueNAS SCALE (Big Boi)]]'
last_verified: 2026-10-20
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/plex-vm
notion_id: 3087ae76-22ba-819f-aef3-e5cbf40b98e5
---

Plex Media Server running as a VM on TrueNAS SCALE (Big Boi). Plex Pass active. EAE codec manually installed. Access: [http://192.168.1.116:32400/](http://192.168.1.116:32400/)

## Overview

Plex Media Server running as a VM on TrueNAS SCALE (Big Boi). Plex Pass lifetime active. Handles local and remote media playback including Live TV/DVR via HDHomeRun.

## Host

- **Hypervisor:** TrueNAS SCALE (Big Boi) — 192.168.1.248
- **VM IP:** 192.168.1.116
- **Management URL:** [http://192.168.1.116:32400/web](http://192.168.1.116:32400/web)
- **VM OS:** Ubuntu 24.04.5 LTS (noble), kernel 6.8.0-146-generic (as of 2026-10-16)
- **VM spec (TrueNAS, verified 2026-10-16):** 4 vCPU × 2 cores × 2 threads, Host Passthrough, UEFI, autostart; VirtIO NIC on `br0`, MAC `00:a0:98:31:ab:d0`; iGPU passed through as PCI `pci_0000_00_02_0`; zvol 32 GiB (root LV 14.5 GiB). Rebuild: runbook "Rebuild the Plex VM from scratch".
- **vRAM:** 12 GB
- **Disk:** zvol inside `Big Boi/vmstore` (confirmed by Aaron 2026-09-24; zvol **`Big Boi/vmstore/Plex-9wert`**, found via the TrueNAS API 2026-09-25). It's covered by the daily 00:00 recursive `vmstore` snapshot task.
- **Weekly updates:** enrolled in **homelab-update** (Sun 04:00 America/Denver): Ubuntu full-upgrade, Plex from [plex.tv](http://plex.tv/), reboot if needed, 7 checks, results pushed to HA. See the "homelab-update" runbook. On-demand updates still follow the "Updating the Plex VM (OS + Plex)" runbook.
- **Maintenance access:** Claude Code on the ClaudeCode VM connects as `claude` (`ssh plex`). Root access is limited to `/usr/local/sbin/claude-maint`. See the "Give ClaudeCode VM SSH access to the Plex VM" project. Since 2026-10-16 it also has `plex-db-export`, which copies Plex's newest own DB backup plus `Preferences.xml` to `/mnt/dvr/.plex-db-export/plex-db.tar.gz` (600) weekly for the B2 offsite backup.
- **Network:** Bridged via br0 on TrueNAS (LAN IP on 192.168.1.0/24)
- **SSH:** `ssh plexadmin@192.168.1.116`
- **SSH access:** Preferred over SPICE console for management
- **Timezone:** America/Denver

## Plex Media Server

- **Remote Access:** Enabled and fully working — validated over 5G cellular
- **Public mapping:** WAN IP:32400 (the WAN IP is dynamic; Plex re-detects it)
- **Port forward:** TCP 32400 → 192.168.1.116:32400 (configured on UDM Pro)
- **Remote access preference:** Bookmarked full URL (no DDNS or reverse proxy configured)
- **Version:** 1.43.4.10903-e5521bd8c (upgraded 2026-09-24 from 1.43.0.10492)
- **Repo:** [https://downloads.plex.tv/repo/deb](https://downloads.plex.tv/repo/deb) is still configured but **stale**: its newest build was 1.42.2 as of 2026-09-24. Upgrade Plex with `claude-maint upgrade-plex`, which installs the latest *public* .deb from [plex.tv](http://plex.tv/)'s official download API. See the "Updating the Plex VM (OS + Plex)" runbook.
- **Plex Pass:** Lifetime
- **Service:** plexmediaserver (systemd, active)

## Hardware Transcoding

- **GPU:** Intel CoffeeLake-S GT2 (UHD Graphics 630) — Gen9 iGPU
- **Passthrough:** /dev/dri exposed to VM (card0, card1, renderD128)
- **VA-API version:** 1.20
- **libva:** 2.12.0
- **Intel iHD driver:** 24.1.0
- **Verified:** intel_gpu_top confirms Plex Transcoder using Render/Video engines during active transcode
- **Plex user groups:** video, render

## Transcode RAM Disk

- **Mount point:** /transcode (tmpfs)
- **Size:** 8 GB (increased from 6 GB)
- **fstab:** `tmpfs /transcode tmpfs size=8G,mode=1777,nosuid,nodev,noexec 0 0`
- **Plex config:** Transcoder temporary directory set to /transcode
- **Note:** Large chunk files accumulate during long 4K→1080p sessions; 8 GB accepted as sufficient for most use cases
- **Verified 2026-09-28:** mounted (tmpfs 8.0G, rw,nosuid,nodev,noexec) and `TranscoderTempDirectory="/transcode"` in Preferences.xml. Restored by Aaron that day after the fstab entry was found missing on 2026-09-24.

## Media Storage (NFS)

- **NFS source:** TrueNAS dataset at /mnt/Big Boi/BIGBOI/plex_content
- **NFS export allowed:** 192.168.1.116 only (TrueNAS `hosts`; verified via the API 2026-09-28)
- **VM mount point:** /mnt/media
- **fstab:** Persistent entry with space escaped as 040 (Big040Boi)
- **Library structure (verified 2026-09-28):** `/mnt/media/Movies`, `/mnt/media/TV Shows`, plus `/mnt/media/downloads/usenet` (servarr's download area on the same dataset). DVR recordings in `/mnt/dvr`.
- **Mount type:** systemd automount (`x-systemd.automount` in fstab, with `_netdev`). Both `/mnt/media` (ro) and `/mnt/dvr` (rw) mount on first access. Verified 2026-09-24.

## Live TV / DVR

- **Tuner:** HDHomeRun Flex 4K (192.168.1.106)
- **Channels:** 114 OTA channels, zip 80602
- **Tuners:** 4
- **DVR recordings dataset:** `plex_recordings` on TrueNAS
- **DVR NFS mount:** `192.168.1.248:/mnt/Big Boi/BIGBOI/plex_recordings` → `/mnt/dvr` (RW, NFS v3)
- **Plex DVR library:** 'Recordings' (type: TV Shows, path: `/mnt/dvr`)
- **Important:** When scheduling a recording, always select the 'Recordings' library — NOT 'TV Shows'. The TV Shows library is read-only and Plex will silently fail to write there.
- **How DVR writes:** Two-stage — temp `.grab` subfolder first, then moves finished file into library path. Both stages require write access.

## Automatic Maintenance

- **unattended-upgrades:** 2.9.1+nmu4ubuntu1, enabled
- **Plex origin allowed:** o=Plex and site=[downloads.plex.tv](http://downloads.plex.tv/)
- **apt-daily timer:** 03:20 (RandomizedDelay disabled)
- **apt-daily-upgrade timer:** 03:30
- **fstrim.timer:** Enabled; fstrim -Av verified successful
- **Plex updates:** the apt repo is stale (newest build 1.42.2), so Plex updates come from `claude-maint upgrade-plex` (weekly via homelab-update, or on request). unattended-upgrades only installs Ubuntu *security* updates; regular `noble-updates` land through homelab-update's full-upgrade.

## Clients & Codec Strategy

- **Primary client:** Apple TV 4K (3rd generation, A15, no AV1 hardware decode). Apple TV 4K (4th generation, A19, dedicated AV1 hardware decoder per [Apple](https://www.apple.com/newsroom/2026/10/apple-unveils-the-new-apple-tv-4k/)) ordered by Aaron, arriving 2026-11-13; Plex app direct play of AV1 on it is untested.
- **Current encode codec:** H.265 (HEVC) 10-bit, encoded via HandBrake NVENC on workstation (RTX 3080 Ti)
- **Audio:** TrueHD 7.1 converted to E-AC3 5.1 with Atmos compatibility; TrueHD retained as secondary track
- **AV1:** Deferred until Plex AV1 direct play is confirmed on the 4th-gen Apple TV. Re-encoding from existing H.265 files is possible but introduces generational quality loss — keep source files where possible.
- **EasyAudioEncoder (EAE):** installed manually to stop 429 rate-limit errors when Plex tried to download it. Lives in `/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Codecs/EasyAudioEncoder-6a4213e165f8ac3d108a346e-linux-x86_64` (verified 2026-09-28). Redo if the VM is rebuilt.
- See Workstation (Desktop) system page for full HandBrake encoding workflow

## Open work

Backup policy for the VM and media is under "Plan backup strategy for TrueNAS and VMs". The Plex DB and `Preferences.xml` go to B2 weekly (runbook "Offsite backup to B2"); the media library has no offsite copy.
![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
