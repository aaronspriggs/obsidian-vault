---
type: task
status: active
priority: low
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
next_step: '2026-11-15: picked by Aaron at the quarterly triage. In a fresh session Claude dry-runs "Rebuild the ClaudeCode VM from scratch" against the repo and the live VM (every file, unit and step it names exists and matches), fixes the runbook and sets last_tested. Then, with Aaron: confirm the newest Home Assistant backup opens with the encryption key from 1Password, and set last_tested on the restore runbook. Both before February 2027.'
---

From the quarterly triage of 2026-11-15. Of the 12 untested runbooks, Aaron picked two to test before the next triage.

## Goal

Know that the two recovery paths that matter most would work: this VM's disk isn't backed up, and Home Assistant's backups are only worth something if the key opens them.

## Plan

1. **[Rebuild the ClaudeCode VM from scratch](<../runbooks/Rebuild the ClaudeCode VM from scratch.md>):** a dry run by Claude, no new VM. Walk every step and check each file, unit, path and command it names against `~/homelab` and the live VM; fix what has drifted (the kb-export removals of 2026-11-15, for one). A full rebuild on a throwaway VM would need Aaron to create the VM (Tier 3) and is not planned.
2. **[Restore Home Assistant from backup](<../runbooks/Restore Home Assistant from backup (new VM or in place).md>):** partial. Confirm the newest backup decrypts with the emergency-kit key in 1Password and lists its contents. Not a restore onto a second VM: a second Home Assistant on the LAN would double up cloud integrations and automations.

## Decisions

- **2026-11-15 (Aaron): the other ten are left or ride along with other work.** The Big Boi reboot checklist is exercised by the rack move and the bare-metal rebuild runbook by the rebuild; the Cloudflare DDNS runbook is checked when Ting goes live; Claude checks the dashboard reference and the Mosquitto setup against the live system alone, as it touches them. Left until needed: the disaster recovery index (tested through its parts), the appliance-image VM setup, the MFA recovery (a real test risks a lockout), the Plex VM rebuild (after the Big Boi rebuild) and the wall panel troubleshooting (Claude has no SSH to the Pi).
