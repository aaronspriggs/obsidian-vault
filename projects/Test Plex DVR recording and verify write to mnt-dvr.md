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

**2026-11-15 (checked live during the quarterly triage):** `/mnt/dvr` on the Plex VM is the `plex_recordings` NFS share, mounted read-write, and holds one recording: `NHL Hockey (2008)/Season 2026/… Washington Capitals at Boston Bruins.ts`, 841 MB, dated 2026-03-07. So a DVR recording has landed there; whether to close this as done is with Aaron in the triage.
