---
type: task
status: backlog
priority: medium
system:
- '[[Plex Media Server]]'
notion_id: 31b7ae76-22ba-81a2-8ff5-f94dc0bcb1db
---

# Test Plex DVR recording and verify write to /mnt/dvr

DVR storage setup is complete — plex_recordings NFS mounted RW at /mnt/dvr on Plex VM, library created in Plex. Schedule a test recording via Plex Live TV and confirm the .ts file lands in /mnt/dvr on the VM.
