---
date: 2026-09-28
type: doc
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
notion_id: 3e97ae76-22ba-814a-b0b9-d6befc502aab
---

# Added Backlog status to Projects; triaged stalled projects and closed two verified tasks

Projects Status gained Backlog; 7 stalled projects moved there per Aaron. NFS-restriction task closed (already restricted); update-verification task closed. /transcode task created.

**What:** Aaron's answers to the phase 3 decisions of [KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)](<../projects/KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager).md>).
- **Projects ****`Status`** gained **Backlog** (wanted, not in progress; not counted as stalled). Existing options kept their IDs. [STANDARDS](<../STANDARDS.md>) lifecycle updated.
- **Moved to Backlog:** Scrypted HomeKit bridge, BIGBOI dataset reorg, Seerr + Discord external requests, Test Plex DVR recording, Fix Yu Yu Hakusho organization, Verify/clean up plex_config, Design wall panel screensaver.
- **Closed Done:** "Restrict TrueNAS NFS exports to the Plex VM" (both exports already had `hosts = [192.168.1.116]`; the TrueNAS audit log shows no NFS changes in its 7-day window, so the 2026-09-26 finding had misread `networks` alone). "Verify first automatic update runs" (both VMs ran cleanly 2026-09-27; Aaron installed HA 2026.9.4 by hand because iOS action buttons can't send the approval).
- **New Task:** [Restore transcode tmpfs on the Plex VM](<../projects/Restore transcode tmpfs on the Plex VM.md>), approved by Aaron; he runs the commands.
