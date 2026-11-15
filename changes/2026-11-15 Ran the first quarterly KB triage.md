---
date: 2026-11-15
type: doc
system:
- '[[ClaudeCode (VM)]]'
- '[[Claude Code (Remote Control service)]]'
- '[[Home Assistant (integrations and automations)]]'
- '[[Home Assistant OS (VM)]]'
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
- '[[Raspberry Pi Wall Panel]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
- '[[Quarterly KB triage with Aaron (Deferred items and Ideas)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/ed0283987fe71650e199f4b5b9020036a658bc70
---

# Ran the first quarterly KB triage

## What changed

Step 8, part 3 of the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>), following [the triage note](<../projects/Quarterly KB triage with Aaron (Deferred items and Ideas).md>). Claude read all 42 backlog notes, the three memory files, CLAUDE.md's dated rules and the two split change notes, checked what could be checked live, and put every decision to Aaron in one message. He answered "Yes to all" (2026-11-15).

**Backlog, 42 notes.**

- Done: [Test Plex DVR recording](<../projects/Test Plex DVR recording and verify write to mnt-dvr.md>) (a recording from 2026-03-07 is on the share), [Delete the pre-dockhand-1.1.38 snapshot](<../projects/Delete the pre-dockhand-1.1.38 snapshot after a quiet week.md>) and [Weekend-aware morning wake](<../projects/Weekend-aware morning wake for the wall panel.md>), the last two done in this run.
- Made active, each with a dated `next_step`: the Dockhand API token rotation and the TrueNAS read-only key rotation (one sitting, by 2026-12-20), the Nest thermostats (already under way), the kb-export token (half done, below), and the AV1 pipeline (the A380's tests are tied to its return window; Aaron still owes the arrival and window dates).
- Kept: 27, of which these were updated: Seerr and Discord (priority medium to low), the BIGBOI dataset reorganization (`parent` is now the rebuild; a Status paragraph says which parts are stale), the workstation specs task (trimmed to the workstation, the Apple TV half is answered), `plex_config`, Yu Yu Hakusho and the HDHomeRun outage test (today's live findings), and the three Claude Code mod notes (version and bundling).
- **Dropped: seven approved, not yet applied.** Cowork repo access, the UNAS Pro expansion, the workstation GPU upgrade, the two-week push-rule review, centralized VM update management, Renovate, and certificate expiry monitoring. The triage note says a dropped note gets `status: deprecated`, but the rulebook's property table and `check.py` only allow active, blocked, backlog and done on project notes, so the commit hook refuses it. Adding the value is a rulebook change (Tier 3) that Aaron wasn't asked about; it is with him now, and the seven stay in the backlog until he answers.

**Live changes Aaron approved.**

| What | Tier | How | Undo |
| --- | --- | --- | --- |
| Removed five store integrations with no config entry: Amplifi, Raspberry Pi GPIO, Raspberry Pi GPIO PWM, Stream Deck, Dyson Cloud | 3 | `ha_manage_hacs` remove | Download again from the Marketplace |
| Uninstalled the Spotify Connect add-on (`a0d7b954_spotify`, 0.19.0) | 3 | `ha_manage_app` uninstall | Reinstall from the community add-on repository; its options were name "Home Assistant", bitrate 320, initial volume 50, autoplay on, no access token |
| Deleted `~/.config/kb-export/notion-token` and `kb-export.json` on the ClaudeCode VM, and the empty directory | 3 | `rm` | Aaron creates a new token in Notion; nothing needs one |
| Deleted seven manual snapshots: `pre-dockhand-1.1.38` and `pre-dockhand-update-2026-09-26` on `ix-apps/app_mounts`, `app_mounts/dockhand` and `app_mounts/dockhand/data`, and `BIGBOI@pre-servarr-cleanup-2026-10-16` | 2 | `truenas-api --write zfs.snapshot.delete`, each returned true | None |
| `automation.wall_panel_morning_wake`: added a time condition, Monday to Friday, and a description | 2 | `ha_config_set_automation` | Before: trigger `time` at 07:00:00, no conditions, empty description, actions `light.turn_on` on `light.touchkio_hadashboard_display` and `number.set_value` 15 on `number.wall_panel_brightness`, mode single. Remove the condition to restore it |
| `automation.ha_updates_install_on_approval`: description no longer says "(Face ID-gated)" | 1 | `ha_config_set_automation` | Text only; the gate was removed on 2026-10-14 |

Checked before the removals: none of the five integrations had a config entry or a key in `configuration.yaml`, and the working Dyson integration (`dyson_local`, Office and Bedroom) has its own cloud module and doesn't import the removed Dyson Cloud one. Checked after: five add-ons installed and running, both Dyson entries loaded, no `pre-*` snapshot left. No Home Assistant restart was needed, since none of the removed integrations was loaded. No full backup was taken first: each removal has the inverse named above, and the Spotify Connect add-on held no credentials.

**Untested runbooks.** Aaron picked two to test before the next triage, tracked in [their own task](<../projects/Test the Home Assistant restore and ClaudeCode VM rebuild runbooks before the February 2027 triage.md>), which also records what happens to the other ten.

**Memory fold.** No memory file moved. Two are procedures too long for a line, and the Remote Control surfaces one isn't settled (its Artifact half changed today; its mod UI half waits on a re-test now that the VM is on 2.1.321). Every dated rule in CLAUDE.md still holds. Two lines changed in CLAUDE.md (repo commit ed02839, 1,879 to 1,927 words): the map-first examples now name the split System notes, and a new line under "How Aaron works" says to give the reason and what was rejected, check the work, and record each decision in the project note.

**What the split change notes left for Aaron.** The "Face ID-gated" wording: fixed. The Denon model: settled live, Home Assistant reports AVR-S970H and nothing in the vault says S930H. The unused add-on and integrations: removed. The older snapshot set: deleted. The 148 GB of Plex VM disk snapshots: retention left alone, with a task to [find what churns](<../projects/Find what churns 5 GB a day on the Plex VM disk.md>).

**New notes.** The runbook test task and the Plex VM churn task above, and [Narrow tier3-guard's ssh-keygen and authorized_keys rules](<../projects/Narrow tier3-guard's ssh-keygen and authorized_keys rules to commands that run or write them.md>) from the setup review's open questions. The untested fix runs became item 4 of [Verify one-tap actions on first real use](<../projects/Verify one-tap actions on first real use.md>).

**System notes corrected:** the store count and the add-on list in the two Home Assistant notes, the manual snapshots in Big Boi storage, the wake time in the wall panel note, and the kb-export token line in the ClaudeCode VM note.

## Why

The backlog had grown to 42 notes with nothing pruning it, several of them overtaken by decisions made since (the rebuild, the A380, the move of all homelab work to this VM) and two with dates that fall before the next triage. Each recommendation, with its reason, is in the session's proposal; the ones that weren't obvious:

- **Dropped rather than kept as reference** (the UNAS Pro research, the VM update tools): a dropped note isn't deleted, so the research stays searchable, and the backlog list every session reads gets shorter.
- **Certificate monitoring dropped rather than built:** only two Kuma monitors are HTTPS. Scrypted already has expiry notification on and the TrueNAS certificate runs to 2035-03-15, so there is nothing to warn about until a real certificate appears (Dockhand over HTTPS, a reverse proxy).
- **The push-rule review folded into the monthly prune** rather than kept: both read the same Alert2 fire counts and the prune is due now.
- **Memory fold empty on purpose:** moving the Remote Control line into CLAUDE.md while it is still changing would put an unsettled rule in the file meant for settled ones.

Rejected for the Plex VM snapshots: shortening the retention (a Tier 3 snapshot-task change that treats the symptom) and excluding the zvol (no rollback for the VM).

## How

Vault commits of 2026-11-15 from b2c0f38 (the live findings) through this one. Repo commit ed02839 for CLAUDE.md; it is a symlink target, so it took effect at once, and `make check` reports 40 of 40 ok.

## Verify / roll back

Verify: `~/obsidian-vault/.kb/check.py` reports 0 errors and `--projects` shows the changed statuses. Found and left alone: the Marketplace lists two repositories for the one folder `custom_components/dyson_local` (`libdyson-wg/ha-dyson`, the code on disk, and the older `shenxn/ha-dyson`); removing the stale entry through the store could delete the folder, so it wasn't touched. The `kb-export` integration still exists in Notion until Aaron removes it. Roll back: the table above has each inverse; note changes revert with `git revert`.
