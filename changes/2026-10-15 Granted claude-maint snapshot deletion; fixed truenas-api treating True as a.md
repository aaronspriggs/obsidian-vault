---
date: 2026-10-15
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/3c5fa62
notion_id: 3fa7ae76-22ba-8180-be99-f160aa87399b
---

# Granted claude-maint snapshot deletion; fixed truenas-api treating True as a job id

SNAPSHOT_DELETE added by Aaron; delete verified with a throwaway snapshot; truenas-api no longer polls job id 1 when a method returns True.

## What changed

- **TrueNAS (Aaron):** the Claude Maintenance privilege gained `SNAPSHOT_DELETE`. Its roles are now READONLY_ADMIN, APPS_WRITE, POOL_SCRUB_WRITE, SNAPSHOT_DELETE, SNAPSHOT_WRITE, SYSTEM_UPDATE_WRITE and VM_WRITE.
- **`truenas-api`**** fix** (commit 3c5fa62, deployed, `make check` ok): `zfs.snapshot.delete` returns `True`, and Python treats bool as an int, so `--write` mistook it for job id 1 and polled until the one-hour timeout. Now only real integers are treated as job ids.

## Why

This completes the Tier 2 snapshot change in KB Standards (see the 2026-10-15 Doc entry and commit a32b34c).

## Verify

On 2026-10-15, `app_mounts@claude-delete-test` was created and deleted twice. The first time hung on the bug and was stopped; the second ran with the fix and returned at once. A `zfs.snapshot.query` afterwards finds no test snapshot, and the three `pre-dockhand-1.1.38` snapshots are untouched.
