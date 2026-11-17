---
date: 2026-11-17
type: doc
system:
- '[[Home Assistant OS (VM)]]'
project: '[[Test the Home Assistant restore and ClaudeCode VM rebuild runbooks before the February 2027 triage]]'
---

## What changed

No system changes. The [restore runbook](<../runbooks/Restore Home Assistant from backup (new VM or in place).md>) got `last_tested: 2026-11-17` for a partial test, and its prerequisites now say where Home Assistant shows the key. The [disaster recovery index](<../runbooks/Disaster recovery - rebuild order (index).md>) has the new date for the key.

## Why

Aaron picked this runbook at the 2026-11-15 triage as one of two to test before February 2027. A restore onto a second VM was ruled out (a second Home Assistant on the LAN would double up cloud integrations and automations), so the test is of the two things a restore depends on: a complete backup, and a key that opens it.

## How

- **Backup (Claude, ha-mcp):** the newest automatic backup, `f1d6befb` of 2026-11-16 05:19, Core 2026.11.0, 409.6 MB, is in `hassio.local` and in Google Drive, encrypted in both, with settings, database, five add-ons and the `ssl` folder and no failed parts.
- **Key (Aaron):** saved from Home Assistant into 1Password on 2026-11-17, from Settings → System → Backups, the Encryption key card ([docs](https://www.home-assistant.io/more-info/backup-emergency-kit/)). Claude never saw it. The item name isn't recorded yet.

Not done: no backup was decrypted or restored. ha-mcp has no decrypt-only check, and a real restore is Tier 3.

## How to verify / roll back

Nothing to roll back. To repeat: `ha_manage_backup` lists the backups and their locations; the key is compared by Aaron on the Encryption key card.
