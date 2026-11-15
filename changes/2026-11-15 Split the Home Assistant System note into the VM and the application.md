---
date: 2026-11-15
type: doc
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Assistant (integrations and automations)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/480c34085c1bb3681112500ea3482fc63e850a03
---

# Split the Home Assistant System note into the VM and the application

## What changed

Step 8, part 2 of the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>). Docs only; nothing in Home Assistant was changed.

[Home Assistant OS (VM)](<../systems/Home Assistant OS (VM).md>) was 1,720 words against the 1,500 limit. Aaron approved the line "machine against application" on 2026-11-15.

- **The machine stays in the old note** (1,027 words): the VM definition, HAOS, Supervisor and kernel, the six add-ons with Mosquitto and Scrypted, sizing, backups, console and shell access, and the decisions on the 2026-02-15 migration, the backup add-on and Scrypted as an add-on.
- **The application moved to a new note,** [Home Assistant (integrations and automations)](<../systems/Home Assistant (integrations and automations).md>) (1,392 words): the UI and its users, Claude's ha-mcp access, Nabu Casa, Core and the store, the integration inventory, climate, Alert2 alerting, the 26 automations, update approvals, and the decisions on Nabu Casa, phone approvals, Alert2, ecobee, the Face ID gate, the HomeKit bridge and the cameras.
- Both are on the Systems skeleton with `last_verified: 2026-11-15`, link to each other, and the new note has `runs_on` the VM. The `url` property moved to the new note, since it is the UI's.

**Relinked.** 38 projects and runbooks that are about the application now name the new note; three name both (home security plan, Scrypted, the off-box dead-man check). Nine stay with the VM: the four done backup and add-on tasks, the Mosquitto task and runbook, the restore runbook, the Google Drive backup runbook and the deprecated recovery runbook. The appliance-image VM runbook now names the VM as well as Big Boi. Done projects were relinked too, since nothing forbids it and it keeps a search by System right; the 91 change notes that name the VM were left, because change notes aren't edited afterwards. [Home Health](<../systems/Home Health (HA dashboard + alerts).md>) now has `runs_on` the new note. Links were fixed in Uptime Kuma, the Claude Code note, the wall panel (which had none), Home, the thermostat project and the repo's `ha/README.md`.

**Corrected against the live system** (ha-mcp, the TrueNAS API, UniFi and port checks from the ClaudeCode VM):

| Was in the note | Live on 2026-11-15 |
| --- | --- |
| HAOS 18.3, Core 2026.10.1, Supervisor 2026.09.3, kernel 6.18.52 | HAOS 18.4, Core 2026.11.0, Supervisor 2026.11.0, kernel 6.18.58 |
| HACS 2.0.5, 26 repositories | The built-in Marketplace, 27 repositories |
| 71 config entries (56 loaded, 3 retrying, 12 ignored) | 84 (63 loaded, 2 retrying, 18 ignored, 1 disabled); the Denon loads again |
| ha-mcp 9.0.0; Terminal & SSH 10.5.0; Matter Server 9.2.0 | 9.1.2; 10.6.0; 9.3.0 |
| Recorder 824 MiB, history since 2026-09-18; 11.3 GB disk used | 857 MiB, since 2026-10-30; 14.4 GB |
| Backups include no folders, about 430 MB | They include `ssl`; about 400 MB |
| Updates "held to 09:00 if it arrives overnight" | Held if they appear between 21:00 and 09:00 (Alert2's quiet hours start at 22:00) |
| Presets home, away, sleep | Also away_indefinitely |
| `camera.kitchen` broken | The entity is gone; the HomeKit "Kitchen" accessory entry remains |
| Mobile app on the iPhone | iPhone and iPad |
| Claude Code note: "the ha-mcp add-on" | It is a custom integration; there are six add-ons and none is ha-mcp |

Added because they were missing: the `claude` HA user, the automation list by group (weekly report, ack and snooze, maintenance mode, container restart and update-all, the two fix-run automations), the store's five leftover integrations, and the open Nest repair.

**Dropped, and why:**

- The climate dashboard cards (wall-panel bubble card, two mushroom cards): dashboard content, not checked today, and recorded in the done project [Migrate thermostats from Nest to ecobee](<../projects/Migrate thermostats from Nest to ecobee.md>).
- "Aaron installed 2026.9.4 by hand" and "tapping still also offers `/config/updates`": history of one update, kept in the done project "Verify first automatic update runs".
- The 2026-09-29 retry list with "covered by the HA tidy-up task": that task is done and the Denon loads.
- How Protect was added and its entity types in detail: trimmed to the entity count; the detail is in the [Protect research note](<../changes/2026-10-27 Researched UniFi Protect's Home Assistant integration for the alarm plan.md>).
- The mDNS check's wording (`Scrypted FE0A` and five accessories announcing `_hap._tcp`): trimmed to "worked on 2026-10-17"; HA now has six accessory entries.
- The UPS sentence about Big Boi not powering back on: it belongs to the [UPS project](<../projects/Rack Infrastructure — UPS + Power Management.md>), which has it; the VM note links there.
- "History of the Home Health build and the wall panel: Changes entries from 2026-02-15 onward": the Recent changes view does this.

**Not checkable today, kept with their dates:** the HA user list and MFA, backup retention (7 days local, 30 on Drive; read 2026-10-16), Protect's API-key-only mode, the Companion app setting, and Scrypted's mDNS.

## Why

The note was over the size rule and mixed two things that change at different rates: the VM changes a few times a year, the integrations, automations and alerting weekly. The same line already separates the ClaudeCode VM from Claude Code. Rejected: a separate "Homelab alerting" note (the alerting is one section, and its procedure already has a runbook), a reference runbook for the inventory (it is current state, and it would sit in "untested runbooks" for good), and a Scrypted System note now (one add-on; the project holds its state until it is done).

Also fixed: [Switch ha-mcp auth to Home Assistant sign-in (OAuth)](<../projects/Switch ha-mcp auth to Home Assistant sign-in (OAuth).md>) was blocked without a `next_step`; the upstream issue is still open.

## How

This vault commit, plus repo commit 480c340 (`ha/README.md` names both notes; nothing deployed, `make check` 40 of 40 ok).

## Verify / roll back

Verify: `~/obsidian-vault/.kb/check.py` reports 0 errors; `check.py --map "Home Assistant (integrations and automations)"` and `--map "Home Assistant OS (VM)"` list the projects and runbooks above. Found and left alone, for Aaron to decide: the description of `ha_updates_install_on_approval` still says "Face ID-gated"; the old note called the receiver a Denon AVR-S930H where the rack project says AVR-S970H; Spotify Connect and five store integrations look unused. Roll back: `git revert` this commit; the new note would then be deprecated, not deleted.
