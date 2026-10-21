---
date: 2026-10-15
type: doc
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/a32b34c
notion_id: 3fa7ae76-22ba-813d-bfa1-e61637bf315f
---

# KB Standards: creating and deleting ZFS snapshots moved to Tier 2

Snapshot create/delete Tier 3 → Tier 2 (Aaron); rollbacks and snapshot task changes stay Tier 3; truenas-api allows zfs.snapshot.delete except scheduled auto-* snapshots.

## What changed

- [STANDARDS](<../STANDARDS.md>)** → Change authority:**
    - New Tier 2 bullet: creating and deleting ZFS snapshots. Scheduled `auto-*` snapshots aren't deleted by hand; they expire through their task's retention.
    - The Tier 3 line now reads "ZFS pool or dataset changes, snapshot task changes, snapshot rollbacks and VM disk operations".
- **`truenas-api`** (commit a32b34c, deployed, `make check` ok): `zfs.snapshot.delete` added to `WRITE_ALLOWED`. It takes one `<dataset>@<name>` and refuses `auto-*` names and anything without `@`. Rollback is still not allowlisted. Tested offline: an `auto-*` name, a bare dataset and `zfs.snapshot.rollback` were all refused before login.

## Why

Aaron, 2026-10-15: "for snapshots both create and erase should be tier 2". Rollbacks stay Tier 3 because they overwrite live data.

## Pending

TrueNAS still needs the `SNAPSHOT_DELETE` role on the Claude Maintenance privilege (Aaron, UI) before deletes work.
