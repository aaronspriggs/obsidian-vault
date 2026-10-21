---
date: 2026-03-05
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 31b7ae76-22ba-81c9-a303-fd74e8bd9cf5
---

# Backup strategy research and design session

Designed full backup strategy for current single-node setup and future two-node (Big Boi + UNAS Pro) architecture. Key decisions: (1) Three-layer strategy — ZFS snapshots on-pool, Backblaze B2 for offsite configs and irreplaceable content, UNAS Pro as local rsync target for Big Boi VM disks when purchased. (2) Servarr-managed content is re-downloadable and excluded from B2 to control cost. (3) Self-ripped content, home videos, and computer backups are irreplaceable and DO go to B2. (4) UNAS Pro directory structure must be planned before populating — separate paths for re-downloadable vs irreplaceable content required for selective backup. (5) UNAS Pro is a primary storage node, not a backup target for Big Boi — these are separate roles. Full strategy documented in the Plan backup strategy project page.
