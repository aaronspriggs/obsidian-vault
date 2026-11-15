---
date: 2026-11-15
type: doc
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Allow deprecated on project notes in the rulebook, then drop the seven notes from the 2026-11-15 triage]]'
- '[[Quarterly KB triage with Aaron (Deferred items and Ideas)]]'
---

# Allowed deprecated on project notes and dropped seven backlog notes

## What changed

A rulebook change, approved by Aaron on 2026-11-15 (Tier 3): "Yes to that and finish it."

- `STANDARDS.md`, property table, `projects/` row: the `status` list is now "active, blocked, backlog, done, deprecated". Nothing else in the rulebook changed.
- `.kb/check.py`: the same value added to the projects status set.
- `bases/Projects.base`: the "Open for this system" view filters on `status != "done" && status != "deprecated"`, so System notes stop listing dropped projects.

With that in place, the seven notes Aaron agreed to drop at the [first quarterly triage](<2026-11-15 Ran the first quarterly KB triage.md>) are `status: deprecated`, each opening with a dated line saying why:

| Note | `superseded_by` |
| --- | --- |
| [Check whether Cowork can read the spriggs-homelab repo](<../projects/Check whether Cowork can read the spriggs-homelab repo.md>) | none |
| [Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier](<../projects/Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier.md>) | the Big Boi rebuild |
| [Evaluate GPU upgrade for AV1 encoding](<../projects/Evaluate GPU upgrade for AV1 encoding.md>) | the AV1 re-encode pipeline |
| [Review push rules after two weeks](<../projects/Review push rules after two weeks (which alerts get ignored or always acked).md>) | the monthly alert prune, whose next step now includes the ack and snooze taps |
| [Evaluate centralized VM update management](<../projects/Evaluate centralized VM update management (Ansible or Cockpit).md>) | none |
| [Evaluate Renovate](<../projects/Evaluate Renovate for container image and dependency updates.md>) | none |
| [SSL certificate expiry monitoring](<../projects/SSL certificate expiry monitoring.md>) | none |

Also recorded from the same message: the Arc A380 has arrived (Aaron: "early this week"), in the AV1 pipeline's next step and the rebuild's parts table. The date its return window closes is still not recorded.

## Why

The rulebook's Lifecycle section says any note is dropped by setting `status: deprecated`, and the quarterly triage depends on it, but the property table and the checker allowed only four statuses for project notes, so the commit hook refused the first drop ever attempted. The table was the part that was wrong: `superseded_by` was already an optional property on project notes, which only makes sense for a deprecated one.

Rejected: marking dropped notes `done` (a search for finished work would find things that were never done), a separate `dropped` status (a second word for what the rulebook already calls deprecated), and changing the checker without the table it enforces.

## How

This vault commit. No repo change and nothing deployed.

## Verify / roll back

Verify: `.kb/check.py` reports 0 errors; `--projects` and the session block no longer list the seven (they list only active, blocked and backlog), and the backlog count is 29. Roll back: `git revert` this commit, which puts the seven back in the backlog.
