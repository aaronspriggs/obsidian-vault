---
type: task
status: done
priority: high
system:
- '[[Home Assistant OS (VM)]]'
completed: 2026-09-29
notion_id: 3ea7ae76-22ba-818f-a87f-fe2a69cb33a6
---

Confirmed by Aaron 2026-09-29: the HA backup emergency kit (encryption key) has been in 1Password since 2026-09-04, when the Google Drive backup migration was done. Nothing else to do.

## Goal

The HA backup encryption key (emergency kit) is stored off the HA instance, in 1Password, so the offsite Google Drive backups are actually restorable.

## Status

2026-09-29: open. Only Aaron can check 1Password; Claude never sees the key.

## Plan

1. Look in 1Password for an item holding the HA backup key.
2. If it's missing: HA → Settings → System → Backups → ⋮ → Encryption key → download the emergency kit, and store it (or its key) as a 1Password item.
3. Tell Claude the item name so the HA OS page's Access section can reference it; then mark Done.
