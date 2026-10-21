---
date: 2026-03-05
type: config
system:
- '[[Plex Media Server]]'
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 31b7ae76-22ba-81be-9931-f0a1cdecbb5f
---

# Finalized Plex DVR recording storage — /mnt/dvr mounted RW, Plex library created

Completed full Plex DVR recording storage setup:
- Fixed ownership on plex_recordings dataset: chown 1000:1000, chmod 770
- NFS export for plex_recordings was already configured on TrueNAS (RW, 192.168.1.0/24)
- Created /mnt/dvr mount point on Plex VM
- Found existing fstab entry for plex_recordings → /mnt/dvr (RW, NFS v3, x-systemd.automount) — already correct
- Ran mount -a and systemctl daemon-reload, confirmed RW mount working
- Created DVR Recordings library in Plex pointed at /mnt/dvr
