---
date: 2026-10-15
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Decide backup for the Dockhand TrueNAS app upgrade, then upgrade it]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/4798143
notion_id: 3fa7ae76-22ba-816e-a8e7-ff3967a55ade
---

# Granted claude-maint snapshot creation (SNAPSHOT_WRITE + allowlist)

Aaron added SNAPSHOT_WRITE to the Claude Maintenance privilege; truenas-api WRITE_ALLOWED now includes zfs.snapshot.create only.

## What changed

- **TrueNAS (Aaron, UI):** the privilege "Claude Maintenance" gained the role `SNAPSHOT_WRITE`. A first attempt added `SNAPSHOT_READ` by mistake and was corrected. `SNAPSHOT_DELETE` was not granted.
- **ClaudeCode VM (Claude):** `truenas-api` `WRITE_ALLOWED` now includes `zfs.snapshot.create`. The docstring and `truenas/README.md` are updated. Commit 4798143, deployed to `~/.local/bin/truenas-api`, `make check` ok.

## Why

Aaron, 2026-10-15: so Claude can take its own pre-change snapshots, starting with the Dockhand upgrade. This is a security change (Tier 3), approved explicitly.

## How to verify / roll back

`truenas-api privilege.query` shows `SNAPSHOT_WRITE` on Claude Maintenance. The first use (`app_mounts@pre-dockhand-1.1.38`) succeeded, and the earlier attempt with only `SNAPSHOT_READ` was correctly refused (EACCES). To roll back, remove the role in Credentials → Groups → Privileges and revert the commit.
