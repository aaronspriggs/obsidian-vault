---
kind: recovery
status: active
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
repo: https://github.com/aaronspriggs/spriggs-homelab
notion_id: 3fb7ae76-22ba-8183-b819-cd4ce4c80569
---

# Disaster recovery: rebuild order (index)

Start here when more than one service is lost (Big Boi failure, fire, theft). The order to bring services back, the runbook for each, and the credentials a full rebuild needs. Brings Claude back second so it can drive the rest.

## When to use

More than one service is gone at once: Big Boi's pool or hardware failed, or a fire or theft. For a single service, go straight to its runbook below. For anything inside the last 30 days with the pool intact, restore from a ZFS snapshot first. This page is only the order and the links; the steps are in each runbook.

## Rebuild order

Each step depends on the ones above it. The ClaudeCode VM comes back second so that Claude can drive steps 3-5 from a Remote Control session.
1. **Big Boi (TrueNAS)**: [Rebuild Big Boi (TrueNAS) from bare metal](<Rebuild Big Boi (TrueNAS) from bare metal.md>): reinstall and upload the config (it also brings back the B2 credential); new pool only if the old one is lost. Data restore: [Offsite backup to B2 - what's covered and how to restore](<Offsite backup to B2 - what's covered and how to restore.md>).
2. **ClaudeCode VM**: [Rebuild the ClaudeCode VM from scratch](<Rebuild the ClaudeCode VM from scratch.md>). Needs only TrueNAS, 1Password and GitHub; ha-mcp comes back with step 3.
3. **Home Assistant**: [Restore Home Assistant from backup (new VM or in place)](<Restore Home Assistant from backup (new VM or in place).md>) (Path B). Needs only TrueNAS, the Google account and the HA backup encryption key; ha-mcp comes back with it.
4. **Dockhand and its stacks** (servarr, uptime-kuma, autokuma): step 4 of the B2 runbook (Dockhand DB, encryption key, stack dirs), compose files in repo `stacks/`, then [Managing the Servarr Docker Stack](<Managing the Servarr Docker Stack.md>) for the Gluetun start order.
5. **Plex VM**: [Rebuild the Plex VM from scratch](<Rebuild the Plex VM from scratch.md>). Needs the ClaudeCode VM (Claude's Plex key), the NFS exports from step 1, `plex-db.tar.gz` from B2 if the pool was lost, and Kuma from step 4 for its push URL.
Not covered here: the UDM Pro and the rest of the UniFi network (assumed working), the wall panel Pi, and bulk Plex media (re-downloadable through Seerr; self-ripped discs are backup phase 2).

## Credentials a full rebuild needs

All in Aaron's 1Password unless noted. Without the first three, the offsite copies can't be read.

| Credential | Where | Status |
| --- | --- | --- |
| 1Password account (master password, Secret Key) | Aaron | Everything else depends on it |
| B2 `truenas-bigboi`: keyID, applicationKey, **encryption password and salt** | Item "Backblaze B2 - truenas-bigboi" | Created 2026-10-16 |
| HA backup encryption key (emergency kit) | Aaron's vault | Confirmed 2026-09-29 |
| Google account (holds the HA backups in Drive) | Aaron, 2FA |  |
| GitHub (repo admin, for the deploy key) | Aaron |  |
| Claude account ([claude.ai](http://claude.ai/) login) | Email magic link to Gmail |  |
| TrueNAS admin login | Aaron's vault | Confirmed 2026-10-16 |
| UniFi account (UDM, DHCP reservations) | Aaron's vault | Confirmed 2026-10-16 |
| Plex account ([plex.tv](http://plex.tv/), Plex Pass lifetime) | Aaron's vault | Confirmed 2026-10-16 (Aaron's personal vault). Only needed if the restored `Preferences.xml` doesn't keep the claim |
| Wrapper credentials (Dockhand, UniFi read-only, *arr, Kuma, TrueNAS `claude-maint`, ha-mcp URL) | Vault `Homelab - Claude` (9 items, checked 2026-10-16) | Some may need reissuing after a TrueNAS or Dockhand rebuild |
| Service account `claudecode-vm` token, TrueNAS `claude-readonlyapi` key, obsidian-vault deploy key | Reissued on rebuild | See the ClaudeCode VM runbook |

## Verify

After each step, run that runbook's Verify section. At the end, Uptime Kuma should be all green and the HA Home Health dashboard clear. Log the recovery as a change note. The KB itself survives the loss of everything here: it is on GitHub (aaronspriggs/obsidian-vault) and in the Mac clone.

## Rollback

Not applicable: this page only orders the other runbooks, and each has its own rollback.
