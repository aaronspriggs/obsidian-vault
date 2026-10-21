---
date: 2026-02-06
type: install
system:
- '[[Plex Media Server]]'
notion_id: 3087ae76-22ba-81c6-91a4-d03c54bc975e
---

# Plex VM initial build and configuration

Built Plex VM on TrueNAS SCALE. Configured br0 bridge for LAN access. Set up Intel iGPU passthrough (UHD 630). Mounted plex_content NFS share at /mnt/media. Configured 8GB tmpfs RAM disk at /transcode. Enabled unattended-upgrades with Plex origin. Set timezone to America/Denver. Enabled fstrim.timer.
