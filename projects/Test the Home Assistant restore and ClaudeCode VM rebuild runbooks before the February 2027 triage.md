---
type: task
status: active
priority: low
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
next_step: '2026-11-17: Home Assistant half started. Claude checked the newest backup live (below); Aaron compares the key Home Assistant shows (Settings → System → Backups, the Encryption key card, Show) with the one in 1Password and says whether they match, then Claude sets last_tested on the restore runbook. Still to do in a fresh session: Claude dry-runs "Rebuild the ClaudeCode VM from scratch" against the repo and the live VM, fixes the runbook and sets last_tested.'
---

From the quarterly triage of 2026-11-15. Of the 12 untested runbooks, Aaron picked two to test before the next triage.

## Goal

Know that the two recovery paths that matter most would work: this VM's disk isn't backed up, and Home Assistant's backups are only worth something if the key opens them.

## Plan

1. **[Rebuild the ClaudeCode VM from scratch](<../runbooks/Rebuild the ClaudeCode VM from scratch.md>):** a dry run by Claude, no new VM. Walk every step and check each file, unit, path and command it names against `~/homelab` and the live VM; fix what has drifted (the kb-export removals of 2026-11-15, for one). A full rebuild on a throwaway VM would need Aaron to create the VM (Tier 3) and is not planned.
2. **[Restore Home Assistant from backup](<../runbooks/Restore Home Assistant from backup (new VM or in place).md>):** partial. Confirm the newest backup decrypts with the emergency-kit key in 1Password and lists its contents. Not a restore onto a second VM: a second Home Assistant on the LAN would double up cloud integrations and automations.

## Decisions

- **2026-11-15 (Aaron): the other ten are left or ride along with other work.** The Big Boi reboot checklist is exercised by the rack move and the bare-metal rebuild runbook by the rebuild; the Cloudflare DDNS runbook is checked when Ting goes live; Claude checks the dashboard reference and the Mosquitto setup against the live system alone, as it touches them. Left until needed: the disaster recovery index (tested through its parts), the appliance-image VM setup, the MFA recovery (a real test risks a lockout), the Plex VM rebuild (after the Big Boi rebuild) and the wall panel troubleshooting (Claude has no SSH to the Pi).

## Status (2026-11-17)

Home Assistant restore, Claude's half: the newest automatic backup (`f1d6befb`, 2026-11-16 05:19, Core 2026.11.0, 409.6 MB) is in both locations (`hassio.local` and Google Drive), is encrypted in both (`protected: true`), and holds the settings, the database, all five add-ons and the `ssl` folder, with no failed parts. The restore runbook's "What a backup holds" section was corrected to match.

Aaron's half: compare the key. Where it is, per the [Home Assistant docs](https://www.home-assistant.io/more-info/backup-emergency-kit/) (read 2026-11-17, docs build 2026.11.2): Settings → System → Backups, on the **Encryption key** card, **Show** next to "Show my encryption key", or **Download** next to "Download emergency kit" for a text file holding the key. The key is seven groups of four characters with hyphens. Claude first sent Aaron to `/config/backup/settings`, from memory, and he found nothing there that shows the key. Claude never sees it: the key is in Aaron's own 1Password vault, and typing it into a chat would leave it in the session log on this VM. A match between the key Home Assistant is using and the 1Password copy means the automatic backups, which are encrypted with that key, open with it. It is not a restore; the runbook stays "not yet test-restored".
