---
date: 2026-11-15
type: doc
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/5354d0c910fee5d2a64cc43e88c79ed85bca3b19
---

# Split the Big Boi System note into the box and its storage

## What changed

Step 8, part 2 of the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>). Docs only; nothing on TrueNAS was changed.

[TrueNAS SCALE (Big Boi)](<../systems/TrueNAS SCALE (Big Boi).md>) was 1,689 words against the 1,500 limit. Aaron approved the line "box against storage" on 2026-11-15.

- **The box stays in the old note** (1,289 words): hardware, network, the TrueNAS install, services, certificate, open alerts, the UI and SSH logins, both of Claude's API users with the API gotchas, how VMs are created, the guests table, and the decisions on the removed apps, the CPU swap, the rebuild and native VMs.
- **Storage moved to a new note,** [Big Boi storage (pool, datasets, shares, backups)](<../systems/Big Boi storage (pool, datasets, shares, backups).md>) (1,170 words): the pool and its scrub, the datasets and zvols table, NFS and SMB shares, ACLs, snapshot tasks and the manual snapshots still held, the two B2 Cloud Sync tasks, the stacks cron, S.M.A.R.T. tests and the pool-name path quirks, with the decisions on `ix-apps`, the NFS host restriction, B2 and the media left out of snapshots.
- Both are on the Systems skeleton with `last_verified: 2026-11-15`, link to each other, and the new note has `runs_on` Big Boi.

**Relinked.** Eleven projects and runbooks now name the storage note: the backup strategy, the dataset reorganization, the `plex_config` cleanup, the snapshot deletion, the UNAS Pro idea, four done storage tasks, the B2 runbook and the Plex NFS runbook. Four name both: the rebuild project, the done Dockhand-upgrade backup task, the bare-metal rebuild runbook and the disaster recovery index. Eighteen stay with the box. The 50 change notes that name Big Boi were left, because change notes aren't edited afterwards. Links to the storage note were added in the Home Assistant OS VM, ClaudeCode VM, Plex and Dockhand notes, in Home, in two projects' body links, and in the repo's `truenas/README.md` and `backup/README.md`.

**Corrected against the live system** (TrueNAS API, UniFi, port checks):

| Was in the note | Live on 2026-11-15 |
| --- | --- |
| Last scrub 2026-09-20 | 2026-10-25, 0 errors; the weekly task with its 35-day threshold is now recorded |
| 2.3 TB used, 13.5 TB available | 2.44 TB used, 13.40 TB available |
| `vmstore` 187 GB; zvols 44, 77 and 62 GB | 320 GB; 52, 188 and 73 GB. Snapshots are most of it: 148 GB on the Plex VM's 32 GiB disk |
| The stacks cron's rsync command | Stale since 2026-10-23: the live job also has `--delete-excluded` and excludes `logs/` and `Definitions/`. The note now links the repo README, which matches |
| "S.M.A.R.T. tests configured 2026-03-07" | SHORT weekly on Sunday 00:00, LONG monthly on the 1st at 01:00, all disks |
| `claude-maint` key, no expiry mentioned | Expires 2027-10-14 |
| Dockhand 1.1.38 "(2026-10-16)" | Still 1.1.38, with an app update available |
| Home: "graceful shutdown isn't configured yet" | Live since 2026-09-29, untested end to end |

Added because they were missing: UIDs and the group behind the read-only user, that Big Boi sits on the Pro Max 16's "SFP+ 2" at 10 Gb (from UniFi), the alerts open today, the manual snapshots still held, and the API's login rate limit (about 25 `truenas-api` calls in a row give `[EBUSY] Rate Limit Exceeded`).

**Dropped, and why:**

- What each B2 task uploads and what the pre-script stages: the [B2 runbook](<../runbooks/Offsite backup to B2 - what's covered and how to restore.md>) has it, and it is the one that gets used in a restore.
- The cron command's text: source belongs in the repo, and the copy here had gone stale.
- The Dockhand app's leftover `/stacks` bind mount: moved to the [Dockhand](<../systems/Dockhand.md>) note, where it belongs.
- The 2026-03-04 line about a future 16 GB low-profile GPU: replaced by the 2026-11-09 Arc A380 decision in the rebuild project.
- "Was `America/Los_Angeles`" and "the expired `truenas_default` certificate was deleted 2026-09-26": history, in the done timezone task and the 2026-09-26 change note.
- "Write test (`alert.dismiss`) returns EACCES": a test result from 2026-09-25, in that day's change note and in the API runbook.
- `vmstore`'s ACL mode "Discard": not re-read today; the ACL type (POSIX) is.
- The Related list of six runbooks: the Runbooks view shows them; the three not otherwise linked are kept in the text.

**Not checkable through the API, kept with their sources:** the board, case, PSU, NIC and RAM kit models, the `apps` group's ACL entries, and the directory names inside `BIGBOI`.

## Why

The note was over the size rule, and the open work divides the same way: the backup strategy, the dataset reorganization and the HDD pool land on storage, while the box's own facts rarely change. Rejected: hardware against TrueNAS (the software half would still hold storage and stay over the limit), hypervisor against NAS (the guests table is small and every guest has its own note), and three notes (two more Systems to verify for no gain).

## How

This vault commit, plus repo commit 5354d0c (`truenas/README.md` and `backup/README.md` name the notes; nothing deployed, `make check` 40 of 40 ok).

## Verify / roll back

Verify: `~/obsidian-vault/.kb/check.py` reports 0 errors; `check.py --map "Big Boi storage (pool, datasets, shares, backups)"` and `--map "TrueNAS SCALE (Big Boi)"` list the projects and runbooks above. Found and left alone, for Aaron to decide: the manual snapshot `pre-dockhand-update-2026-09-26` on `ix-apps` is still held alongside `pre-dockhand-1.1.38`, and the Plex VM's disk snapshots take 148 GB. Roll back: `git revert` this commit; the new note would then be deprecated, not deleted.
