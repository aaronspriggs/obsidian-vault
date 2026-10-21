---
type: task
status: done
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
completed: 2026-09-04
notion_id: 3d17ae76-22ba-81c3-a850-ea054c0a055e
---

Retired the community "Home Assistant Google Drive Backup" add-on in favor of HA Core's native google_drive backup integration, closing the gap where native automatic backups had no offsite destination while the add-on ran a redundant parallel schedule. Verified end-to-end (backup.create_automatic produced a backup with agent_ids including both hassio.local and google_drive.spriggs_aaron_gmail_com) before uninstalling the add-on. Full walkthrough, Google Cloud Console gotchas, and verification steps documented in the "Set up native Google Drive backup integration for Home Assistant" runbook and the matching Changes log entry (2026-09-04). Two follow-ups still open: confirm the encryption key emergency kit is stored somewhere durable off-instance, and identify a second unexplained "Home Assistant" entry under Google Account → Connected apps.
