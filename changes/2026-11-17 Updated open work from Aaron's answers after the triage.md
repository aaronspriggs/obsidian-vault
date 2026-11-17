---
date: 2026-11-17
type: doc
system:
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
- '[[Home Assistant (integrations and automations)]]'
project:
- '[[Quarterly KB triage with Aaron (Deferred items and Ideas)]]'
- '[[Revoke the unused kb-export Notion integration token]]'
- '[[Factory-reset and sell the two Nest thermostats]]'
- '[[Test the Home Assistant restore and ClaudeCode VM rebuild runbooks before the February 2027 triage]]'
---

# Updated open work from Aaron's answers after the triage

## What changed

After the [first quarterly triage](<2026-11-15 Ran the first quarterly KB triage.md>) Claude gave Aaron a list of the 22 things waiting on him. He answered each on 2026-11-17, and the notes now say what he said. Nothing on any system was changed by Claude; the one live change is Aaron's.

- **Done:** [the kb-export token](<../projects/Revoke the unused kb-export Notion integration token.md>): Aaron deleted the `kb-export` integration in Notion, which revokes the token (the local copy went on 2026-11-15). [The Nest thermostats](<../projects/Factory-reset and sell the two Nest thermostats.md>): both reset and listed; both ecobees read live as online.
- **Back to the backlog:** the AV1 pipeline (Aaron isn't concerned about the A380's return window, the only reason it had been made active) and the houseplant sensors (pick up later).
- **Blocked on the 30U rack move:** the UPS power-loss test and the camera migration.
- **Dated or corrected next steps:** both credential rotations move to the week of 2026-12-21 (Aaron: end of December, not now); the USW Aggregation was bought 2026-11-11 with a 30-day return window; two UACC-CM-RJ45-MG modules are in hand for Ting (one spare); the SFF-8643 cables and the UP Siren PoE are in hand; the 12S4 won't be measured on arrival.
- **Unchanged, for later or for their own chats:** the leak sensor battery, Scrypted's HKSV check, the leak test, the mod UI re-test with the mods review, the security go-ahead, the wife's account and the gear-selling questions.
- **B2 bucket size:** stays with Aaron. Claude has no B2 credentials, and the TrueNAS API can't report a bucket's size including old file versions.
- **Home Assistant backup check, half done.** Read live through ha-mcp: the newest automatic backup (`f1d6befb`, 2026-11-16 05:19, 409.6 MB) is in `hassio.local` and Google Drive, encrypted in both, with settings, database, five add-ons and the `ssl` folder. The [restore runbook](<../runbooks/Restore Home Assistant from backup (new VM or in place).md>) said backups hold Spotify Connect and no `ssl` folder and are about 430 MB; corrected. Aaron still compares the key Home Assistant shows with the one in 1Password.

## Why

The list was built from next steps, some of them weeks old; his answers closed two tasks, removed two deadlines and showed five purchases already made. The key comparison is left to Aaron rather than done by Claude because the key lives in his own 1Password vault and passing it through a chat would write it into the session log on this VM. Rejected: giving Claude a read-only B2 key for a single size check (a new credential for one number he can read in a minute).

## How

This vault commit. No repo change.

## Verify / roll back

Verify: `.kb/check.py` reports 0 errors and `--health` lists no gaps. Roll back: `git revert` this commit.
