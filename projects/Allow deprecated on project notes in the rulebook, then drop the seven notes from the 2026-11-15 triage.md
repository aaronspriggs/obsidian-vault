---
type: task
status: active
priority: low
system:
- '[[ClaudeCode (VM)]]'
next_step: '2026-11-15: waiting for Aaron''s yes to the rulebook change below (Tier 3; asked in the triage session). On yes: make the three edits, then deprecate the seven notes as listed, update the prune note''s next_step, and replace the "Still open" line in the triage note''s Status.'
---

Follow-up from the [setup review](<Review and tune the Claude Code setup on the ClaudeCode VM.md>) and the [first quarterly triage](<../changes/2026-11-15 Ran the first quarterly KB triage.md>).

## Goal

Make "drop" writable. The rulebook's Lifecycle section says any note is dropped with `status: deprecated` (plus `superseded_by` and one line saying why), and the triage note's step 1 relies on it, but the property table for `projects/` and `.kb/check.py` allow only active, blocked, backlog and done. No project note has ever been deprecated, so the gap went unnoticed until the triage tried.

## Plan

1. **Rulebook (Tier 3, Aaron's yes):** in the `STANDARDS.md` property table, the `projects/` row's `status` list becomes "active, blocked, backlog, done, deprecated".
2. **`.kb/check.py`:** add `deprecated` to the projects status set. `--session`, `--projects` and `--map` already list only active, blocked and backlog, so a deprecated project drops out of them without further change; confirm that with one run.
3. **`bases/Projects.base`:** the view filtered on `status != "done"` also excludes deprecated, so the views hide them as the rulebook says.
4. **Deprecate the seven** Aaron agreed to drop on 2026-11-15, each with one line saying why:

| Note | Why | `superseded_by` |
| --- | --- | --- |
| Check whether Cowork can read the spriggs-homelab repo | Moot since 2026-10-21: homelab work happens only on the ClaudeCode VM | none |
| Rack Storage Expansion — UniFi UNAS Pro + Bulk HDD Tier | Aaron chose the rebuild with an HDD pool on 2026-10-15 | Rebuild Big Boi into a new case with an HDD pool for bulk media |
| Evaluate GPU upgrade for AV1 encoding | The Arc A380 in Big Boi was chosen on 2026-11-09; encoding moves off the workstation | Automated AV1 re-encode pipeline for UHD Blu-ray rips on Big Boi |
| Review push rules after two weeks (which alerts get ignored or always acked) | Same data and same purpose as the monthly prune | Prune homelab alerts monthly from Alert2 fire counts |
| Evaluate centralized VM update management (Ansible or Cockpit) | `homelab-update` covers both Ubuntu VMs since 2026-09-26 and HAOS has update approvals; revisit only if the VM count grows | none |
| Evaluate Renovate for container image and dependency updates | Two stacks, and Dockhand's update entities with one-tap "Update all" already do it | none |
| SSL certificate expiry monitoring | Only two Kuma monitors are HTTPS: Scrypted has expiry notification on and the TrueNAS certificate runs to 2035-03-15. Turn the flag on for any monitor that later gets a real certificate | none |

5. Add "and the ack and snooze taps in the Homelab Alerts logbook" to the next step of [Prune homelab alerts monthly from Alert2 fire counts](<Prune homelab alerts monthly from Alert2 fire counts.md>), which takes over the push-rule review.
6. Change note (type doc), and replace the "Still open" line in the triage note's Status.

## Decisions

- **2026-11-15: ask, don't work around.** Rejected: marking the seven `done` (they weren't done, and a later search for finished work would find them), changing `check.py` without the table it enforces, and editing the rulebook on the strength of "Yes to all", which answered a different question.
